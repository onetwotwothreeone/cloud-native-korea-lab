"""JSONL persistence for GWAN memory snapshots.

11_GWAN_Memory_Persistence_JSONL

The previous step created MemorySnapshot objects in memory. This module makes
those snapshots durable by appending each snapshot as one JSON line.

Why JSONL first?
- simple to inspect
- append-friendly
- easy to test
- easy to migrate to PostgreSQL later
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

from pydantic import Field

from app.schemas.gwan_interface import ContractBaseModel
from app.services.gwan_memory import MemorySnapshot, generate_simulated_memory_snapshot


DEFAULT_MEMORY_JSONL_PATH = Path("data/gwan_memory_snapshots.jsonl")


class MemoryPersistenceResult(ContractBaseModel):
    """Result returned after a memory snapshot is written to JSONL."""

    snapshot_id: str
    path: str
    line_number: int = Field(..., ge=1)
    record_count: int = Field(..., ge=1)
    persisted_at: datetime


class MemoryPersistenceStatus(ContractBaseModel):
    """Current status of the JSONL memory store."""

    path: str
    file_exists: bool
    record_count: int = Field(..., ge=0)
    latest_snapshot_id: str | None = None


class MemoryJsonlStore:
    """Tiny append-only JSONL store for MemorySnapshot records."""

    def __init__(self, path: str | Path = DEFAULT_MEMORY_JSONL_PATH) -> None:
        self.path = Path(path)

    def ensure_parent(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append_snapshot(self, snapshot: MemorySnapshot) -> MemoryPersistenceResult:
        """Append one MemorySnapshot as one JSON line."""

        self.ensure_parent()
        existing_count = self.count_snapshots()
        with self.path.open("a", encoding="utf-8") as file:
            file.write(snapshot.model_dump_json())
            file.write("\n")

        return MemoryPersistenceResult(
            snapshot_id=snapshot.snapshot_id,
            path=str(self.path),
            line_number=existing_count + 1,
            record_count=existing_count + 1,
            persisted_at=datetime.now(UTC),
        )

    def list_snapshots(self) -> list[MemorySnapshot]:
        """Load all snapshots from the JSONL file."""

        if not self.path.exists():
            return []

        snapshots: list[MemorySnapshot] = []
        with self.path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    snapshots.append(MemorySnapshot.model_validate_json(line))
                except Exception as exc:  # pragma: no cover - keeps error message clear in manual use
                    raise ValueError(f"Invalid MemorySnapshot JSONL record at line {line_number}: {exc}") from exc
        return snapshots

    def count_snapshots(self) -> int:
        return len(self.list_snapshots())

    def latest_snapshot(self) -> MemorySnapshot | None:
        snapshots = self.list_snapshots()
        if not snapshots:
            return None
        return snapshots[-1]

    def get_snapshot(self, snapshot_id: str) -> MemorySnapshot | None:
        for snapshot in self.list_snapshots():
            if snapshot.snapshot_id == snapshot_id:
                return snapshot
        return None

    def status(self) -> MemoryPersistenceStatus:
        latest = self.latest_snapshot()
        return MemoryPersistenceStatus(
            path=str(self.path),
            file_exists=self.path.exists(),
            record_count=self.count_snapshots(),
            latest_snapshot_id=latest.snapshot_id if latest else None,
        )


def default_memory_store() -> MemoryJsonlStore:
    """Create the default store.

    Tests and local experiments can override the path with:

    HYEAN_MEMORY_JSONL_PATH=/tmp/my-memory.jsonl
    """

    path = os.getenv("HYEAN_MEMORY_JSONL_PATH")
    return MemoryJsonlStore(path or DEFAULT_MEMORY_JSONL_PATH)


def persist_memory_snapshot(snapshot: MemorySnapshot) -> MemoryPersistenceResult:
    """Persist a provided MemorySnapshot using the default JSONL store."""

    return default_memory_store().append_snapshot(snapshot)


def persist_simulated_memory_snapshot() -> MemoryPersistenceResult:
    """Generate the default simulated MemorySnapshot and persist it."""

    snapshot = generate_simulated_memory_snapshot()
    return persist_memory_snapshot(snapshot)


def list_persisted_memory_snapshots() -> list[MemorySnapshot]:
    """Return all persisted snapshots from the default JSONL store."""

    return default_memory_store().list_snapshots()


def get_memory_persistence_status() -> MemoryPersistenceStatus:
    """Return current JSONL store status."""

    return default_memory_store().status()
