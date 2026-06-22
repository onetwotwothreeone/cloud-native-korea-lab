"""Memory and map update models for GWAN.

10_GWAN_Memory_Map_Update_Model

GWAN should not only produce an interface payload. It should also preserve what
it observed, how it scored, what it decided, why uncertainty mattered, and how
the survival map should be updated.

This module converts an integrated simulation result into a MemorySnapshot.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import Field

from app.schemas.gwan_interface import (
    ConfidenceLabel,
    ContractBaseModel,
    DataClassification,
    DisplayCategory,
    Position3D,
    RangeScale,
    RecommendedAction,
    Scores,
    UncertaintyType,
)
from app.services.gwan_simulation import IntegratedSimulationResult, generate_integrated_simulation_result


MapLayer = Literal["resource_candidates", "risk_zones", "navigation_references", "observation_targets", "general_memory"]
MapUpdateType = Literal[
    "store_candidate",
    "store_risk_zone",
    "refresh_navigation_reference",
    "store_observation_target",
    "store_wait_state",
]


class ObservationRecord(ContractBaseModel):
    """What GWAN observed or represented in the spatial package."""

    record_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    object_name: str | None = None
    object_type: str = Field(..., min_length=1)
    observed_at: datetime
    range_scale: RangeScale
    relative_position_3d: Position3D
    distance_au: float | None = Field(default=None, ge=0)
    distance_km: float | None = Field(default=None, ge=0)
    display_category: DisplayCategory
    confidence_label: ConfidenceLabel
    data_classification: DataClassification
    source_summary: str = Field(..., min_length=1)


class ScoreRecord(ContractBaseModel):
    """Scores that influenced a GWAN decision."""

    record_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    case_id: str = Field(..., min_length=1)
    scores: Scores
    created_at: datetime


class DecisionRecord(ContractBaseModel):
    """Recommended action and reason from GWAN."""

    record_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    case_id: str = Field(..., min_length=1)
    recommended_action: RecommendedAction
    reason_summary: str = Field(..., min_length=1)
    alert_level: Literal["none", "info", "low", "medium", "high", "critical"]
    created_at: datetime


class MemoryUncertaintyRecord(ContractBaseModel):
    """Uncertainty that must remain visible in memory and future map updates."""

    record_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    uncertainty_type: UncertaintyType
    uncertainty_reason: str = Field(..., min_length=1)
    impact_on_decision: str = Field(..., min_length=1)
    suggested_resolution: str = Field(..., min_length=1)
    confidence_label: ConfidenceLabel
    created_at: datetime


class MapUpdateRecord(ContractBaseModel):
    """How one object should change the survival map."""

    update_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    map_layer: MapLayer
    update_type: MapUpdateType
    update_survival_map: bool
    summary: str = Field(..., min_length=1)
    created_at: datetime


class MemorySnapshot(ContractBaseModel):
    """A complete memory snapshot from one GWAN run."""

    snapshot_id: str = Field(..., min_length=1)
    mission_id: str = Field(..., min_length=1)
    generated_at: datetime
    observations: list[ObservationRecord]
    scores: list[ScoreRecord]
    decisions: list[DecisionRecord]
    uncertainties: list[MemoryUncertaintyRecord]
    map_updates: list[MapUpdateRecord]

    def object_count(self) -> int:
        return len({record.object_id for record in self.observations})

    def high_risk_count(self) -> int:
        return sum(1 for decision in self.decisions if decision.alert_level in {"high", "critical"})

    def map_layers(self) -> set[MapLayer]:
        return {update.map_layer for update in self.map_updates}


def _map_update_for_object(
    *,
    object_id: str,
    display_category: DisplayCategory,
    action: RecommendedAction,
    created_at: datetime,
) -> MapUpdateRecord:
    """Translate a GWAN decision into a survival-map update record."""

    if action == RecommendedAction.AVOID or display_category == DisplayCategory.RISK_ZONE:
        return MapUpdateRecord(
            update_id=f"map-update-{object_id}",
            object_id=object_id,
            map_layer="risk_zones",
            update_type="store_risk_zone",
            update_survival_map=True,
            summary="Store or refresh this object as a risk zone for future avoidance planning.",
            created_at=created_at,
        )
    if display_category == DisplayCategory.NAVIGATION_REFERENCE:
        return MapUpdateRecord(
            update_id=f"map-update-{object_id}",
            object_id=object_id,
            map_layer="navigation_references",
            update_type="refresh_navigation_reference",
            update_survival_map=True,
            summary="Refresh this object as a navigation reference in the survival map.",
            created_at=created_at,
        )
    if display_category == DisplayCategory.RESOURCE_CANDIDATE:
        return MapUpdateRecord(
            update_id=f"map-update-{object_id}",
            object_id=object_id,
            map_layer="resource_candidates",
            update_type="store_candidate",
            update_survival_map=True,
            summary="Store this object as a resource candidate with current scores and uncertainty.",
            created_at=created_at,
        )
    if display_category == DisplayCategory.OBSERVATION_TARGET:
        return MapUpdateRecord(
            update_id=f"map-update-{object_id}",
            object_id=object_id,
            map_layer="observation_targets",
            update_type="store_observation_target",
            update_survival_map=True,
            summary="Store this object as an observation target for later review.",
            created_at=created_at,
        )
    return MapUpdateRecord(
        update_id=f"map-update-{object_id}",
        object_id=object_id,
        map_layer="general_memory",
        update_type="store_wait_state",
        update_survival_map=False,
        summary="Keep this object in general memory without changing a priority map layer.",
        created_at=created_at,
    )


def create_memory_snapshot_from_integrated_result(
    result: IntegratedSimulationResult,
    *,
    snapshot_id: str | None = None,
) -> MemorySnapshot:
    """Convert integrated simulation output into persistent memory records."""

    payload = result.payload
    now = datetime.now(UTC)
    snapshot_id = snapshot_id or f"memory-snapshot-{payload.mission_context.mission_id}"
    spatial_package = payload.packages.spatial_visualization_package
    spatial_by_id = {item.object_id: item for item in spatial_package.objects}

    observations = [
        ObservationRecord(
            record_id=f"obs-{item.object_id}",
            object_id=item.object_id,
            object_name=item.object_name,
            object_type=item.object_type,
            observed_at=payload.generated_at,
            range_scale=spatial_package.range_scale,
            relative_position_3d=item.relative_position_3d,
            distance_au=item.distance_au,
            distance_km=item.distance_km,
            display_category=item.display_category,
            confidence_label=item.confidence_label,
            data_classification=item.data_classification,
            source_summary="Generated from GWAN spatial_visualization_package.",
        )
        for item in spatial_package.objects
    ]

    score_records = [
        ScoreRecord(
            record_id=f"score-{pair.simulated_object.object_id}",
            object_id=pair.simulated_object.object_id,
            case_id=pair.decision.case_id,
            scores=pair.decision.scores,
            created_at=now,
        )
        for pair in result.object_decisions
    ]

    decision_records = [
        DecisionRecord(
            record_id=f"decision-{pair.simulated_object.object_id}",
            object_id=pair.simulated_object.object_id,
            case_id=pair.decision.case_id,
            recommended_action=pair.decision.recommended_action,
            reason_summary=pair.decision.reason_summary,
            alert_level=pair.decision.alert_level,
            created_at=now,
        )
        for pair in result.object_decisions
    ]

    uncertainty_items = payload.packages.uncertainty_package.items if payload.packages.uncertainty_package else []
    uncertainty_records = [
        MemoryUncertaintyRecord(
            record_id=f"memory-{item.uncertainty_id}",
            object_id=item.object_id,
            uncertainty_type=item.uncertainty_type,
            uncertainty_reason=item.uncertainty_reason,
            impact_on_decision=item.impact_on_decision,
            suggested_resolution=item.suggested_resolution,
            confidence_label=item.confidence_label,
            created_at=now,
        )
        for item in uncertainty_items
    ]

    map_updates = [
        _map_update_for_object(
            object_id=decision.object_id,
            display_category=spatial_by_id[decision.object_id].display_category,
            action=decision.recommended_action,
            created_at=now,
        )
        for decision in decision_records
    ]

    return MemorySnapshot(
        snapshot_id=snapshot_id,
        mission_id=payload.mission_context.mission_id,
        generated_at=now,
        observations=observations,
        scores=score_records,
        decisions=decision_records,
        uncertainties=uncertainty_records,
        map_updates=map_updates,
    )


def generate_simulated_memory_snapshot() -> MemorySnapshot:
    """Generate a memory snapshot from the default integrated simulation."""

    return create_memory_snapshot_from_integrated_result(generate_integrated_simulation_result())
