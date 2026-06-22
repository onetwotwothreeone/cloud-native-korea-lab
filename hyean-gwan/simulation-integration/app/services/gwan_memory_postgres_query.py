"""PostgreSQL/SQLAlchemy query API for persisted GWAN memory records.

15_GWAN_PostgreSQL_Query_API

The JSONL query API proved the query shape. This module applies the same
operator-facing query contract to relational tables so GWAN memory can be
searched directly from PostgreSQL or any SQLAlchemy-compatible test database.
"""

from __future__ import annotations

from sqlalchemy import and_, func, select

from app.db.gwan_memory_models import (
    DecisionRecordORM,
    MapUpdateRecordORM,
    MemorySnapshotORM,
    ObservationRecordORM,
    ScoreRecordORM,
    UncertaintyRecordORM,
)
from app.db.session import create_database_engine, session_scope
from app.services.gwan_memory_query import MemoryQueryMatch, MemoryQueryRequest, MemoryQueryResponse


def _base_object_query():
    """Build the object-level relational query used by the DB memory search."""

    return (
        select(
            MemorySnapshotORM.snapshot_id,
            MemorySnapshotORM.mission_id,
            ObservationRecordORM.object_id,
            ObservationRecordORM.object_name,
            ObservationRecordORM.object_type,
            ObservationRecordORM.display_category,
            DecisionRecordORM.recommended_action,
            DecisionRecordORM.alert_level,
            ScoreRecordORM.risk_score,
            ScoreRecordORM.uncertainty_score,
            ScoreRecordORM.survival_priority_score,
            MapUpdateRecordORM.map_layer,
            UncertaintyRecordORM.uncertainty_reason,
            MapUpdateRecordORM.summary,
            MemorySnapshotORM.generated_at,
        )
        .select_from(MemorySnapshotORM)
        .join(
            ObservationRecordORM,
            ObservationRecordORM.snapshot_id == MemorySnapshotORM.snapshot_id,
        )
        .join(
            ScoreRecordORM,
            and_(
                ScoreRecordORM.snapshot_id == ObservationRecordORM.snapshot_id,
                ScoreRecordORM.object_id == ObservationRecordORM.object_id,
            ),
        )
        .join(
            DecisionRecordORM,
            and_(
                DecisionRecordORM.snapshot_id == ObservationRecordORM.snapshot_id,
                DecisionRecordORM.object_id == ObservationRecordORM.object_id,
            ),
        )
        .outerjoin(
            UncertaintyRecordORM,
            and_(
                UncertaintyRecordORM.snapshot_id == ObservationRecordORM.snapshot_id,
                UncertaintyRecordORM.object_id == ObservationRecordORM.object_id,
            ),
        )
        .outerjoin(
            MapUpdateRecordORM,
            and_(
                MapUpdateRecordORM.snapshot_id == ObservationRecordORM.snapshot_id,
                MapUpdateRecordORM.object_id == ObservationRecordORM.object_id,
            ),
        )
    )


def _apply_filters(statement, query: MemoryQueryRequest):
    """Apply MemoryQueryRequest filters to the SQL statement."""

    if query.snapshot_id:
        statement = statement.where(MemorySnapshotORM.snapshot_id == query.snapshot_id)
    if query.mission_id:
        statement = statement.where(MemorySnapshotORM.mission_id == query.mission_id)
    if query.object_id:
        statement = statement.where(ObservationRecordORM.object_id == query.object_id)
    if query.map_layer:
        statement = statement.where(MapUpdateRecordORM.map_layer == query.map_layer)
    if query.display_category:
        statement = statement.where(ObservationRecordORM.display_category == query.display_category)
    if query.recommended_action:
        statement = statement.where(DecisionRecordORM.recommended_action == query.recommended_action)
    if query.alert_level:
        statement = statement.where(DecisionRecordORM.alert_level == query.alert_level)
    if query.min_risk_score is not None:
        statement = statement.where(ScoreRecordORM.risk_score >= query.min_risk_score)
    if query.min_uncertainty_score is not None:
        statement = statement.where(ScoreRecordORM.uncertainty_score >= query.min_uncertainty_score)
    return statement


def query_database_memory_snapshots(
    query: MemoryQueryRequest | None = None,
    *,
    database_url: str | None = None,
) -> MemoryQueryResponse:
    """Query relational GWAN memory tables with operator-facing filters."""

    query = query or MemoryQueryRequest()
    engine = create_database_engine(database_url)

    with session_scope(engine) as session:
        total_snapshots = session.scalar(select(func.count()).select_from(MemorySnapshotORM)) or 0
        statement = _apply_filters(_base_object_query(), query)
        statement = statement.order_by(MemorySnapshotORM.generated_at.desc(), ObservationRecordORM.object_id).limit(
            query.limit
        )
        rows = session.execute(statement).all()

    matches = [
        MemoryQueryMatch(
            snapshot_id=row.snapshot_id,
            mission_id=row.mission_id,
            object_id=row.object_id,
            object_name=row.object_name,
            object_type=row.object_type,
            display_category=row.display_category,
            recommended_action=row.recommended_action,
            alert_level=row.alert_level,
            risk_score=row.risk_score,
            uncertainty_score=row.uncertainty_score,
            survival_priority_score=row.survival_priority_score,
            map_layer=row.map_layer,
            uncertainty_reason=row.uncertainty_reason,
            map_update_summary=row.summary,
        )
        for row in rows
    ]

    return MemoryQueryResponse(
        query=query,
        total_snapshots_scanned=total_snapshots,
        total_matches=len(matches),
        matches=matches,
    )


def query_database_object_history(
    object_id: str,
    *,
    limit: int = 50,
    database_url: str | None = None,
) -> MemoryQueryResponse:
    """Convenience helper for querying relational memory by object_id."""

    return query_database_memory_snapshots(MemoryQueryRequest(object_id=object_id, limit=limit), database_url=database_url)
