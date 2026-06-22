"""Persist GWAN MemorySnapshot records into SQLAlchemy/PostgreSQL tables.

This is the first real database persistence layer. It keeps JSONL support in
place, but adds a path for local PostgreSQL through Docker Compose.
"""

from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.engine import Engine

from app.db.gwan_memory_models import (
    DecisionRecordORM,
    MapUpdateRecordORM,
    MemorySnapshotORM,
    ObservationRecordORM,
    ScoreRecordORM,
    UncertaintyRecordORM,
)
from app.db.session import create_database_engine, session_scope
from app.schemas.gwan_interface import ContractBaseModel
from app.services.gwan_memory import MemorySnapshot, generate_simulated_memory_snapshot
from app.services.gwan_memory_postgres_design import memory_snapshot_to_insert_plan


class MemoryPostgresPersistenceResult(ContractBaseModel):
    snapshot_id: str
    inserted: bool
    database_url_safe: str
    table_counts: dict[str, int]
    message: str


class MemoryPostgresSnapshotSummary(ContractBaseModel):
    snapshot_id: str
    mission_id: str
    generated_at: str
    observation_count: int
    score_count: int
    decision_count: int
    uncertainty_count: int
    map_update_count: int


class MemoryPostgresSnapshotList(ContractBaseModel):
    snapshots: list[MemoryPostgresSnapshotSummary]
    count: int


def _count_tables(engine: Engine) -> dict[str, int]:
    with session_scope(engine) as session:
        return {
            "memory_snapshots": session.scalar(select(func.count()).select_from(MemorySnapshotORM)) or 0,
            "observation_records": session.scalar(select(func.count()).select_from(ObservationRecordORM)) or 0,
            "score_records": session.scalar(select(func.count()).select_from(ScoreRecordORM)) or 0,
            "decision_records": session.scalar(select(func.count()).select_from(DecisionRecordORM)) or 0,
            "uncertainty_records": session.scalar(select(func.count()).select_from(UncertaintyRecordORM)) or 0,
            "map_update_records": session.scalar(select(func.count()).select_from(MapUpdateRecordORM)) or 0,
        }


def persist_memory_snapshot_to_database(
    snapshot: MemorySnapshot,
    *,
    database_url: str | None = None,
) -> MemoryPostgresPersistenceResult:
    """Persist one MemorySnapshot into database tables.

    Re-running the same simulated snapshot is treated as a safe no-op instead
    of raising a duplicate primary-key error.
    """

    from app.db.session import create_memory_tables, make_safe_database_url, get_database_url

    url = database_url or get_database_url()
    engine = create_database_engine(url)
    create_memory_tables(url)

    plan = memory_snapshot_to_insert_plan(snapshot)
    with session_scope(engine) as session:
        existing = session.get(MemorySnapshotORM, snapshot.snapshot_id)
        if existing:
            counts = _count_tables(engine)
            return MemoryPostgresPersistenceResult(
                snapshot_id=snapshot.snapshot_id,
                inserted=False,
                database_url_safe=make_safe_database_url(url),
                table_counts=counts,
                message="Snapshot already exists. No duplicate rows inserted.",
            )

        session.add(MemorySnapshotORM(**plan.snapshot))
        session.add_all(ObservationRecordORM(**row) for row in plan.observations)
        session.add_all(ScoreRecordORM(**row) for row in plan.scores)
        session.add_all(DecisionRecordORM(**row) for row in plan.decisions)
        session.add_all(UncertaintyRecordORM(**row) for row in plan.uncertainties)
        session.add_all(MapUpdateRecordORM(**row) for row in plan.map_updates)

    counts = _count_tables(engine)
    return MemoryPostgresPersistenceResult(
        snapshot_id=snapshot.snapshot_id,
        inserted=True,
        database_url_safe=make_safe_database_url(url),
        table_counts=counts,
        message="MemorySnapshot persisted to database.",
    )


def persist_simulated_memory_snapshot_to_database(database_url: str | None = None) -> MemoryPostgresPersistenceResult:
    """Generate the default simulated memory snapshot and persist it to DB."""

    return persist_memory_snapshot_to_database(generate_simulated_memory_snapshot(), database_url=database_url)


def list_database_memory_snapshots(database_url: str | None = None) -> MemoryPostgresSnapshotList:
    """List persisted memory snapshots from the database."""

    engine = create_database_engine(database_url)
    with session_scope(engine) as session:
        rows = session.scalars(select(MemorySnapshotORM).order_by(MemorySnapshotORM.generated_at.desc())).all()
        summaries: list[MemoryPostgresSnapshotSummary] = []
        for row in rows:
            summaries.append(
                MemoryPostgresSnapshotSummary(
                    snapshot_id=row.snapshot_id,
                    mission_id=row.mission_id,
                    generated_at=row.generated_at.isoformat(),
                    observation_count=len(row.observations),
                    score_count=len(row.scores),
                    decision_count=len(row.decisions),
                    uncertainty_count=len(row.uncertainties),
                    map_update_count=len(row.map_updates),
                )
            )
    return MemoryPostgresSnapshotList(snapshots=summaries, count=len(summaries))
