"""예방 레이어 데이터 형태 (입력/출력/enum).

근거: docs/PREVENTION_LAYER_SPEC.md 5·9절.
이 모듈은 '형태'만 정의한다. 계산 규칙(상수)은 rules.py, 계산 절차는 engine.py.
gwan_judgment 를 import 하지 않는다(약한 상호 참조: severity 는 값으로만 받는다).
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PreventionStatus(str, Enum):
    """예방(흐름) 상태. severity(순간)와 별개 축. shelter_or_abort 채택(SPEC 4절)."""

    NORMAL = "normal"
    WATCH = "watch"
    ADJUST = "adjust"
    RESTRICT = "restrict"
    SHELTER_OR_ABORT = "shelter_or_abort"


class HolisticState(str, Enum):
    """severity × prevention 을 함께 본 서술적 상태(행동 강제 아님, SPEC 7.3)."""

    STABLE = "stable"
    EARLY_DRIFT = "early_drift"
    ACUTE_BUFFERED_RECOVERABLE = "acute_buffered_recoverable"
    COMPOUND_ESCALATION = "compound_escalation"
    PREVENTION_ONLY = "prevention_only"


class FlowAxis(str, Enum):
    """흐름의 성격(씨앗). v0.1 engine은 temporal만 실제 계산(SPEC 5.1)."""

    TEMPORAL = "temporal"  # 시간 흐름
    SPATIAL = "spatial"    # 공간 이동 경로 흐름
    MIXED = "mixed"


# severity 어휘는 gwan_judgment 를 import 하지 않고 값으로만 참조(침범 금지, SPEC 3절).
_ALLOWED_SEVERITY = {"normal", "watch", "adjust", "restrict", "abort"}


class PreventionReading(BaseModel):
    """한 시점의 관측. 모든 신호는 0.0~1.0, anomaly_flags 만 정수."""

    composite_risk: float = Field(..., ge=0.0, le=1.0)
    uncertainty: float = Field(..., ge=0.0, le=1.0)
    energy_level: float = Field(..., ge=0.0, le=1.0)
    energy_consumption_rate: float = Field(..., ge=0.0, le=1.0)
    recovery_capacity: float = Field(..., ge=0.0, le=1.0)  # 기존 입력 재사용(passthrough)
    resource_pursuit: float = Field(..., ge=0.0, le=1.0)
    risk_exposure: float = Field(..., ge=0.0, le=1.0)
    anomaly_flags: int = Field(0, ge=0)
    # ↓ 씨앗(v0.1 계산 미사용, SPEC 5.1): 자리만 마련. engine은 읽지 않는다.
    energy_signal: Optional[float] = Field(None, ge=0.0, le=1.0)  # 환경 빛/에너지 신호 강도(잔량과 다름)


class PreventionInput(BaseModel):
    """예방 평가 입력. 시간창(readings) + severity 약한 참조."""

    readings: list[PreventionReading] = Field(..., min_length=1)
    severity_context: Optional[str] = None  # 현재 severity 값(없으면 None). import 아님, 데이터.
    # ↓ 씨앗(v0.1 계산 미사용, SPEC 5.1): 흐름의 성격. v0.1 engine은 temporal만 실제 계산.
    flow_axis: FlowAxis = FlowAxis.TEMPORAL

    @field_validator("severity_context")
    @classmethod
    def _validate_severity(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _ALLOWED_SEVERITY:
            raise ValueError(
                f"severity_context must be one of {sorted(_ALLOWED_SEVERITY)} or None"
            )
        return v


class PreventionAssessment(BaseModel):
    """예방 평가 출력."""

    trend_score: float
    imbalance_score: float
    early_warning_score: float
    recovery_capacity: float  # passthrough
    preventive_action_priority: float
    prevention_status: PreventionStatus
    severity_context: Optional[str]  # 읽기 전용 에코(침범 금지)
    holistic_state: HolisticState
    reason_codes: list[str]
    reason_summary: str
