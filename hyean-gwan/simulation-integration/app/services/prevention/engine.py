"""예방 레이어 규칙 '실행' (엔진).

근거: docs/PREVENTION_LAYER_SPEC.md 6·7절.
이 모듈은 '어떻게 계산하는지'(절차)만 안다. 가중치·임계값·조건은 ruleset 에서 읽고
숫자를 하드코딩하지 않는다. (0.0/1.0 은 점수의 계약상 정규화 범위이지 튜닝 규칙이 아님)

gwan_judgment 를 import 하지 않는다. severity 는 PreventionInput.severity_context 값으로만 참조.
"""

from __future__ import annotations

from typing import Optional

from .models import (
    HolisticState,
    PreventionAssessment,
    PreventionInput,
    PreventionReading,
    PreventionStatus,
)
from .rules import (
    DEFAULT_RULESET,
    EarlyWarningRules,
    ImbalanceRules,
    PreventionRuleSet,
    PriorityWeights,
    TrendRules,
)


def clamp01(x: float) -> float:
    """점수를 계약상 정규화 범위[0,1]로 자른다(규칙 상수가 아니라 구조적 불변)."""
    return max(0.0, min(1.0, x))


# 흐름 상태 심각도 순서(비교용). 값이 아니라 순서 관계.
_STATUS_ORDER = {
    PreventionStatus.NORMAL: 0,
    PreventionStatus.WATCH: 1,
    PreventionStatus.ADJUST: 2,
    PreventionStatus.RESTRICT: 3,
    PreventionStatus.SHELTER_OR_ABORT: 4,
}

_SEVERITY_HIGH = {"restrict", "abort"}


def _stress(reading: PreventionReading, t: TrendRules) -> float:
    return t.risk_weight * reading.composite_risk + t.unc_weight * reading.uncertainty


def calc_trend(readings: list[PreventionReading], t: TrendRules) -> float:
    """추세 점수. 단일 reading 이면 추세 정보가 없으므로 0.0."""
    if len(readings) < 2:
        return 0.0
    stresses = [_stress(r, t) for r in readings]
    n = len(stresses)
    half = n // 2
    earlier = stresses[:half]
    later = stresses[n - half:]
    delta = (sum(later) / len(later)) - (sum(earlier) / len(earlier))
    return clamp01(delta * t.gain)  # 개선/안정(delta<=0)은 0으로 수렴


def calc_imbalance(last: PreventionReading, im: ImbalanceRules) -> float:
    """균형 이탈 점수(최신 reading 기준)."""
    headroom = im.energy_w * last.energy_level + im.recovery_w * last.recovery_capacity
    consumption_gap = max(0.0, last.energy_consumption_rate - headroom)
    exposure = last.resource_pursuit * last.risk_exposure
    return clamp01(im.consumption_w * consumption_gap + im.exposure_w * exposure)


def calc_early_warning(
    readings: list[PreventionReading], ew: EarlyWarningRules
) -> tuple[float, float]:
    """조기 신호 점수와 지속성(반복 정도)을 함께 반환."""
    n = len(readings)
    total_flags = sum(r.anomaly_flags for r in readings)
    magnitude = total_flags / (n * ew.max_flags) if ew.max_flags > 0 else 0.0
    flagged = sum(1 for r in readings if r.anomaly_flags >= 1)
    persistence = flagged / n
    score = clamp01(ew.magnitude_w * magnitude + ew.persistence_w * persistence)
    return score, persistence


def calc_priority(
    trend: float, imbalance: float, early: float, recovery: float, pr: PriorityWeights
) -> float:
    return clamp01(
        pr.trend_w * trend
        + pr.imbalance_w * imbalance
        + pr.early_w * early
        + pr.low_recovery_w * (1.0 - recovery)
    )


def derive_status(
    priority: float,
    recovery: float,
    early: float,
    trend: float,
    ruleset: PreventionRuleSet,
) -> tuple[PreventionStatus, bool, bool]:
    """기본 임계값 + 오버라이드로 prevention_status 결정. (status, acute, floor) 반환."""
    th = ruleset.thresholds
    if priority < th.watch:
        status = PreventionStatus.NORMAL
    elif priority < th.adjust:
        status = PreventionStatus.WATCH
    elif priority < th.restrict:
        status = PreventionStatus.ADJUST
    elif priority < th.shelter:
        status = PreventionStatus.RESTRICT
    else:
        status = PreventionStatus.SHELTER_OR_ABORT

    ov = ruleset.overrides
    acute = False
    floor = False
    if (
        early >= ov.acute_ew_min
        and recovery <= ov.acute_recovery_max
        and trend >= ov.acute_trend_min
    ):
        status = PreventionStatus.SHELTER_OR_ABORT
        acute = True
    elif recovery <= ov.floor_recovery_max and priority >= ov.floor_priority_min:
        if _STATUS_ORDER[status] < _STATUS_ORDER[PreventionStatus.RESTRICT]:
            status = PreventionStatus.RESTRICT
        floor = True

    return status, acute, floor


def derive_holistic(
    severity: Optional[str], status: PreventionStatus
) -> tuple[HolisticState, bool]:
    """severity(순간) × prevention(흐름) 동시 관찰. (holistic_state, divergence) 반환."""
    if severity is None:
        return HolisticState.PREVENTION_ONLY, False

    sev_high = severity in _SEVERITY_HIGH
    prev_high = _STATUS_ORDER[status] >= _STATUS_ORDER[PreventionStatus.ADJUST]

    if sev_high and prev_high:
        return HolisticState.COMPOUND_ESCALATION, False
    if sev_high and not prev_high:
        return HolisticState.ACUTE_BUFFERED_RECOVERABLE, True
    if not sev_high and prev_high:
        return HolisticState.EARLY_DRIFT, True
    return HolisticState.STABLE, False


def _build_reason_codes(
    trend: float,
    imbalance: float,
    early: float,
    persistence: float,
    acute: bool,
    floor: bool,
    divergence: bool,
    ruleset: PreventionRuleSet,
) -> list[str]:
    rr = ruleset.reason
    codes: list[str] = []
    if trend >= rr.trend_min:
        codes.append("TREND_WORSENING")
    if imbalance >= rr.imbalance_min:
        codes.append("IMBALANCE_HIGH")
    if early >= rr.early_min and persistence >= rr.early_persistence_min:
        codes.append("REPEATED_ANOMALY")
    if floor:
        codes.append("LOW_RECOVERY_FLOOR")
    if acute:
        codes.append("ACUTE_SHELTER")
    if divergence:
        codes.append("SEVERITY_PREVENTION_DIVERGENCE")
    return codes


def _build_reason_summary(
    status: PreventionStatus, holistic: HolisticState
) -> str:
    base = f"prevention_status={status.value}, holistic_state={holistic.value}. "
    if holistic == HolisticState.ACUTE_BUFFERED_RECOVERABLE:
        base += "완충 여력이 남아 관측·조정으로 대응 가능(급성이나 회복 여지 있음)."
    elif holistic == HolisticState.COMPOUND_ESCALATION:
        base += "여력이 소진되며 순간·흐름이 함께 악화 — 대피(shelter) 쪽으로 무게."
    elif holistic == HolisticState.EARLY_DRIFT:
        base += "순간 위험은 낮으나 흐름이 먼저 악화(조기 경보)."
    elif holistic == HolisticState.STABLE:
        base += "순간·흐름 모두 안정."
    else:
        base += "severity 미제공 — 흐름(예방) 기준만으로 판단."
    return base


def assess_prevention(
    data: PreventionInput, ruleset: PreventionRuleSet = DEFAULT_RULESET
) -> PreventionAssessment:
    """예방 평가 공개 API. 규칙(ruleset)을 주입받아 흐름 상태를 산출한다."""
    readings = data.readings
    last = readings[-1]

    trend = calc_trend(readings, ruleset.trend)
    imbalance = calc_imbalance(last, ruleset.imbalance)
    early, persistence = calc_early_warning(readings, ruleset.early)
    recovery = last.recovery_capacity  # passthrough(재계산 없음)
    priority = calc_priority(trend, imbalance, early, recovery, ruleset.priority)

    status, acute, floor = derive_status(priority, recovery, early, trend, ruleset)
    holistic, divergence = derive_holistic(data.severity_context, status)

    reason_codes = _build_reason_codes(
        trend, imbalance, early, persistence, acute, floor, divergence, ruleset
    )
    reason_summary = _build_reason_summary(status, holistic)

    return PreventionAssessment(
        trend_score=trend,
        imbalance_score=imbalance,
        early_warning_score=early,
        recovery_capacity=recovery,
        preventive_action_priority=priority,
        prevention_status=status,
        severity_context=data.severity_context,
        holistic_state=holistic,
        reason_codes=reason_codes,
        reason_summary=reason_summary,
    )
