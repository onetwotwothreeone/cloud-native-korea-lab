"""PostgreSQL design helpers for GWAN memory persistence.

This is a design and migration-preparation layer. It does not connect to a real
PostgreSQL database yet. It provides:
- table design metadata for docs/API inspection
- conversion from MemorySnapshot to database-ready row dictionaries
"""

from __future__ import annotations

from typing import Any

from app.db.gwan_memory_models import Base
from app.schemas.gwan_interface import ContractBaseModel
from app.services.gwan_memory import MemorySnapshot, generate_simulated_memory_snapshot


class MemoryPostgresTableDesign(ContractBaseModel):
    table_name: str
    purpose: str
    primary_key: str
    important_indexes: list[str]
    parent_table: str | None = None


class MemoryPostgresDesignResponse(ContractBaseModel):
    design_version: str = "hyean.gwan.memory.postgres.v0.1"
    tables: list[MemoryPostgresTableDesign]
    migration_note: str


class MemoryDatabaseInsertPlan(ContractBaseModel):
    """Database-ready rows derived from one MemorySnapshot."""

    snapshot: dict[str, Any]
    observations: list[dict[str, Any]]
    scores: list[dict[str, Any]]
    decisions: list[dict[str, Any]]
    uncertainties: list[dict[str, Any]]
    map_updates: list[dict[str, Any]]

    def total_child_rows(self) -> int:
        return len(self.observations) + len(self.scores) + len(self.decisions) + len(self.uncertainties) + len(self.map_updates)


def get_memory_postgres_design() -> MemoryPostgresDesignResponse:
    """Return the first official PostgreSQL table design for GWAN memory."""

    return MemoryPostgresDesignResponse(
        tables=[
            MemoryPostgresTableDesign(
                table_name="memory_snapshots",
                purpose="Parent record for one complete GWAN memory run.",
                primary_key="snapshot_id",
                important_indexes=["mission_id", "generated_at"],
            ),
            MemoryPostgresTableDesign(
                table_name="observation_records",
                purpose="Stores what GWAN observed or represented in spatial output.",
                primary_key="record_id",
                important_indexes=["snapshot_id", "object_id", "display_category", "data_classification"],
                parent_table="memory_snapshots",
            ),
            MemoryPostgresTableDesign(
                table_name="score_records",
                purpose="Stores energy, resource, risk, exploration, uncertainty, and survival priority scores.",
                primary_key="record_id",
                important_indexes=["snapshot_id", "object_id", "risk_score", "uncertainty_score", "survival_priority_score"],
                parent_table="memory_snapshots",
            ),
            MemoryPostgresTableDesign(
                table_name="decision_records",
                purpose="Stores recommended action, reason summary, and alert level.",
                primary_key="record_id",
                important_indexes=["snapshot_id", "object_id", "recommended_action", "alert_level"],
                parent_table="memory_snapshots",
            ),
            MemoryPostgresTableDesign(
                table_name="uncertainty_records",
                purpose="Stores uncertainty reason, impact on decision, and suggested resolution.",
                primary_key="record_id",
                important_indexes=["snapshot_id", "object_id", "uncertainty_type", "confidence_label"],
                parent_table="memory_snapshots",
            ),
            MemoryPostgresTableDesign(
                table_name="map_update_records",
                purpose="Stores how each object should update the living survival map.",
                primary_key="update_id",
                important_indexes=["snapshot_id", "object_id", "map_layer", "update_type"],
                parent_table="memory_snapshots",
            ),
        ],
        migration_note="Keep JSONL as the simple local log for now. Use these tables when the project needs query speed, relationships, concurrency, and durable service storage.",
    )


def get_sqlalchemy_table_names() -> list[str]:
    """Return SQLAlchemy table names for tests and inspection."""

    return sorted(Base.metadata.tables.keys())


def memory_snapshot_to_insert_plan(snapshot: MemorySnapshot) -> MemoryDatabaseInsertPlan:
    """Convert a MemorySnapshot into database-ready row dictionaries."""

    snapshot_row = {
        "snapshot_id": snapshot.snapshot_id,
        "mission_id": snapshot.mission_id,
        "generated_at": snapshot.generated_at,
    }

    observations = [
        {
            "record_id": record.record_id,
            "snapshot_id": snapshot.snapshot_id,
            "object_id": record.object_id,
            "object_name": record.object_name,
            "object_type": record.object_type,
            "observed_at": record.observed_at,
            "range_scale": record.range_scale.value,
            "relative_position_3d": record.relative_position_3d.model_dump(mode="json", exclude_none=True),
            "distance_au": record.distance_au,
            "distance_km": record.distance_km,
            "display_category": record.display_category.value,
            "confidence_label": record.confidence_label.value,
            "data_classification": record.data_classification.value,
            "source_summary": record.source_summary,
        }
        for record in snapshot.observations
    ]

    scores = [
        {
            "record_id": record.record_id,
            "snapshot_id": snapshot.snapshot_id,
            "object_id": record.object_id,
            "case_id": record.case_id,
            "energy_score": record.scores.energy_score,
            "resource_score": record.scores.resource_score,
            "risk_score": record.scores.risk_score,
            "exploration_value_score": record.scores.exploration_value_score,
            "uncertainty_score": record.scores.uncertainty_score,
            "survival_priority_score": record.scores.survival_priority_score,
            "created_at": record.created_at,
        }
        for record in snapshot.scores
    ]

    decisions = [
        {
            "record_id": record.record_id,
            "snapshot_id": snapshot.snapshot_id,
            "object_id": record.object_id,
            "case_id": record.case_id,
            "recommended_action": record.recommended_action.value,
            "reason_summary": record.reason_summary,
            "alert_level": record.alert_level,
            "created_at": record.created_at,
        }
        for record in snapshot.decisions
    ]

    uncertainties = [
        {
            "record_id": record.record_id,
            "snapshot_id": snapshot.snapshot_id,
            "object_id": record.object_id,
            "uncertainty_type": record.uncertainty_type.value,
            "uncertainty_reason": record.uncertainty_reason,
            "impact_on_decision": record.impact_on_decision,
            "suggested_resolution": record.suggested_resolution,
            "confidence_label": record.confidence_label.value,
            "created_at": record.created_at,
        }
        for record in snapshot.uncertainties
    ]

    map_updates = [
        {
            "update_id": record.update_id,
            "snapshot_id": snapshot.snapshot_id,
            "object_id": record.object_id,
            "map_layer": record.map_layer,
            "update_type": record.update_type,
            "update_survival_map": record.update_survival_map,
            "summary": record.summary,
            "created_at": record.created_at,
        }
        for record in snapshot.map_updates
    ]

    return MemoryDatabaseInsertPlan(
        snapshot=snapshot_row,
        observations=observations,
        scores=scores,
        decisions=decisions,
        uncertainties=uncertainties,
        map_updates=map_updates,
    )


def generate_simulated_memory_insert_plan() -> MemoryDatabaseInsertPlan:
    """Generate an insert plan from the default simulated memory snapshot."""

    return memory_snapshot_to_insert_plan(generate_simulated_memory_snapshot())
