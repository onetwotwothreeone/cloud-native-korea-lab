from pathlib import Path

from fastapi.testclient import TestClient

from app.db.session import create_memory_tables
from app.main import app
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_postgres_persistence import persist_memory_snapshot_to_database
from app.services.gwan_memory_postgres_query import query_database_memory_snapshots, query_database_object_history
from app.services.gwan_memory_query import MemoryQueryRequest


def sqlite_url(tmp_path: Path) -> str:
    return f"sqlite+pysqlite:///{tmp_path / 'gwan_memory_query_test.db'}"


def seed_database(tmp_path: Path) -> str:
    url = sqlite_url(tmp_path)
    create_memory_tables(url)
    persist_memory_snapshot_to_database(generate_simulated_memory_snapshot(), database_url=url)
    return url


def test_database_memory_query_returns_all_object_matches(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_memory_snapshots(database_url=url)

    assert result.total_snapshots_scanned == 1
    assert result.total_matches == 4
    assert {match.object_id for match in result.matches} == {
        "candidate-resource-stable-001",
        "risk-radiation-critical-001",
        "candidate-ice-weak-signal-001",
        "nav-reference-stable-001",
    }


def test_database_high_risk_query_finds_radiation_zone(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_memory_snapshots(MemoryQueryRequest(min_risk_score=0.75), database_url=url)

    assert result.total_matches == 1
    match = result.matches[0]
    assert match.object_id == "risk-radiation-critical-001"
    assert match.recommended_action == "avoid"
    assert match.map_layer == "risk_zones"


def test_database_high_uncertainty_query_finds_weak_signal_candidate(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_memory_snapshots(MemoryQueryRequest(min_uncertainty_score=0.60), database_url=url)

    assert result.total_matches == 1
    match = result.matches[0]
    assert match.object_id == "candidate-ice-weak-signal-001"
    assert match.recommended_action == "observe_more"
    assert "too weak for confirmation" in match.uncertainty_reason


def test_database_object_history_query(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_object_history("candidate-resource-stable-001", database_url=url)

    assert result.total_matches == 1
    assert result.matches[0].recommended_action == "send_micro_probe"
    assert result.matches[0].display_category == "resource_candidate"


def test_database_recommended_action_filter(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_memory_snapshots(MemoryQueryRequest(recommended_action="update_survival_map"), database_url=url)

    assert result.total_matches == 1
    assert result.matches[0].object_id == "nav-reference-stable-001"


def test_database_query_respects_limit(tmp_path):
    url = seed_database(tmp_path)

    result = query_database_memory_snapshots(MemoryQueryRequest(limit=2), database_url=url)

    assert len(result.matches) == 2
    assert result.total_matches == 2


def test_database_query_api_routes_with_sqlite(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", sqlite_url(tmp_path))
    client = TestClient(app)

    create_response = client.post("/gwan/memory/db-create-tables")
    assert create_response.status_code == 200

    persist_response = client.post("/gwan/memory/db-persist-simulated-snapshot")
    assert persist_response.status_code == 200
    assert persist_response.json()["inserted"] is True

    high_risk_response = client.get("/gwan/memory/db-query/high-risk")
    assert high_risk_response.status_code == 200
    assert high_risk_response.json()["matches"][0]["object_id"] == "risk-radiation-critical-001"

    object_response = client.get("/gwan/memory/db-query/object/candidate-ice-weak-signal-001")
    assert object_response.status_code == 200
    assert object_response.json()["matches"][0]["recommended_action"] == "observe_more"

    action_response = client.get("/gwan/memory/db-query/action/send_micro_probe")
    assert action_response.status_code == 200
    assert action_response.json()["matches"][0]["object_id"] == "candidate-resource-stable-001"
