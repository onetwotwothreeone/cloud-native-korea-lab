from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.db.session import create_memory_tables
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_persistence import MemoryJsonlStore
from app.services.gwan_memory_sync import (
    MemorySyncRequest,
    get_memory_sync_status,
    sync_jsonl_memory_to_database,
)
from app.services.gwan_memory_postgres_query import query_database_memory_snapshots
from app.services.gwan_memory_query import MemoryQueryRequest


def sqlite_url(tmp_path: Path) -> str:
    return f"sqlite:///{tmp_path / 'sync-test.db'}"


def write_sample_jsonl(path: Path, repeat: int = 1) -> None:
    store = MemoryJsonlStore(path)
    snapshot = generate_simulated_memory_snapshot()
    for _ in range(repeat):
        store.append_snapshot(snapshot)


def test_sync_status_detects_pending_jsonl_snapshot(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)
    create_memory_tables(db_url)

    status = get_memory_sync_status(jsonl_path=str(path), database_url=db_url)

    assert status.jsonl_file_exists is True
    assert status.jsonl_record_count == 1
    assert status.db_snapshot_count == 0
    assert status.pending_snapshot_ids == ["memory-snapshot-sim-001"]
    assert status.already_synced_snapshot_ids == []


def test_sync_jsonl_to_database_inserts_pending_snapshot(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)

    result = sync_jsonl_memory_to_database(MemorySyncRequest(jsonl_path=str(path)), database_url=db_url)

    assert result.jsonl_record_count == 1
    assert result.processed_count == 1
    assert result.inserted_count == 1
    assert result.skipped_count == 0
    assert result.pending_count_after_sync == 0
    assert result.table_counts["memory_snapshots"] == 1
    assert result.table_counts["observation_records"] == 4
    assert result.results[0].inserted is True


def test_sync_is_idempotent_and_skips_existing_snapshot(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)

    first = sync_jsonl_memory_to_database(MemorySyncRequest(jsonl_path=str(path)), database_url=db_url)
    second = sync_jsonl_memory_to_database(MemorySyncRequest(jsonl_path=str(path)), database_url=db_url)

    assert first.inserted_count == 1
    assert second.inserted_count == 0
    assert second.skipped_count == 1
    assert second.results[0].skipped_reason == "already_exists"
    assert second.table_counts["memory_snapshots"] == 1


def test_sync_handles_duplicate_snapshot_ids_inside_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path, repeat=2)

    result = sync_jsonl_memory_to_database(MemorySyncRequest(jsonl_path=str(path)), database_url=db_url)

    assert result.jsonl_record_count == 2
    assert result.processed_count == 2
    assert result.inserted_count == 1
    assert result.skipped_count == 1
    assert [item.inserted for item in result.results] == [True, False]
    assert result.results[1].skipped_reason == "already_exists"


def test_dry_run_reports_pending_without_inserting(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)

    result = sync_jsonl_memory_to_database(
        MemorySyncRequest(jsonl_path=str(path), dry_run=True),
        database_url=db_url,
    )

    assert result.dry_run is True
    assert result.inserted_count == 0
    assert result.skipped_count == 1
    assert result.pending_count_after_sync == 1
    assert result.table_counts["memory_snapshots"] == 0
    assert result.results[0].skipped_reason == "dry_run"


def test_synced_snapshot_can_be_queried_from_database(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)
    sync_jsonl_memory_to_database(MemorySyncRequest(jsonl_path=str(path)), database_url=db_url)

    response = query_database_memory_snapshots(
        MemoryQueryRequest(recommended_action="send_micro_probe"),
        database_url=db_url,
    )

    assert response.total_matches == 1
    assert response.matches[0].object_id == "candidate-resource-stable-001"


def test_sync_api_status_and_sync_with_env_paths(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "memory.jsonl"
    db_url = sqlite_url(tmp_path)
    write_sample_jsonl(path)
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(path))
    monkeypatch.setenv("DATABASE_URL", db_url)

    client = TestClient(app)

    status_response = client.get("/gwan/memory/sync-status")
    assert status_response.status_code == 200
    assert status_response.json()["pending_snapshot_ids"] == ["memory-snapshot-sim-001"]

    sync_response = client.post("/gwan/memory/sync-jsonl-to-db", json={})
    assert sync_response.status_code == 200
    sync_body = sync_response.json()
    assert sync_body["inserted_count"] == 1
    assert sync_body["pending_count_after_sync"] == 0

    query_response = client.get("/gwan/memory/db-query/action/send_micro_probe")
    assert query_response.status_code == 200
    assert query_response.json()["matches"][0]["object_id"] == "candidate-resource-stable-001"
