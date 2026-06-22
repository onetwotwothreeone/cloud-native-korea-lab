from fastapi.testclient import TestClient

from app.main import app
from app.schemas.gwan_interface import RecommendedAction
from app.services.gwan_memory import create_memory_snapshot_from_integrated_result, generate_simulated_memory_snapshot
from app.services.gwan_simulation import generate_integrated_simulation_result


def test_memory_snapshot_preserves_all_integrated_simulation_objects() -> None:
    result = generate_integrated_simulation_result()
    snapshot = create_memory_snapshot_from_integrated_result(result)

    assert snapshot.object_count() == len(result.object_decisions)
    assert len(snapshot.observations) == len(result.object_decisions)
    assert len(snapshot.scores) == len(result.object_decisions)
    assert len(snapshot.decisions) == len(result.object_decisions)
    assert len(snapshot.map_updates) == len(result.object_decisions)


def test_memory_snapshot_keeps_recommended_actions() -> None:
    snapshot = generate_simulated_memory_snapshot()
    actions = {decision.object_id: decision.recommended_action for decision in snapshot.decisions}

    assert actions["candidate-resource-stable-001"] == RecommendedAction.SEND_MICRO_PROBE
    assert actions["risk-radiation-critical-001"] == RecommendedAction.AVOID
    assert actions["candidate-ice-weak-signal-001"] == RecommendedAction.OBSERVE_MORE
    assert actions["nav-reference-stable-001"] == RecommendedAction.UPDATE_SURVIVAL_MAP


def test_memory_snapshot_creates_expected_map_layers() -> None:
    snapshot = generate_simulated_memory_snapshot()

    assert "resource_candidates" in snapshot.map_layers()
    assert "risk_zones" in snapshot.map_layers()
    assert "navigation_references" in snapshot.map_layers()
    assert snapshot.high_risk_count() == 1


def test_memory_snapshot_preserves_uncertainty_reason() -> None:
    snapshot = generate_simulated_memory_snapshot()

    weak_signal = next(item for item in snapshot.uncertainties if item.object_id == "candidate-ice-weak-signal-001")
    assert weak_signal.uncertainty_type == "weak_signal"
    assert "too weak" in weak_signal.uncertainty_reason
    assert "repeat spectral observation" in weak_signal.suggested_resolution.lower()


def test_simulated_memory_snapshot_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/gwan/memory/simulated-snapshot")

    assert response.status_code == 200
    data = response.json()
    assert data["snapshot_id"] == "memory-snapshot-sim-001"
    assert len(data["observations"]) == 4
    assert len(data["map_updates"]) == 4


def test_memory_snapshot_endpoint_accepts_integrated_result() -> None:
    client = TestClient(app)
    result = generate_integrated_simulation_result()

    response = client.post("/gwan/memory/snapshot", json=result.model_dump(mode="json"))

    assert response.status_code == 200
    data = response.json()
    assert data["mission_id"] == "sim-001"
    assert len(data["decisions"]) == len(result.object_decisions)
