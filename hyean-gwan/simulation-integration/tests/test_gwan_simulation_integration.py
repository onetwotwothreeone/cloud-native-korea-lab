from fastapi.testclient import TestClient

from app.main import app
from app.schemas.gwan_interface import RecommendedAction
from app.services.gwan_scoring import recommend_action
from app.services.gwan_simulation import (
    default_simulated_objects,
    generate_first_simulation_payload,
    generate_integrated_simulation_result,
)


def test_integrated_simulation_generates_valid_interface_payload() -> None:
    result = generate_integrated_simulation_result()
    payload = result.payload

    assert payload.schema_version == "hyean.gwan.interface.v0.1"
    assert len(result.object_decisions) == 4
    assert len(payload.packages.spatial_visualization_package.objects) == 4
    assert payload.packages.sidebar_intelligence_package is not None
    assert payload.packages.alert_feed_package is not None
    assert payload.packages.uncertainty_package is not None
    assert payload.packages.decision_report_package is not None


def test_simulation_uses_shared_scoring_rule_for_each_object() -> None:
    result = generate_integrated_simulation_result()

    for pair in result.object_decisions:
        expected = recommend_action(pair.simulated_object.to_scoring_case())
        assert pair.decision.recommended_action == expected.recommended_action
        assert pair.decision.scores == expected.scores
        assert pair.decision.alert_level == expected.alert_level


def test_spatial_recommended_actions_are_generated_from_scoring_decisions() -> None:
    result = generate_integrated_simulation_result()
    objects = {item.object_id: item for item in result.payload.packages.spatial_visualization_package.objects}

    assert objects["candidate-resource-stable-001"].recommended_action == RecommendedAction.SEND_MICRO_PROBE
    assert objects["risk-radiation-critical-001"].recommended_action == RecommendedAction.AVOID
    assert objects["candidate-ice-weak-signal-001"].recommended_action == RecommendedAction.OBSERVE_MORE
    assert objects["nav-reference-stable-001"].recommended_action == RecommendedAction.UPDATE_SURVIVAL_MAP


def test_integrated_payload_contains_uncertainty_record_for_weak_signal_object() -> None:
    payload = generate_first_simulation_payload()
    records = payload.packages.uncertainty_package.items

    weak_signal = next(item for item in records if item.object_id == "candidate-ice-weak-signal-001")
    assert weak_signal.uncertainty_type == "weak_signal"
    assert "too weak" in weak_signal.uncertainty_reason


def test_integrated_payload_alerts_include_risk_and_uncertainty() -> None:
    payload = generate_first_simulation_payload()
    alerts = payload.packages.alert_feed_package.alerts
    categories = {alert.category for alert in alerts}
    severities = {alert.severity for alert in alerts}

    assert "risk" in categories
    assert "uncertainty" in categories
    assert "critical" in severities
    assert "medium" in severities


def test_sidebar_selects_strongest_non_risk_candidate() -> None:
    payload = generate_first_simulation_payload()
    sidebar = payload.packages.sidebar_intelligence_package

    assert sidebar.selected_object_id == "candidate-resource-stable-001"
    assert sidebar.recommended_action == RecommendedAction.SEND_MICRO_PROBE
    assert sidebar.scores.resource_score >= 0.80


def test_integrated_simulation_endpoint_returns_payload() -> None:
    client = TestClient(app)
    response = client.post(
        "/gwan/simulate",
        json={
            "mission_id": "sim-custom-001",
            "operator_intent": "regional_resource_scan",
            "mission_phase": "regional_scan",
            "priority_context": "prefer low-risk resource candidates",
            "observer": "onboard_gwan_core",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["mission_context"]["mission_id"] == "sim-custom-001"
    assert data["packages"]["sidebar_intelligence_package"]["recommended_action"] == "send_micro_probe"


def test_integrated_review_endpoint_returns_payload_and_decisions() -> None:
    client = TestClient(app)
    response = client.post("/gwan/simulate-integrated", json={})

    assert response.status_code == 200
    data = response.json()
    assert "payload" in data
    assert "object_decisions" in data
    assert len(data["object_decisions"]) == len(default_simulated_objects())
