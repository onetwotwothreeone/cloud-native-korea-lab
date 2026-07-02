"""H4 중간 연결(Mid-Connection) 검증 테스트 (TDD: 구현 전 red).

근거: docs/H4_INTEGRATION_SPEC.md 부록(중간 연결) M4.
검증 대상 — 새 래퍼 generate_simulation_with_prevention(prevention_input, request=None):
  1. 진짜 PreventionInput 주입 시 payload.prevention 이 실제로 채워짐
  2. 채워진 값이 assess_prevention 결과와 100% 일치 (품질 가드)
  3. 채워진 뒤에도 기존 5 package 무변경 (비파괴)
  4. 채워진 페이로드가 계약 규약(ContractBaseModel) 위반 없음 (품질 가드)
  5. prevention_input 미주입 기존 빌더 경로는 여전히 prevention=None (경계)

구현(generate_simulation_with_prevention)이 아직 없으므로 import 단계에서 red 가 정상이다.
"""

from app.schemas.gwan_interface import GWANInterfacePayload, PreventionReport
from app.services.gwan_simulation import (
    generate_first_simulation_payload,
    generate_integrated_simulation_result,
    generate_simulation_with_prevention,  # 아직 없음 → ImportError(red)
)
from app.services.prevention import assess_prevention
from app.services.prevention.contract_adapter import to_prevention_report
from app.services.prevention.models import PreventionInput, PreventionReading


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
    if isinstance(value, list):
        return [getattr(item, "value", item) for item in value]
    return getattr(value, "value", value)


def _sample_prevention_input() -> PreventionInput:
    """비자명한 값이 나오는 거주체 흐름 입력(호출자 명시 제공, 길 A)."""
    return PreventionInput(
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
        severity_context="restrict",
    )


def _packages_fingerprint(payload: GWANInterfacePayload) -> dict:
    """package 비교용 지문. 유일한 시간 필드(alert created_at)를 제거해 결정적으로 만든다."""
    data = payload.packages.model_dump(mode="json")
    alert_pkg = data.get("alert_feed_package") or {}
    for alert in alert_pkg.get("alerts", []):
        alert.pop("created_at", None)
    return data


# --------------------------------------------------------------------------- #
# 1. 진짜 PreventionInput 주입 시 payload.prevention 이 실제로 채워짐
# --------------------------------------------------------------------------- #
def test_prevention_input_populates_payload_prevention():
    result = generate_simulation_with_prevention(_sample_prevention_input())

    assert result.payload.prevention is not None
    assert isinstance(result.payload.prevention, PreventionReport)


# --------------------------------------------------------------------------- #
# 2. 채워진 값이 assess_prevention 결과와 100% 일치 (품질 가드)
# --------------------------------------------------------------------------- #
def test_populated_prevention_matches_assessment_exactly():
    prevention_input = _sample_prevention_input()
    result = generate_simulation_with_prevention(prevention_input)

    expected = to_prevention_report(assess_prevention(prevention_input))
    got = result.payload.prevention

    for field in MIRROR_FIELDS:
        assert _norm(getattr(got, field)) == _norm(getattr(expected, field)), (
            f"필드 '{field}' 불일치: {getattr(expected, field)!r} -> {getattr(got, field)!r}"
        )


# --------------------------------------------------------------------------- #
# 3. 채워진 뒤에도 기존 5 package 무변경 (비파괴)
# --------------------------------------------------------------------------- #
def test_prevention_populate_does_not_alter_packages_or_decisions():
    baseline = generate_integrated_simulation_result()
    enriched = generate_simulation_with_prevention(_sample_prevention_input())

    # object_decisions 는 타임스탬프가 없어 결정적으로 동일해야 함
    assert enriched.object_decisions == baseline.object_decisions
    # 5 package 도 동일(유일한 시간 필드 제외)
    assert _packages_fingerprint(enriched.payload) == _packages_fingerprint(baseline.payload)


# --------------------------------------------------------------------------- #
# 4. 채워진 페이로드가 계약 규약(ContractBaseModel) 위반 없음 (품질 가드)
# --------------------------------------------------------------------------- #
def test_enriched_payload_still_satisfies_contract():
    result = generate_simulation_with_prevention(_sample_prevention_input())

    # 라운드트립 재검증: extra=forbid, cross-package validator 등 계약 규약 전부 통과해야 함
    dumped = result.payload.model_dump(mode="json")
    revalidated = GWANInterfacePayload.model_validate(dumped)

    assert revalidated.prevention is not None
    assert revalidated.schema_version == "hyean.gwan.interface.v0.1"


# --------------------------------------------------------------------------- #
# 5. prevention_input 미주입 기존 경로는 여전히 prevention=None (경계)
# --------------------------------------------------------------------------- #
def test_existing_builder_paths_still_have_no_prevention():
    result = generate_integrated_simulation_result()
    payload = generate_first_simulation_payload()

    assert result.payload.prevention is None
    assert payload.prevention is None
