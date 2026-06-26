"""예방 레이어 규칙 '정의' (데이터).

근거: docs/PREVENTION_LAYER_SPEC.md 2·6·7절 (규칙 정의 / 실행 엔진 분리).
여기에는 '얼마로 계산하는지'(가중치·임계값·오버라이드 조건)만 있다.
'어떻게 계산하는지'(절차)는 engine.py 에 있다.

진화 가능성: 새 발견이 생기면 engine.py 코드를 갈아엎지 않고 이 파일의 값만 갱신한다.
v0.1 한계선(과추상화 금지, DECISIONS 2.10): 외부 파일/DB 로더·DSL 없음. DEFAULT_RULESET 하나까지만.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TrendRules(BaseModel):
    """추세: stress = risk_weight*risk + unc_weight*uncertainty, trend = clamp01(delta*gain)."""

    risk_weight: float = 0.6
    unc_weight: float = 0.4
    gain: float = 1.5


class ImbalanceRules(BaseModel):
    """균형 이탈: 소비-회복 gap + 자원추구×위험노출."""

    energy_w: float = 0.5       # consumption_gap 내 energy_level 가중
    recovery_w: float = 0.5     # consumption_gap 내 recovery_capacity 가중
    consumption_w: float = 0.5  # 최종 결합: 소비 gap
    exposure_w: float = 0.5     # 최종 결합: 노출


class EarlyWarningRules(BaseModel):
    """조기 신호: 크기(magnitude) + 반복 지속성(persistence)."""

    magnitude_w: float = 0.5
    persistence_w: float = 0.5
    max_flags: int = 3  # reading 당 정규화 기준 최대 이상신호 수


class PriorityWeights(BaseModel):
    """예방 행동 우선순위 가중합. (합이 꼭 1일 필요는 없으나 0~1 클램프됨)"""

    trend_w: float = 0.40
    imbalance_w: float = 0.20
    early_w: float = 0.30
    low_recovery_w: float = 0.10  # (1 - recovery_capacity) 에 곱


class StatusThresholds(BaseModel):
    """preventive_action_priority -> prevention_status 경계."""

    watch: float = 0.20
    adjust: float = 0.40
    restrict: float = 0.60
    shelter: float = 0.80


class OverrideRules(BaseModel):
    """기본 임계값보다 우선하는 안전 오버라이드."""

    # 급변 대피: 조기신호 매우 높음 + 회복 바닥 + 추세 급악화 -> shelter_or_abort
    acute_ew_min: float = 0.80
    acute_recovery_max: float = 0.20
    acute_trend_min: float = 0.70
    # 회복 바닥 플로어: 회복 낮음 + 일정 우선순위 이상 -> 최소 restrict
    floor_recovery_max: float = 0.30
    floor_priority_min: float = 0.25


class ReasonRules(BaseModel):
    """reason_code 부여 임계값."""

    trend_min: float = 0.30
    imbalance_min: float = 0.30
    early_min: float = 0.40
    early_persistence_min: float = 0.50  # '반복'으로 인정할 최소 지속성


class PreventionRuleSet(BaseModel):
    """예방 레이어의 모든 규칙 정의를 담는 단일 값 객체. 가변(규칙 교체 가능)."""

    trend: TrendRules = Field(default_factory=TrendRules)
    imbalance: ImbalanceRules = Field(default_factory=ImbalanceRules)
    early: EarlyWarningRules = Field(default_factory=EarlyWarningRules)
    priority: PriorityWeights = Field(default_factory=PriorityWeights)
    thresholds: StatusThresholds = Field(default_factory=StatusThresholds)
    overrides: OverrideRules = Field(default_factory=OverrideRules)
    reason: ReasonRules = Field(default_factory=ReasonRules)


# 기본 규칙 묶음. 새 발견이 생기면 이 값들을 갱신하거나, 사본을 만들어 engine 에 주입한다.
DEFAULT_RULESET = PreventionRuleSet()
