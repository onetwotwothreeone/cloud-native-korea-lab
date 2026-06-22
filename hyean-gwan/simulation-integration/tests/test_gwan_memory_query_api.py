from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_persistence import MemoryJsonlStore
from app.services.gwan_memory_query import MemoryQueryRequest, query_memory_snapshots


def test_query_memory_snapshots_by_object_id() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(object_id="candidate-ice-weak-signal-001"))

    assert response.total_snapshots_scanned == 1
    assert response.total_matches == 1
    assert response.matches[0].object_id == "candidate-ice-weak-signal-001"
    assert response.matches[0].recommended_action == "observe_more"


def test_query_memory_snapshots_by_high_risk() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(min_risk_score=0.75))

    assert response.total_matches == 1
    assert response.matches[0].object_id == "risk-radiation-critical-001"
    assert response.matches[0].alert_level == "critical"


def test_query_memory_snapshots_by_high_uncertainty() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(min_uncertainty_score=0.60))

    assert response.total_matches == 1
    assert response.matches[0].object_id == "candidate-ice-weak-signal-001"
    assert response.matches[0].uncertainty_reason is not None


def test_query_memory_snapshots_by_map_layer() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(map_layer="risk_zones"))

    assert response.total_matches == 1
    assert response.matches[0].object_id == "risk-radiation-critical-001"
    assert response.matches[0].map_layer == "risk_zones"


def test_query_memory_snapshots_by_recommended_action() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(recommended_action="update_survival_map"))

    assert response.total_matches == 1
    assert response.matches[0].object_id == "nav-reference-stable-001"


def test_query_memory_snapshots_respects_limit() -> None:
    snapshot = generate_simulated_memory_snapshot()

    response = query_memory_snapshots([snapshot], MemoryQueryRequest(limit=2))

    assert response.total_matches == 4
    assert len(response.matches) == 2


def test_memory_query_endpoint_returns_empty_when_no_store(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(tmp_path / "missing.jsonl"))
    client = TestClient(app)

    response = client.post("/gwan/memory/query", json={"min_risk_score": 0.75})

    assert response.status_code == 200
    data = response.json()
    assert data["total_snapshots_scanned"] == 0
    assert data["total_matches"] == 0
    assert data["matches"] == []


def test_memory_query_endpoint_finds_persisted_high_risk(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    store = MemoryJsonlStore(memory_path)
    store.append_snapshot(generate_simulated_memory_snapshot())
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    response = client.post("/gwan/memory/query", json={"min_risk_score": 0.75})

    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] == 1
    assert data["matches"][0]["object_id"] == "risk-radiation-critical-001"


def test_memory_query_by_object_endpoint(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    store = MemoryJsonlStore(memory_path)
    store.append_snapshot(generate_simulated_memory_snapshot())
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    response = client.get("/gwan/memory/query/object/candidate-ice-weak-signal-001")

    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] == 1
    assert data["matches"][0]["recommended_action"] == "observe_more"


def test_high_risk_and_high_uncertainty_convenience_endpoints(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    store = MemoryJsonlStore(memory_path)
    store.append_snapshot(generate_simulated_memory_snapshot())
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    risk_response = client.get("/gwan/memory/query/high-risk?min_risk_score=0.75")
    uncertainty_response = client.get("/gwan/memory/query/high-uncertainty?min_uncertainty_score=0.60")

    assert risk_response.status_code == 200
    assert uncertainty_response.status_code == 200
    assert risk_response.json()["matches"][0]["object_id"] == "risk-radiation-critical-001"
    assert uncertainty_response.json()["matches"][0]["object_id"] == "candidate-ice-weak-signal-001"
