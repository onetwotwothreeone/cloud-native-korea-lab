"""Sync GWAN local JSONL memory logs into PostgreSQL.

17_GWAN_Local_Log_To_PostgreSQL_Sync

The previous steps proved two separate memory paths:
- JSONL local log for offline / onboard-first persistence
- PostgreSQL database for searchable long-term memory

This module connects them. It reads MemorySnapshot records from the local JSONL
log and inserts only snapshots that do not already exist in the database.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import Field
from sqlalchemy import select, func

from app.db.gwan_memory_models import (
    DecisionRecordORM,
    MapUpdateRecordORM,
    MemorySnapshotORM,
    ObservationRecordORM,
    ScoreRecordORM,
    UncertaintyRecordORM,
)
from app.db.session import (
    create_database_engine,
    create_memory_tables,
    get_database_url,
    make_safe_database_url,
    session_scope,
)
from app.schemas.gwan_interface import ContractBaseModel
from app.services.gwan_memory_persistence import MemoryJsonlStore, default_memory_store
from app.services.gwan_memory_postgres_persistence import persist_memory_snapshot_to_database


class MemorySyncRequest(ContractBaseModel):
    """Request for syncing local JSONL snapshots to the configured database."""

    jsonl_path: str | None = None
    dry_run: bool = False
    limit: int | None = Field(default=None, ge=1, le=1000)


class MemorySyncSnapshotResult(ContractBaseModel):
    """Per-snapshot sync result."""

    snapshot_id: str
    line_number: int = Field(..., ge=1)
    inserted: bool
    skipped_reason: str | None = None
    message: str


class MemorySyncResult(ContractBaseModel):
    """Result returned after JSONL -> database sync."""

    source_path: str
    database_url_safe: str
    dry_run: bool
    jsonl_record_count: int = Field(..., ge=0)
    processed_count: int = Field(..., ge=0)
    inserted_count: int = Field(..., ge=0)
    skipped_count: int = Field(..., ge=0)
    pending_count_after_sync: int = Field(..., ge=0)
    table_counts: dict[str, int]
    results: list[MemorySyncSnapshotResult]
    synced_at: datetime


class MemorySyncStatus(ContractBaseModel):
    """Comparison between local JSONL memory and database memory."""

    source_path: str
    database_url_safe: str
    jsonl_file_exists: bool
    jsonl_record_count: int = Field(..., ge=0)
    db_snapshot_count: int = Field(..., ge=0)
    pending_snapshot_ids: list[str]
    already_synced_snapshot_ids: list[str]
    checked_at: datetime


def _jsonl_store(path: str | None = None) -> MemoryJsonlStore:
    if path:
        return MemoryJsonlStore(path)
    return default_memory_store()


def _count_tables(database_url: str | None = None) -> dict[str, int]:
    engine = create_database_engine(database_url)
    with session_scope(engine) as session:
        return {
            "memory_snapshots": session.scalar(select(func.count()).select_from(MemorySnapshotORM)) or 0,
            "observation_records": session.scalar(select(func.count()).select_from(ObservationRecordORM)) or 0,
            "score_records": session.scalar(select(func.count()).select_from(ScoreRecordORM)) or 0,
            "decision_records": session.scalar(select(func.count()).select_from(DecisionRecordORM)) or 0,
            "uncertainty_records": session.scalar(select(func.count()).select_from(UncertaintyRecordORM)) or 0,
            "map_update_records": session.scalar(select(func.count()).select_from(MapUpdateRecordORM)) or 0,
        }


def _database_snapshot_ids(database_url: str | None = None) -> set[str]:
    engine = create_database_engine(database_url)
    with session_scope(engine) as session:
        return set(session.scalars(select(MemorySnapshotORM.snapshot_id)).all())


def get_memory_sync_status(
    *,
    jsonl_path: str | None = None,
    database_url: str | None = None,
) -> MemorySyncStatus:
    """Return local-vs-database memory sync status."""

    url = database_url or get_database_url()
    create_memory_tables(url)

    store = _jsonl_store(jsonl_path)
    snapshots = store.list_snapshots()
    db_ids = _database_snapshot_ids(url)
    jsonl_ids = [snapshot.snapshot_id for snapshot in snapshots]

    pending_ids: list[str] = []
    already_synced_ids: list[str] = []
    seen_pending: set[str] = set()
    seen_synced: set[str] = set()

    for snapshot_id in jsonl_ids:
        if snapshot_id in db_ids:
            if snapshot_id not in seen_synced:
                already_synced_ids.append(snapshot_id)
                seen_synced.add(snapshot_id)
        else:
            if snapshot_id not in seen_pending:
                pending_ids.append(snapshot_id)
                seen_pending.add(snapshot_id)

    return MemorySyncStatus(
        source_path=str(store.path),
        database_url_safe=make_safe_database_url(url),
        jsonl_file_exists=Path(store.path).exists(),
        jsonl_record_count=len(snapshots),
        db_snapshot_count=len(db_ids),
        pending_snapshot_ids=pending_ids,
        already_synced_snapshot_ids=already_synced_ids,
        checked_at=datetime.now(UTC),
    )


def sync_jsonl_memory_to_database(
    request: MemorySyncRequest | None = None,
    *,
    database_url: str | None = None,
) -> MemorySyncResult:
    """Sync JSONL MemorySnapshot records into database tables.

    Rules:
    - Only snapshots not already present in the database are inserted.
    - Duplicate snapshot IDs in JSONL are skipped after the first successful insert.
    - dry_run reports what would happen without inserting rows.
    """

    request = request or MemorySyncRequest()
    url = database_url or get_database_url()
    create_memory_tables(url)

    store = _jsonl_store(request.jsonl_path)
    snapshots = store.list_snapshots()
    selected_snapshots = snapshots[: request.limit] if request.limit else snapshots

    db_ids = _database_snapshot_ids(url)
    results: list[MemorySyncSnapshotResult] = []
    inserted_count = 0
    skipped_count = 0

    for index, snapshot in enumerate(selected_snapshots, start=1):
        if snapshot.snapshot_id in db_ids:
            skipped_count += 1
            results.append(
                MemorySyncSnapshotResult(
                    snapshot_id=snapshot.snapshot_id,
                    line_number=index,
                    inserted=False,
                    skipped_reason="already_exists",
                    message="Snapshot already exists in database. Skipped.",
                )
            )
            continue

        if request.dry_run:
            skipped_count += 1
            results.append(
                MemorySyncSnapshotResult(
                    snapshot_id=snapshot.snapshot_id,
                    line_number=index,
                    inserted=False,
                    skipped_reason="dry_run",
                    message="Dry run only. Snapshot would be inserted.",
                )
            )
            continue

        persist_result = persist_memory_snapshot_to_database(snapshot, database_url=url)
        if persist_result.inserted:
            inserted_count += 1
            db_ids.add(snapshot.snapshot_id)
            results.append(
                MemorySyncSnapshotResult(
                    snapshot_id=snapshot.snapshot_id,
                    line_number=index,
                    inserted=True,
                    message="Snapshot inserted into database.",
                )
            )
        else:
            skipped_count += 1
            db_ids.add(snapshot.snapshot_id)
            results.append(
                MemorySyncSnapshotResult(
                    snapshot_id=snapshot.snapshot_id,
                    line_number=index,
                    inserted=False,
                    skipped_reason="already_exists",
                    message=persist_result.message,
                )
            )

    status_after = get_memory_sync_status(jsonl_path=request.jsonl_path, database_url=url)
    return MemorySyncResult(
        source_path=str(store.path),
        database_url_safe=make_safe_database_url(url),
        dry_run=request.dry_run,
        jsonl_record_count=len(snapshots),
        processed_count=len(selected_snapshots),
        inserted_count=inserted_count,
        skipped_count=skipped_count,
        pending_count_after_sync=len(status_after.pending_snapshot_ids),
        table_counts=_count_tables(url),
        results=results,
        synced_at=datetime.now(UTC),
    )
