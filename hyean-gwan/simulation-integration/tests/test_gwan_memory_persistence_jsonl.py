from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_persistence import MemoryJsonlStore


def test_jsonl_store_appends_and_reads_snapshot(tmp_path: Path) -> None:
    store = MemoryJsonlStore(tmp_path / "memory.jsonl")
    snapshot = generate_simulated_memory_snapshot()

    result = store.append_snapshot(snapshot)
    loaded = store.list_snapshots()

    assert result.snapshot_id == snapshot.snapshot_id
    assert result.line_number == 1
    assert result.record_count == 1
    assert len(loaded) == 1
    assert loaded[0].snapshot_id == snapshot.snapshot_id


def test_jsonl_store_one_snapshot_per_line(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    store = MemoryJsonlStore(path)

    store.append_snapshot(generate_simulated_memory_snapshot())
    store.append_snapshot(generate_simulated_memory_snapshot())

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert store.count_snapshots() == 2


def test_jsonl_store_status_tracks_latest_snapshot(tmp_path: Path) -> None:
    store = MemoryJsonlStore(tmp_path / "memory.jsonl")
    snapshot = generate_simulated_memory_snapshot()

    assert store.status().file_exists is False
    store.append_snapshot(snapshot)
    status = store.status()

    assert status.file_exists is True
    assert status.record_count == 1
    assert status.latest_snapshot_id == snapshot.snapshot_id


def test_jsonl_store_get_snapshot_by_id(tmp_path: Path) -> None:
    store = MemoryJsonlStore(tmp_path / "memory.jsonl")
    snapshot = generate_simulated_memory_snapshot()
    store.append_snapshot(snapshot)

    found = store.get_snapshot(snapshot.snapshot_id)
    missing = store.get_snapshot("missing-snapshot")

    assert found is not None
    assert found.snapshot_id == snapshot.snapshot_id
    assert missing is None


def test_persist_simulated_snapshot_endpoint_writes_jsonl(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    response = client.post("/gwan/memory/persist-simulated-snapshot")

    assert response.status_code == 200
    data = response.json()
    assert data["snapshot_id"] == "memory-snapshot-sim-001"
    assert data["record_count"] == 1
    assert memory_path.exists()


def test_persisted_snapshots_endpoint_reads_jsonl(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    client.post("/gwan/memory/persist-simulated-snapshot")
    response = client.get("/gwan/memory/persisted-snapshots")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["snapshot_id"] == "memory-snapshot-sim-001"
    assert "observations" in data[0]
    assert "map_updates" in data[0]


def test_persistence_status_endpoint(tmp_path: Path, monkeypatch) -> None:
    memory_path = tmp_path / "api-memory.jsonl"
    monkeypatch.setenv("HYEAN_MEMORY_JSONL_PATH", str(memory_path))
    client = TestClient(app)

    empty = client.get("/gwan/memory/persistence-status").json()
    assert empty["record_count"] == 0
    assert empty["file_exists"] is False

    client.post("/gwan/memory/persist-simulated-snapshot")
    status = client.get("/gwan/memory/persistence-status").json()

    assert status["record_count"] == 1
    assert status["file_exists"] is True
    assert status["latest_snapshot_id"] == "memory-snapshot-sim-001"
