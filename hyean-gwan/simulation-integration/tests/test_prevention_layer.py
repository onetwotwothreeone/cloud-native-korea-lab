"""예방 레이어 v0.1 동작 검증 테스트 (TDD: 구현 전 red).

근거: docs/PREVENTION_LAYER_SPEC.md 8절 시나리오 S1~S9.
이 테스트는 "단어가 문서에 있나"가 아니라 "입력 -> 출력 값이 규칙대로 나오나"를 검사한다.
특히:
  - S7/S8: severity 와 prevention 의 '약한 상호 참조'(holistic, acute_buffered_recoverable 포함)
  - S9: 동일 입력 + 다른 ruleset -> 다른 결과 (규칙 정의/실행 엔진 분리 = 진화 가능성)

구현(app/services/prevention/)이 아직 없으므로 import 단계에서 실패(red)하는 것이 정상이다.
"""

import copy

import pytest

# 아직 존재하지 않는 모듈 — 구현 전에는 ModuleNotFoundError 로 red 가 정상.
from app.services.prevention import assess_prevention
from app.services.prevention.models import (
    FlowAxis,
    HolisticState,
    PreventionInput,
    PreventionReading,
    PreventionStatus,
)
from app.services.prevention.rules import DEFAULT_RULESET


# --------------------------------------------------------------------------- #
# 헬퍼
# --------------------------------------------------------------------------- #
def reading(**overrides):
    """안전·균형 잡힌 기본 reading. 시나리오별로 필요한 값만 override."""
    base = dict(
        composite_risk=0.20,
        uncertainty=0.20,
        energy_level=0.80,
        energy_consumption_rate=0.20,
        recovery_capacity=0.80,
        resource_pursuit=0.20,
        risk_exposure=0.20,
        anomaly_flags=0,
    )
    base.update(overrides)
    return PreventionReading(**base)


_STATUS_ORDER = {
    "normal": 0,
    "watch": 1,
    "adjust": 2,
    "restrict": 3,
    "shelter_or_abort": 4,
}


def _v(value):
    """enum 이든 str 이든 문자열 값으로 정규화."""
    return getattr(value, "value", value)


def _rank(status):
    return _STATUS_ORDER[_v(status)]


# --------------------------------------------------------------------------- #
# S1: 위험 낮지만 불확실↑ & 추세 악화 -> watch 이상
# --------------------------------------------------------------------------- #
def test_s1_low_risk_but_worsening_trend_reaches_watch():
    inp = PreventionInput(
        readings=[
            reading(composite_risk=0.20, uncertainty=0.30),
            reading(composite_risk=0.35, uncertainty=0.85),  # 불확실성 악화
        ]
    )
    result = assess_prevention(inp)

    assert result.trend_score > 0.0  # 추세가 잡혀야 함
    assert _rank(result.prevention_status) >= _STATUS_ORDER["watch"]


# --------------------------------------------------------------------------- #
# S2: 자원 가치 높아도 recovery_capacity 낮음 -> restrict (회복 바닥 플로어)
# --------------------------------------------------------------------------- #
def test_s2_low_recovery_floor_forces_restrict():
    inp = PreventionInput(
        readings=[
            reading(
                composite_risk=0.40, uncertainty=0.40, energy_level=0.40,
                energy_consumption_rate=0.60, recovery_capacity=0.15,
                resource_pursuit=0.90, risk_exposure=0.60,
            ),
            reading(
                composite_risk=0.55, uncertainty=0.50, energy_level=0.35,
                energy_consumption_rate=0.65, recovery_capacity=0.15,
                resource_pursuit=0.90, risk_exposure=0.65,
            ),
        ]
    )
    result = assess_prevention(inp)

    assert _v(result.prevention_status) == "restrict"
    assert "LOW_RECOVERY_FLOOR" in result.reason_codes


# --------------------------------------------------------------------------- #
# S3: 방사선·통신잡음·센서오차가 반복 증가 -> adjust 또는 restrict
# --------------------------------------------------------------------------- #
def test_s3_repeated_anomalies_reach_adjust_or_restrict():
    inp = PreventionInput(
        readings=[
            reading(composite_risk=0.30, anomaly_flags=2, risk_exposure=0.40),
            reading(composite_risk=0.45, anomaly_flags=2, risk_exposure=0.50),
            reading(composite_risk=0.55, anomaly_flags=3, risk_exposure=0.50,
                    recovery_capacity=0.50),
        ]
    )
    result = assess_prevention(inp)

    assert result.early_warning_score > 0.0
    assert _v(result.prevention_status) in {"adjust", "restrict"}
    assert "REPEATED_ANOMALY" in result.reason_codes


# --------------------------------------------------------------------------- #
# S4: SEP 급변 + 회복 여력 낮음 -> shelter_or_abort (급변 대피 오버라이드)
# --------------------------------------------------------------------------- #
def test_s4_acute_spike_low_recovery_triggers_shelter():
    inp = PreventionInput(
        readings=[
            reading(composite_risk=0.30, uncertainty=0.40, anomaly_flags=3,
                    recovery_capacity=0.15),
            reading(composite_risk=0.95, uncertainty=0.90, anomaly_flags=3,
                    recovery_capacity=0.12, risk_exposure=0.80),
        ]
    )
    result = assess_prevention(inp)

    assert _v(result.prevention_status) == "shelter_or_abort"
    assert "ACUTE_SHELTER" in result.reason_codes


# --------------------------------------------------------------------------- #
# S5: 안정·균형·이상신호 없음 -> normal
# --------------------------------------------------------------------------- #
def test_s5_stable_balanced_is_normal():
    inp = PreventionInput(readings=[reading(), reading()])
    result = assess_prevention(inp)

    assert _v(result.prevention_status) == "normal"


# --------------------------------------------------------------------------- #
# S6: 단일 reading(추세 정보 없음) -> trend_score == 0.0, 안전 동작
# --------------------------------------------------------------------------- #
def test_s6_single_reading_has_zero_trend():
    inp = PreventionInput(
        readings=[reading(composite_risk=0.50, uncertainty=0.50)]
    )
    result = assess_prevention(inp)

    assert result.trend_score == 0.0  # 추세를 계산할 창이 없음


# --------------------------------------------------------------------------- #
# S7: severity=restrict(순간 높음) + prevention 낮음 -> acute_buffered_recoverable
#     (약한 상호 참조: divergence 표시, 어느 쪽도 침범하지 않음)
# --------------------------------------------------------------------------- #
def test_s7_high_severity_low_prevention_is_acute_buffered_recoverable():
    inp = PreventionInput(
        readings=[reading(), reading()],   # 흐름은 안정 -> prevention 낮음
        severity_context="restrict",       # 순간 위험은 높음 (값으로만 주입)
    )
    result = assess_prevention(inp)

    assert _v(result.holistic_state) == "acute_buffered_recoverable"
    assert "SEVERITY_PREVENTION_DIVERGENCE" in result.reason_codes
    # 침범 금지: severity_context 는 그대로 에코될 뿐 변형되지 않음
    assert result.severity_context == "restrict"


# --------------------------------------------------------------------------- #
# S8: severity=normal(순간 낮음) + prevention 높음(adjust↑) -> early_drift
#     (흐름이 먼저 경고하는 동양의학적 조기 발견)
# --------------------------------------------------------------------------- #
def test_s8_low_severity_high_prevention_is_early_drift():
    inp = PreventionInput(
        readings=[
            reading(composite_risk=0.35, uncertainty=0.50, anomaly_flags=1,
                    energy_level=0.40, energy_consumption_rate=0.60,
                    recovery_capacity=0.40, resource_pursuit=0.70,
                    risk_exposure=0.60),
            reading(composite_risk=0.60, uncertainty=0.70, anomaly_flags=2,
                    energy_level=0.35, energy_consumption_rate=0.65,
                    recovery_capacity=0.40, resource_pursuit=0.75,
                    risk_exposure=0.65),
        ],
        severity_context="normal",
    )
    result = assess_prevention(inp)

    assert _rank(result.prevention_status) >= _STATUS_ORDER["adjust"]
    assert _v(result.holistic_state) == "early_drift"


# --------------------------------------------------------------------------- #
# S9: 동일 입력 + 다른 ruleset -> 다른 결과
#     (규칙 '정의'(rules)와 '실행'(engine) 분리 = 진화 가능성: 엔진 코드 무수정)
# --------------------------------------------------------------------------- #
def test_s9_same_input_different_ruleset_changes_outcome():
    inp = PreventionInput(
        readings=[
            reading(composite_risk=0.25, uncertainty=0.40),
            reading(composite_risk=0.60, uncertainty=0.85),  # 추세 지배적
        ]
    )

    # 새 발견을 반영해 규칙만 교체 (엔진 코드는 건드리지 않음)
    evolved = copy.deepcopy(DEFAULT_RULESET)
    evolved.trend.gain = 0.0  # 추세 민감도 제거

    base_result = assess_prevention(inp)
    evolved_result = assess_prevention(inp, ruleset=evolved)

    # 규칙이 결과를 바꾼다 = 진화 가능성
    assert evolved_result.trend_score == 0.0
    assert base_result.trend_score > evolved_result.trend_score
    assert _v(base_result.prevention_status) != _v(evolved_result.prevention_status)


# --------------------------------------------------------------------------- #
# 씨앗 필드: energy_signal / flow_axis 는 자리만 있고 v0.1 계산에 미반영
# (SPEC 5.1) — 주든 안 주든 결과가 동일해야 함.
# --------------------------------------------------------------------------- #
def test_seed_energy_signal_is_not_used_in_v0_1():
    """energy_signal 을 줘도(0.x) 안 줘도(None) 평가 결과가 동일 = 아직 계산에 안 쓰임."""
    without = assess_prevention(
        PreventionInput(
            readings=[
                reading(composite_risk=0.30, uncertainty=0.40),
                reading(composite_risk=0.50, uncertainty=0.70),
            ]
        )
    )
    with_signal = assess_prevention(
        PreventionInput(
            readings=[
                reading(composite_risk=0.30, uncertainty=0.40, energy_signal=0.40),
                reading(composite_risk=0.50, uncertainty=0.70, energy_signal=0.60),
            ]
        )
    )
    assert without.model_dump() == with_signal.model_dump()


def test_seed_flow_axis_spatial_equals_temporal_in_v0_1():
    """flow_axis=spatial 로 줘도 temporal(기본)과 동일 결과 = 자리만 있고 미사용."""
    readings = [
        reading(composite_risk=0.30, uncertainty=0.40, anomaly_flags=1),
        reading(composite_risk=0.55, uncertainty=0.75, anomaly_flags=2),
    ]
    temporal = assess_prevention(
        PreventionInput(readings=readings, flow_axis=FlowAxis.TEMPORAL)
    )
    spatial = assess_prevention(
        PreventionInput(readings=readings, flow_axis=FlowAxis.SPATIAL)
    )
    assert temporal.model_dump() == spatial.model_dump()
    # 기본값이 temporal 임도 확인
    assert PreventionInput(readings=readings).flow_axis == FlowAxis.TEMPORAL
