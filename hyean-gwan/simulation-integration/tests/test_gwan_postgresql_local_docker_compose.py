from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.db.gwan_memory_models import Base
from app.db.session import (
    create_database_engine,
    create_memory_tables,
    get_database_status,
    make_safe_database_url,
)
from app.main import app
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_postgres_persistence import (
    list_database_memory_snapshots,
    persist_memory_snapshot_to_database,
)

EXPECTED_TABLES = {
    "memory_snapshots",
    "observation_records",
    "score_records",
    "decision_records",
    "uncertainty_records",
    "map_update_records",
}


def sqlite_url(tmp_path: Path) -> str:
    return f"sqlite+pysqlite:///{tmp_path / 'gwan_memory_test.db'}"


def test_docker_compose_file_exists_and_contains_postgres_service():
    content = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "postgres:16-alpine" in content
    assert "55432:5432" in content
    assert "hyean_gwan" in content


def test_env_example_contains_database_url():
    content = Path(".env.example").read_text(encoding="utf-8")

    assert "DATABASE_URL=postgresql+psycopg://" in content
    assert "POSTGRES_USER=hyean" in content


def test_safe_database_url_hides_password():
    safe = make_safe_database_url("postgresql+psycopg://hyean:secret@localhost:55432/hyean_gwan")

    assert "secret" not in safe
    assert "***" in safe


def test_create_memory_tables_with_sqlite_for_structure(tmp_path):
    url = sqlite_url(tmp_path)
    result = create_memory_tables(url)

    assert result.created is True
    assert set(result.table_names) == EXPECTED_TABLES


def test_database_status_reports_tables_created_with_sqlite(tmp_path):
    url = sqlite_url(tmp_path)
    create_memory_tables(url)
    status = get_database_status(url)

    assert status.connected is True
    assert status.tables_created is True
    assert set(status.table_names) == EXPECTED_TABLES


def test_persist_memory_snapshot_to_database_with_sqlite(tmp_path):
    url = sqlite_url(tmp_path)
    snapshot = generate_simulated_memory_snapshot()

    result = persist_memory_snapshot_to_database(snapshot, database_url=url)

    assert result.inserted is True
    assert result.snapshot_id == "memory-snapshot-sim-001"
    assert result.table_counts["memory_snapshots"] == 1
    assert result.table_counts["observation_records"] == len(snapshot.observations)
    assert result.table_counts["map_update_records"] == len(snapshot.map_updates)


def test_duplicate_snapshot_insert_is_safe_noop(tmp_path):
    url = sqlite_url(tmp_path)
    snapshot = generate_simulated_memory_snapshot()

    first = persist_memory_snapshot_to_database(snapshot, database_url=url)
    second = persist_memory_snapshot_to_database(snapshot, database_url=url)

    assert first.inserted is True
    assert second.inserted is False
    assert second.table_counts["memory_snapshots"] == 1


def test_list_database_memory_snapshots(tmp_path):
    url = sqlite_url(tmp_path)
    persist_memory_snapshot_to_database(generate_simulated_memory_snapshot(), database_url=url)

    result = list_database_memory_snapshots(database_url=url)

    assert result.count == 1
    assert result.snapshots[0].snapshot_id == "memory-snapshot-sim-001"
    assert result.snapshots[0].observation_count == 4


def test_api_database_routes_with_sqlite(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", sqlite_url(tmp_path))
    client = TestClient(app)

    create_response = client.post("/gwan/memory/db-create-tables")
    assert create_response.status_code == 200
    assert set(create_response.json()["table_names"]) == EXPECTED_TABLES

    status_response = client.get("/gwan/memory/db-status")
    assert status_response.status_code == 200
    assert status_response.json()["tables_created"] is True

    persist_response = client.post("/gwan/memory/db-persist-simulated-snapshot")
    assert persist_response.status_code == 200
    assert persist_response.json()["inserted"] is True

    list_response = client.get("/gwan/memory/db-snapshots")
    assert list_response.status_code == 200
    assert list_response.json()["count"] == 1
