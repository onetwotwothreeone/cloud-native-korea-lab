"""SQLAlchemy table design for future PostgreSQL GWAN memory persistence.

13_GWAN_Memory_PostgreSQL_Design

This module does not replace the current JSONL persistence yet. It defines the
relational table structure that the JSONL memory records can later migrate to.

Design rule:
- Keep one MemorySnapshot as the parent record.
- Store observations, scores, decisions, uncertainties, and map updates as child
  tables linked by snapshot_id.
- Store enum-like values as strings at this stage to keep migrations simple.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all GWAN memory database models."""


class MemorySnapshotORM(Base):
    """One complete GWAN memory snapshot."""

    __tablename__ = "memory_snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    mission_id: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    observations: Mapped[list[ObservationRecordORM]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )
    scores: Mapped[list[ScoreRecordORM]] = relationship(back_populates="snapshot", cascade="all, delete-orphan")
    decisions: Mapped[list[DecisionRecordORM]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )
    uncertainties: Mapped[list[UncertaintyRecordORM]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )
    map_updates: Mapped[list[MapUpdateRecordORM]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )


class ObservationRecordORM(Base):
    """What GWAN observed or represented in the spatial package."""

    __tablename__ = "observation_records"

    record_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("memory_snapshots.snapshot_id"), index=True, nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    object_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    object_type: Mapped[str] = mapped_column(String(120), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    range_scale: Mapped[str] = mapped_column(String(80), nullable=False)
    relative_position_3d: Mapped[dict] = mapped_column(JSON, nullable=False)
    distance_au: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    display_category: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    data_classification: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    source_summary: Mapped[str] = mapped_column(Text, nullable=False)

    snapshot: Mapped[MemorySnapshotORM] = relationship(back_populates="observations")


class ScoreRecordORM(Base):
    """Scores that influenced a GWAN decision."""

    __tablename__ = "score_records"

    record_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("memory_snapshots.snapshot_id"), index=True, nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    case_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    energy_score: Mapped[float] = mapped_column(Float, nullable=False)
    resource_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    exploration_value_score: Mapped[float] = mapped_column(Float, nullable=False)
    uncertainty_score: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    survival_priority_score: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    snapshot: Mapped[MemorySnapshotORM] = relationship(back_populates="scores")


class DecisionRecordORM(Base):
    """Recommended action and reason from GWAN."""

    __tablename__ = "decision_records"

    record_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("memory_snapshots.snapshot_id"), index=True, nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    case_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    recommended_action: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    reason_summary: Mapped[str] = mapped_column(Text, nullable=False)
    alert_level: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    snapshot: Mapped[MemorySnapshotORM] = relationship(back_populates="decisions")


class UncertaintyRecordORM(Base):
    """Uncertainty that must remain visible in memory and future map updates."""

    __tablename__ = "uncertainty_records"

    record_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("memory_snapshots.snapshot_id"), index=True, nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    uncertainty_type: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    uncertainty_reason: Mapped[str] = mapped_column(Text, nullable=False)
    impact_on_decision: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_resolution: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    snapshot: Mapped[MemorySnapshotORM] = relationship(back_populates="uncertainties")


class MapUpdateRecordORM(Base):
    """How one object should change the survival map."""

    __tablename__ = "map_update_records"

    update_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("memory_snapshots.snapshot_id"), index=True, nullable=False)
    object_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    map_layer: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    update_type: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    update_survival_map: Mapped[bool] = mapped_column(Boolean, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    snapshot: Mapped[MemorySnapshotORM] = relationship(back_populates="map_updates")
