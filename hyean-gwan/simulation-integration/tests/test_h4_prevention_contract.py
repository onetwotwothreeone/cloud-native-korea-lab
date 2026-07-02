"""H4 (가)+(나) 계약 편입 검증 테스트 (TDD: 구현 전 red).

근거: docs/H4_INTEGRATION_SPEC.md (D1~D7 확정).
검증 대상:
  - 어댑터 번역 정확성: PreventionAssessment -> PreventionReport 전 필드 100% 일치 (품질 가드)
  - severity_context echo 불변
  - 행동 게이트 금지선: PreventionReport 에 recommended_action 필드 '없음'
  - 비파괴: prevention 미포함 기존 페이로드가 여전히 유효 (default None)
  - schema_version v0.1 유지

구현(PreventionReport / to_prevention_report)이 아직 없으므로 import 단계에서 red 가 정상이다.
"""

# 아직 존재하지 않는 계약 스키마 / 어댑터 — 구현 전에는 ImportError 로 red 가 정상.
from app.schemas.gwan_interface import PreventionReport
from app.services.gwan_simulation import generate_first_simulation_payload
from app.services.prevention import assess_prevention
from app.services.prevention.contract_adapter import to_prevention_report
from app.services.prevention.models import PreventionInput, PreventionReading


# 전체 거울(D3): PreventionReport 가 가져야 하는 정확한 필드 집합.
MIRROR_FIELDS = [
    "trend_score",
    "imbalance_score",
    "early_warning_score",
    "recovery_capacity",
    "preventive_action_priority",
    "prevention_status",
    "severity_context",
    "holistic_state",
    "reason_codes",
    "reason_summary",
]


def _norm(value):
    """enum -> 값, list[enum/str] -> list[값] 으로 정규화해 비교 가능하게."""
    if isinstance(value, list):
        return [getattr(item, "value", item) for item in value]
    return getattr(value, "value", value)


def _sample_assessment(severity_context: str = "restrict"):
    """비자명한 값(점수·상태·이유코드 다수)이 나오는 평가 하나."""
    inp = PreventionInput(
        readings=[
            PreventionReading(
                composite_risk=0.35, uncertainty=0.50, energy_level=0.40,
                energy_consumption_rate=0.60, recovery_capacity=0.40,
                resource_pursuit=0.70, risk_exposure=0.60, anomaly_flags=1,
            ),
            PreventionReading(
                composite_risk=0.60, uncertainty=0.70, energy_level=0.35,
                energy_consumption_rate=0.65, recovery_capacity=0.40,
                resource_pursuit=0.75, risk_exposure=0.65, anomaly_flags=2,
            ),
        ],
        severity_context=severity_context,
    )
    return assess_prevention(inp)


# --------------------------------------------------------------------------- #
# 품질 가드: 어댑터 번역 정확성 — 전 필드 100% 일치 (값 누락·왜곡 0)
# --------------------------------------------------------------------------- #
def test_adapter_translates_every_field_exactly():
    assessment = _sample_assessment()
    report = to_prevention_report(assessment)

    for field in MIRROR_FIELDS:
        original = getattr(assessment, field)
        copied = getattr(report, field)
        assert _norm(copied) == _norm(original), (
            f"필드 '{field}' 번역 불일치: {original!r} -> {copied!r}"
        )


def test_adapter_preserves_float_scores_bit_for_bit():
    """5개 점수가 소수점까지 정확히 동일한지 (왜곡 0)."""
    assessment = _sample_assessment()
    report = to_prevention_report(assessment)

    assert report.trend_score == assessment.trend_score
    assert report.imbalance_score == assessment.imbalance_score
    assert report.early_warning_score == assessment.early_warning_score
    assert report.recovery_capacity == assessment.recovery_capacity
    assert report.preventive_action_priority == assessment.preventive_action_priority


def test_adapter_preserves_reason_codes_content_and_order():
    assessment = _sample_assessment()
    report = to_prevention_report(assessment)

    assert list(report.reason_codes) == list(assessment.reason_codes)
    assert report.reason_summary == assessment.reason_summary


# --------------------------------------------------------------------------- #
# severity_context 는 echo 만 (값이 바뀌지 않음, 침범 금지)
# --------------------------------------------------------------------------- #
def test_adapter_echoes_severity_context_unchanged():
    assessment = _sample_assessment(severity_context="restrict")
    report = to_prevention_report(assessment)

    assert report.severity_context == "restrict"
    assert report.severity_context == assessment.severity_context


# --------------------------------------------------------------------------- #
# 행동 게이트 금지선 (D4): PreventionReport 에 recommended_action 이 '없음'
# --------------------------------------------------------------------------- #
def test_prevention_report_has_no_action_field():
    assert "recommended_action" not in PreventionReport.model_fields


def test_prevention_report_is_exact_mirror_of_assessment_fields():
    """전체 거울(D3): 필드 집합이 정확히 MIRROR_FIELDS 와 일치(누락·잉여 0)."""
    assert set(PreventionReport.model_fields.keys()) == set(MIRROR_FIELDS)


# --------------------------------------------------------------------------- #
# 비파괴(D7): prevention 미포함 기존 페이로드가 여전히 유효 + schema_version v0.1
# --------------------------------------------------------------------------- #
def test_existing_payload_without_prevention_is_unchanged():
    payload = generate_first_simulation_payload()

    assert payload.schema_version == "hyean.gwan.interface.v0.1"
    assert payload.prevention is None  # 최상위 옵션 자리, default None


# --------------------------------------------------------------------------- #
# 자리(D1): 최상위 옵션 필드가 PreventionReport 를 받아도 기존 5 package 무변경
# --------------------------------------------------------------------------- #
def test_payload_seat_accepts_prevention_report_without_touching_packages():
    payload = generate_first_simulation_payload()
    report = to_prevention_report(_sample_assessment())

    updated = payload.model_copy(update={"prevention": report})

    assert updated.prevention is not None
    assert _norm(updated.prevention.prevention_status) == _norm(report.prevention_status)
    # 기존 5 package 는 그대로
    assert updated.packages == payload.packages
    assert updated.schema_version == "hyean.gwan.interface.v0.1"
