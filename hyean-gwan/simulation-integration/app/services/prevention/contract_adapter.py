"""예방 평가 → 계약(PreventionReport) 경계 번역기. (H4 (가))

느슨한 BaseModel(PreventionAssessment) → 엄격한 ContractBaseModel(PreventionReport).
engine/rules 의 계산 로직은 건드리지 않는다. 모든 필드를 값 그대로 옮긴다(왜곡 0, 품질 가드).
severity_context 는 echo 만(침범 금지, SPEC 3절). recommended_action 은 만들지 않는다(행동 게이트 금지선, D4).
"""

from __future__ import annotations

from app.schemas.gwan_interface import PreventionReport
from app.services.prevention.models import PreventionAssessment


def to_prevention_report(assessment: PreventionAssessment) -> PreventionReport:
    """PreventionAssessment 의 전 필드를 PreventionReport 로 100% 동일 복사."""
    return PreventionReport(
        trend_score=assessment.trend_score,
        imbalance_score=assessment.imbalance_score,
        early_warning_score=assessment.early_warning_score,
        recovery_capacity=assessment.recovery_capacity,
        preventive_action_priority=assessment.preventive_action_priority,
        prevention_status=assessment.prevention_status,
        severity_context=assessment.severity_context,  # echo only
        holistic_state=assessment.holistic_state,
        reason_codes=list(assessment.reason_codes),
        reason_summary=assessment.reason_summary,
    )
