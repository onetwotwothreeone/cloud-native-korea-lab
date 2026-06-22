"""Query API models and helpers for persisted GWAN memory snapshots.

12_GWAN_Memory_Query_API

The previous step stored MemorySnapshot records as JSONL. This module adds a
small query layer so operators and future UI code can search memory by object,
map layer, recommended action, risk, uncertainty, and display category.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from app.schemas.gwan_interface import ContractBaseModel, DisplayCategory, RecommendedAction
from app.services.gwan_memory import MapLayer, MemorySnapshot
from app.services.gwan_memory_persistence import default_memory_store

AlertLevel = Literal["none", "info", "low", "medium", "high", "critical"]


class MemoryQueryRequest(ContractBaseModel):
    """Filters for querying persisted MemorySnapshot records."""

    snapshot_id: str | None = None
    mission_id: str | None = None
    object_id: str | None = None
    map_layer: MapLayer | None = None
    display_category: DisplayCategory | None = None
    recommended_action: RecommendedAction | None = None
    alert_level: AlertLevel | None = None
    min_risk_score: float | None = Field(default=None, ge=0, le=1)
    min_uncertainty_score: float | None = Field(default=None, ge=0, le=1)
    limit: int = Field(default=50, ge=1, le=500)

    @model_validator(mode="after")
    def validate_at_least_one_filter_for_large_queries(self) -> Self:
        # Empty query is allowed for API convenience, but limit keeps it safe.
        return self


class MemoryQueryMatch(ContractBaseModel):
    """One object-level memory result joined across snapshot records."""

    snapshot_id: str
    mission_id: str
    object_id: str
    object_name: str | None = None
    object_type: str
    display_category: DisplayCategory
    recommended_action: RecommendedAction
    alert_level: AlertLevel
    risk_score: float = Field(..., ge=0, le=1)
    uncertainty_score: float = Field(..., ge=0, le=1)
    survival_priority_score: float = Field(..., ge=0, le=1)
    map_layer: MapLayer | None = None
    uncertainty_reason: str | None = None
    map_update_summary: str | None = None


class MemoryQueryResponse(ContractBaseModel):
    """Response returned by the memory query API."""

    query: MemoryQueryRequest
    total_snapshots_scanned: int = Field(..., ge=0)
    total_matches: int = Field(..., ge=0)
    matches: list[MemoryQueryMatch]


def _snapshot_to_matches(snapshot: MemorySnapshot) -> list[MemoryQueryMatch]:
    """Flatten one MemorySnapshot into object-level query matches."""

    observations_by_id = {record.object_id: record for record in snapshot.observations}
    scores_by_id = {record.object_id: record for record in snapshot.scores}
    decisions_by_id = {record.object_id: record for record in snapshot.decisions}
    uncertainties_by_id = {record.object_id: record for record in snapshot.uncertainties}
    map_updates_by_id = {record.object_id: record for record in snapshot.map_updates}

    matches: list[MemoryQueryMatch] = []
    for object_id, observation in observations_by_id.items():
        score_record = scores_by_id.get(object_id)
        decision_record = decisions_by_id.get(object_id)
        if not score_record or not decision_record:
            # A partial memory record should not crash query use. It simply is
            # not query-ready yet.
            continue

        uncertainty_record = uncertainties_by_id.get(object_id)
        map_update = map_updates_by_id.get(object_id)
        matches.append(
            MemoryQueryMatch(
                snapshot_id=snapshot.snapshot_id,
                mission_id=snapshot.mission_id,
                object_id=object_id,
                object_name=observation.object_name,
                object_type=observation.object_type,
                display_category=observation.display_category,
                recommended_action=decision_record.recommended_action,
                alert_level=decision_record.alert_level,
                risk_score=score_record.scores.risk_score,
                uncertainty_score=score_record.scores.uncertainty_score,
                survival_priority_score=score_record.scores.survival_priority_score,
                map_layer=map_update.map_layer if map_update else None,
                uncertainty_reason=uncertainty_record.uncertainty_reason if uncertainty_record else None,
                map_update_summary=map_update.summary if map_update else None,
            )
        )
    return matches


def _match_passes_query(match: MemoryQueryMatch, query: MemoryQueryRequest) -> bool:
    """Return whether one flattened match satisfies the query filters."""

    if query.snapshot_id and match.snapshot_id != query.snapshot_id:
        return False
    if query.mission_id and match.mission_id != query.mission_id:
        return False
    if query.object_id and match.object_id != query.object_id:
        return False
    if query.map_layer and match.map_layer != query.map_layer:
        return False
    if query.display_category and match.display_category != query.display_category:
        return False
    if query.recommended_action and match.recommended_action != query.recommended_action:
        return False
    if query.alert_level and match.alert_level != query.alert_level:
        return False
    if query.min_risk_score is not None and match.risk_score < query.min_risk_score:
        return False
    if query.min_uncertainty_score is not None and match.uncertainty_score < query.min_uncertainty_score:
        return False
    return True


def query_memory_snapshots(
    snapshots: list[MemorySnapshot],
    query: MemoryQueryRequest | None = None,
) -> MemoryQueryResponse:
    """Query in-memory snapshot objects using object-level filters."""

    query = query or MemoryQueryRequest()
    all_matches: list[MemoryQueryMatch] = []
    for snapshot in snapshots:
        all_matches.extend(_snapshot_to_matches(snapshot))

    filtered = [match for match in all_matches if _match_passes_query(match, query)]
    limited = filtered[: query.limit]

    return MemoryQueryResponse(
        query=query,
        total_snapshots_scanned=len(snapshots),
        total_matches=len(filtered),
        matches=limited,
    )


def query_persisted_memory_snapshots(query: MemoryQueryRequest | None = None) -> MemoryQueryResponse:
    """Query snapshots from the default JSONL memory store."""

    return query_memory_snapshots(default_memory_store().list_snapshots(), query)


def query_object_history(object_id: str, *, limit: int = 50) -> MemoryQueryResponse:
    """Convenience helper for querying all records for one object ID."""

    return query_persisted_memory_snapshots(MemoryQueryRequest(object_id=object_id, limit=limit))
