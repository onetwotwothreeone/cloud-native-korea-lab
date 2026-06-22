"""Pydantic models for the GWAN -> HYEAN Operator Interface data contract.

The models implement the structured output contract:
GWAN calculates and explains. HYEAN Operator Interface displays, filters,
alerts, and supports fast human judgment.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


Score = float


class ContractBaseModel(BaseModel):
    """Base class for all contract models."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class DataClassification(str, Enum):
    KNOWN = "known"
    ESTIMATED = "estimated"
    SIMULATED = "simulated"
    HYPOTHESIS = "hypothesis"
    FICTIONAL_FUTURE_SCENARIO = "fictional_future_scenario"


class ConfidenceLabel(str, Enum):
    CONFIRMED = "confirmed"
    LIKELY = "likely"
    UNCERTAIN = "uncertain"
    LOW_CONFIDENCE = "low_confidence"
    UNKNOWN = "unknown"


class DisplayCategory(str, Enum):
    ENERGY_CANDIDATE = "energy_candidate"
    RESOURCE_CANDIDATE = "resource_candidate"
    RISK_ZONE = "risk_zone"
    OBSERVATION_TARGET = "observation_target"
    UNCERTAIN_DETECTION = "uncertain_detection"
    NAVIGATION_REFERENCE = "navigation_reference"
    MICRO_PROBE = "micro_probe"
    LONG_TERM_CANDIDATE = "long_term_candidate"


class VisualMarkerType(str, Enum):
    PIN = "pin"
    REGION = "region"
    TRAJECTORY = "trajectory"
    SPHERE = "sphere"
    PROBE = "probe"
    WARNING_ZONE = "warning_zone"
    UNKNOWN_POINT = "unknown_point"


class RecommendedAction(str, Enum):
    AVOID = "avoid"
    WAIT = "wait"
    OBSERVE_MORE = "observe_more"
    APPROACH = "approach"
    SEND_MICRO_PROBE = "send_micro_probe"
    MARK_AS_LONG_TERM_CANDIDATE = "mark_as_long_term_candidate"
    UPDATE_SURVIVAL_MAP = "update_survival_map"
    REQUEST_ADDITIONAL_SPECTRAL_OBSERVATION = "request_additional_spectral_observation"


class AlertSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertCategory(str, Enum):
    RISK = "risk"
    UNCERTAINTY = "uncertainty"
    OBSERVATION_REQUEST = "observation_request"
    MISSION_UPDATE = "mission_update"
    MAP_UPDATE = "map_update"


class UncertaintyType(str, Enum):
    WEAK_SIGNAL = "weak_signal"
    MISSING_DATA = "missing_data"
    CONFLICTING_OBSERVATION = "conflicting_observation"
    HIGH_DISTANCE = "high_distance"
    LOW_RESOLUTION = "low_resolution"
    STALE_CATALOG_DATA = "stale_catalog_data"
    SIMULATED_ONLY = "simulated_only"
    UNKNOWN_SOURCE = "unknown_source"


class RangeScale(str, Enum):
    LOCAL_KM = "local_km"
    TACTICAL_KM = "tactical_km"
    REGIONAL_0_01_TO_1_AU = "regional_0_01_to_1_AU"
    STRATEGIC_OVER_1_AU = "strategic_over_1_AU"


class MissionContext(ContractBaseModel):
    mission_id: str = Field(..., min_length=1)
    observer: str = Field(..., min_length=1)
    operator_intent: str = Field(..., min_length=1)
    mission_phase: str | None = None
    priority_context: str | None = None


class CoordinateReference(ContractBaseModel):
    origin: str = Field(default="spacecraft")
    frame: str = Field(default="spacecraft_relative_cartesian")
    unit: Literal["AU", "km"] = "AU"


class Position3D(ContractBaseModel):
    """3D position relative to the spacecraft.

    Use either AU coordinates or km coordinates. Do not mix units inside a single
    position object.
    """

    x_au: float | None = None
    y_au: float | None = None
    z_au: float | None = None
    x_km: float | None = None
    y_km: float | None = None
    z_km: float | None = None

    @model_validator(mode="after")
    def validate_coordinate_group(self) -> Self:
        au_values = [self.x_au, self.y_au, self.z_au]
        km_values = [self.x_km, self.y_km, self.z_km]
        has_any_au = any(value is not None for value in au_values)
        has_all_au = all(value is not None for value in au_values)
        has_any_km = any(value is not None for value in km_values)
        has_all_km = all(value is not None for value in km_values)

        if has_any_au and not has_all_au:
            raise ValueError("AU coordinates must include x_au, y_au, and z_au together.")
        if has_any_km and not has_all_km:
            raise ValueError("km coordinates must include x_km, y_km, and z_km together.")
        if has_all_au and has_all_km:
            raise ValueError("Do not mix AU and km coordinates in one Position3D object.")
        if not has_all_au and not has_all_km:
            raise ValueError("Position3D requires either AU coordinates or km coordinates.")
        return self


class MarkerStyle(ContractBaseModel):
    color_group: str = Field(..., min_length=1)
    outline: str | None = None
    pattern: str | None = None
    number_badge: float | int | None = None
    label: str | None = None


class Scores(ContractBaseModel):
    energy_score: Score = Field(..., ge=0, le=1)
    resource_score: Score = Field(..., ge=0, le=1)
    risk_score: Score = Field(..., ge=0, le=1)
    exploration_value_score: Score = Field(..., ge=0, le=1)
    uncertainty_score: Score = Field(..., ge=0, le=1)
    survival_priority_score: Score = Field(..., ge=0, le=1)


class ProvenanceRecord(ContractBaseModel):
    source_type: str = Field(..., min_length=1)
    source_id: str = Field(..., min_length=1)
    data_classification: DataClassification | None = None
    source_timestamp: datetime | None = None
    url: str | None = None


class SpatialObject(ContractBaseModel):
    object_id: str = Field(..., min_length=1)
    object_name: str | None = None
    object_type: str = Field(..., min_length=1)
    relative_position_3d: Position3D
    distance_au: float | None = Field(default=None, ge=0)
    distance_km: float | None = Field(default=None, ge=0)
    velocity_context: str | None = None
    display_category: DisplayCategory
    visual_marker_type: VisualMarkerType
    marker_style: MarkerStyle
    confidence_label: ConfidenceLabel
    data_classification: DataClassification
    uncertainty_score: Score | None = Field(default=None, ge=0, le=1)
    recommended_action: RecommendedAction | None = None

    @model_validator(mode="after")
    def validate_uncertainty_score_for_uncertain_labels(self) -> Self:
        if self.confidence_label in {
            ConfidenceLabel.UNCERTAIN,
            ConfidenceLabel.LOW_CONFIDENCE,
            ConfidenceLabel.UNKNOWN,
        } and self.uncertainty_score is None:
            raise ValueError("Uncertain or low-confidence spatial objects require uncertainty_score.")
        return self


class SpatialVisualizationPackage(ContractBaseModel):
    package_id: str = Field(..., min_length=1)
    range_scale: RangeScale
    reference_radius_au: float | None = Field(default=None, ge=0)
    reference_radius_km: float | None = Field(default=None, ge=0)
    objects: list[SpatialObject] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_reference_radius_unit(self) -> Self:
        uses_au = self.range_scale in {
            RangeScale.REGIONAL_0_01_TO_1_AU,
            RangeScale.STRATEGIC_OVER_1_AU,
        }
        if uses_au and self.reference_radius_au is None:
            raise ValueError("AU range scales require reference_radius_au.")
        if not uses_au and self.reference_radius_km is None:
            raise ValueError("km range scales require reference_radius_km.")
        return self

    @property
    def object_ids(self) -> set[str]:
        return {item.object_id for item in self.objects}


class SidebarIntelligencePackage(ContractBaseModel):
    package_id: str = Field(..., min_length=1)
    selected_object_id: str = Field(..., min_length=1)
    headline: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    scores: Scores
    spectrum_summary: str | None = None
    interpretation_summary: str = Field(..., min_length=1)
    data_classification: DataClassification
    provenance: list[ProvenanceRecord] = Field(..., min_length=1)
    uncertainty_reason: str | None = None
    recommended_action: RecommendedAction
    required_follow_up_observation: str | None = None


class AlertItem(ContractBaseModel):
    alert_id: str = Field(..., min_length=1)
    object_id: str | None = None
    severity: AlertSeverity
    category: AlertCategory
    message: str = Field(..., min_length=1)
    recommended_operator_response: str = Field(..., min_length=1)
    priority_score: Score = Field(..., ge=0, le=1)
    created_at: datetime


class AlertFeedPackage(ContractBaseModel):
    package_id: str = Field(..., min_length=1)
    alerts: list[AlertItem] = Field(default_factory=list)

    def sorted_alerts(self) -> list[AlertItem]:
        severity_rank = {
            AlertSeverity.CRITICAL: 5,
            AlertSeverity.HIGH: 4,
            AlertSeverity.MEDIUM: 3,
            AlertSeverity.LOW: 2,
            AlertSeverity.INFO: 1,
        }
        return sorted(
            self.alerts,
            key=lambda item: (severity_rank[item.severity], item.priority_score),
            reverse=True,
        )


class UncertaintyRecord(ContractBaseModel):
    uncertainty_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    uncertainty_type: UncertaintyType
    uncertainty_reason: str = Field(..., min_length=1)
    impact_on_decision: str = Field(..., min_length=1)
    suggested_resolution: str = Field(..., min_length=1)
    confidence_label: ConfidenceLabel


class UncertaintyPackage(ContractBaseModel):
    package_id: str = Field(..., min_length=1)
    items: list[UncertaintyRecord] = Field(default_factory=list)

    @property
    def object_ids(self) -> set[str]:
        return {item.object_id for item in self.items}


class MemoryUpdate(ContractBaseModel):
    store_as: str = Field(..., min_length=1)
    update_survival_map: bool
    notes: str | None = None


class DecisionReportPackage(ContractBaseModel):
    package_id: str = Field(..., min_length=1)
    report_id: str = Field(..., min_length=1)
    object_id: str | None = None
    decision_summary: str = Field(..., min_length=1)
    reasoning_steps: list[str] = Field(..., min_length=1)
    recommended_action: RecommendedAction
    memory_update: MemoryUpdate
    provenance: list[ProvenanceRecord] = Field(default_factory=list)


class GWANOutputPackages(ContractBaseModel):
    spatial_visualization_package: SpatialVisualizationPackage
    sidebar_intelligence_package: SidebarIntelligencePackage | None = None
    alert_feed_package: AlertFeedPackage | None = None
    uncertainty_package: UncertaintyPackage | None = None
    decision_report_package: DecisionReportPackage | None = None


class GWANInterfacePayload(ContractBaseModel):
    schema_version: str = Field(default="hyean.gwan.interface.v0.1")
    generated_at: datetime
    mission_context: MissionContext
    coordinate_reference: CoordinateReference
    packages: GWANOutputPackages

    @model_validator(mode="after")
    def validate_cross_package_contract(self) -> Self:
        spatial = self.packages.spatial_visualization_package
        spatial_ids = spatial.object_ids

        sidebar = self.packages.sidebar_intelligence_package
        if sidebar and sidebar.selected_object_id not in spatial_ids:
            raise ValueError(
                f"sidebar selected_object_id '{sidebar.selected_object_id}' does not exist in spatial package."
            )

        alerts = self.packages.alert_feed_package
        if alerts:
            for alert in alerts.alerts:
                if alert.object_id and alert.object_id not in spatial_ids:
                    raise ValueError(
                        f"alert object_id '{alert.object_id}' does not exist in spatial package."
                    )

        uncertainties = self.packages.uncertainty_package
        if uncertainties:
            for item in uncertainties.items:
                if item.object_id not in spatial_ids:
                    raise ValueError(
                        f"uncertainty object_id '{item.object_id}' does not exist in spatial package."
                    )

        report = self.packages.decision_report_package
        if report and report.object_id and report.object_id not in spatial_ids:
            raise ValueError(
                f"decision report object_id '{report.object_id}' does not exist in spatial package."
            )

        uncertain_object_ids = {
            obj.object_id
            for obj in spatial.objects
            if obj.confidence_label
            in {
                ConfidenceLabel.UNCERTAIN,
                ConfidenceLabel.LOW_CONFIDENCE,
                ConfidenceLabel.UNKNOWN,
            }
            or obj.display_category == DisplayCategory.UNCERTAIN_DETECTION
        }
        covered_uncertain_ids = uncertainties.object_ids if uncertainties else set()
        missing_uncertainty_records = uncertain_object_ids - covered_uncertain_ids
        if missing_uncertainty_records:
            raise ValueError(
                "Uncertain spatial objects require uncertainty records: "
                + ", ".join(sorted(missing_uncertainty_records))
            )

        return self

    def alert_count(self) -> int:
        if not self.packages.alert_feed_package:
            return 0
        return len(self.packages.alert_feed_package.alerts)
