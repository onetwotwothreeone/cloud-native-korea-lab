"""GWAN simulation logic integrated with GWAN scoring rules.

09_GWAN_Simulation_To_Interface_Payload_Integration

Before this step, simulation objects and scoring rules could evolve separately.
This module connects them:

simulated object -> scoring case -> scoring decision -> interface payload package
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import ConfigDict, Field

from app.schemas.gwan_interface import (
    AlertCategory,
    AlertFeedPackage,
    AlertItem,
    AlertSeverity,
    ConfidenceLabel,
    ContractBaseModel,
    CoordinateReference,
    DataClassification,
    DecisionReportPackage,
    DisplayCategory,
    GWANInterfacePayload,
    GWANOutputPackages,
    MarkerStyle,
    MemoryUpdate,
    MissionContext,
    Position3D,
    ProvenanceRecord,
    RangeScale,
    RecommendedAction,
    SidebarIntelligencePackage,
    SpatialObject,
    SpatialVisualizationPackage,
    UncertaintyPackage,
    UncertaintyRecord,
    UncertaintyType,
    VisualMarkerType,
)
from app.services.gwan_scoring import GWANScoringCase, GWANScoringDecision, ScoringInputs, recommend_action
from app.services.prevention import assess_prevention
from app.services.prevention.contract_adapter import to_prevention_report
from app.services.prevention.models import PreventionInput, PreventionReading


class GWANSimulationRequest(ContractBaseModel):
    mission_id: str = Field(default="sim-001", min_length=1)
    operator_intent: str = Field(default="regional_resource_scan", min_length=1)
    mission_phase: str = Field(default="regional_scan", min_length=1)
    priority_context: str = Field(default="find resource candidates while avoiding high-risk zones", min_length=1)
    observer: str = Field(default="onboard_gwan_core", min_length=1)


class SimulatedGWANObject(ContractBaseModel):
    """A simulation object that can be scored and transformed into interface payloads."""

    case_id: str
    object_id: str
    object_name: str
    object_type: str
    description: str
    position: Position3D
    distance_au: float = Field(..., ge=0)
    velocity_context: str
    display_category: DisplayCategory
    visual_marker_type: VisualMarkerType
    confidence_label: ConfidenceLabel
    data_classification: DataClassification
    marker_color_group: str
    marker_outline: str | None = None
    marker_pattern: str | None = None
    scoring_inputs: ScoringInputs
    uncertainty_type: UncertaintyType | None = None
    spectrum_summary: str | None = None
    interpretation_summary: str
    uncertainty_reason: str | None = None
    follow_up_observation: str | None = None
    provenance_source_id: str

    def to_scoring_case(self) -> GWANScoringCase:
        return GWANScoringCase(
            case_id=self.case_id,
            object_id=self.object_id,
            description=self.description,
            display_category=self.display_category,
            confidence_label=self.confidence_label,
            data_classification=self.data_classification,
            scoring_inputs=self.scoring_inputs,
            uncertainty_type=self.uncertainty_type,
            expected_action=RecommendedAction.WAIT,
            expected_alert="none",
        )


class IntegratedSimulationObjectDecision(ContractBaseModel):
    simulated_object: SimulatedGWANObject
    decision: GWANScoringDecision


class IntegratedSimulationResult(ContractBaseModel):
    payload: GWANInterfacePayload
    object_decisions: list[IntegratedSimulationObjectDecision]


def default_simulated_objects() -> list[SimulatedGWANObject]:
    """Return deterministic objects for the first integrated simulation."""

    return [
        SimulatedGWANObject(
            case_id="sim-case-001-resource-probe",
            object_id="candidate-resource-stable-001",
            object_name="Stable hydrated resource candidate",
            object_type="small_body_candidate",
            description="High-value resource candidate with low risk and low uncertainty.",
            position=Position3D(x_au=0.10, y_au=-0.03, z_au=0.02),
            distance_au=0.106,
            velocity_context="slow_relative_motion",
            display_category=DisplayCategory.RESOURCE_CANDIDATE,
            visual_marker_type=VisualMarkerType.PIN,
            confidence_label=ConfidenceLabel.LIKELY,
            data_classification=DataClassification.ESTIMATED,
            marker_color_group="resource",
            marker_outline="candidate",
            marker_pattern="solid",
            scoring_inputs=ScoringInputs(
                energy_score=0.42,
                resource_score=0.82,
                risk_score=0.21,
                exploration_value_score=0.78,
                uncertainty_score=0.24,
            ),
            spectrum_summary="Synthetic hydrated-material clue is stable enough for micro-probe consideration.",
            interpretation_summary="GWAN scores this as the strongest low-risk resource candidate in the current regional scan.",
            follow_up_observation="Prepare micro-probe plan and run one final route-risk check.",
            provenance_source_id="sim-resource-obs-001",
        ),
        SimulatedGWANObject(
            case_id="sim-case-002-risk-zone",
            object_id="risk-radiation-critical-001",
            object_name="Critical elevated radiation region",
            object_type="radiation_region",
            description="Dangerous region with high risk score.",
            position=Position3D(x_au=-0.09, y_au=0.07, z_au=-0.01),
            distance_au=0.115,
            velocity_context="region_intersects_possible_route",
            display_category=DisplayCategory.RISK_ZONE,
            visual_marker_type=VisualMarkerType.WARNING_ZONE,
            confidence_label=ConfidenceLabel.LIKELY,
            data_classification=DataClassification.SIMULATED,
            marker_color_group="risk",
            marker_outline="warning",
            marker_pattern="solid",
            scoring_inputs=ScoringInputs(
                energy_score=0.05,
                resource_score=0.04,
                risk_score=0.91,
                exploration_value_score=0.18,
                uncertainty_score=0.29,
            ),
            interpretation_summary="GWAN marks this area as avoid-first because survival risk overwhelms mission value.",
            follow_up_observation="Recalculate route boundary and keep this region out of micro-probe path planning.",
            provenance_source_id="sim-radiation-risk-001",
        ),
        SimulatedGWANObject(
            case_id="sim-case-003-weak-ice",
            object_id="candidate-ice-weak-signal-001",
            object_name="Weak icy small-body candidate",
            object_type="small_body_candidate",
            description="Possible icy target, but spectral signal is weak and uncertainty is high.",
            position=Position3D(x_au=0.13, y_au=-0.06, z_au=0.03),
            distance_au=0.146,
            velocity_context="slow_relative_motion",
            display_category=DisplayCategory.RESOURCE_CANDIDATE,
            visual_marker_type=VisualMarkerType.PIN,
            confidence_label=ConfidenceLabel.UNCERTAIN,
            data_classification=DataClassification.HYPOTHESIS,
            marker_color_group="resource",
            marker_outline="attention",
            marker_pattern="dashed",
            scoring_inputs=ScoringInputs(
                energy_score=0.31,
                resource_score=0.68,
                risk_score=0.27,
                exploration_value_score=0.74,
                uncertainty_score=0.72,
            ),
            uncertainty_type=UncertaintyType.WEAK_SIGNAL,
            spectrum_summary="Weak absorption-like feature near a synthetic water/ice-related band.",
            interpretation_summary="The candidate may matter, but GWAN avoids overclaiming because evidence is weak.",
            uncertainty_reason="The spectral signal is present but too weak for confirmation.",
            follow_up_observation="Repeat spectral observation with higher signal quality before micro-probe decision.",
            provenance_source_id="sim-spectral-obs-044",
        ),
        SimulatedGWANObject(
            case_id="sim-case-004-nav-ref",
            object_id="nav-reference-stable-001",
            object_name="Stable navigation reference source",
            object_type="stellar_navigation_reference",
            description="Known navigation reference with low uncertainty.",
            position=Position3D(x_au=0.32, y_au=0.11, z_au=0.04),
            distance_au=0.341,
            velocity_context="stable_reference",
            display_category=DisplayCategory.NAVIGATION_REFERENCE,
            visual_marker_type=VisualMarkerType.PIN,
            confidence_label=ConfidenceLabel.CONFIRMED,
            data_classification=DataClassification.KNOWN,
            marker_color_group="navigation",
            marker_outline="normal",
            marker_pattern="solid",
            scoring_inputs=ScoringInputs(
                energy_score=0.10,
                resource_score=0.02,
                risk_score=0.08,
                exploration_value_score=0.35,
                uncertainty_score=0.05,
            ),
            interpretation_summary="This object is useful as a stable reference for map update and positional context.",
            follow_up_observation="Refresh survival map reference alignment.",
            provenance_source_id="synthetic-nav-reference-001",
        ),
    ]


def _alert_severity(level: str) -> AlertSeverity:
    mapping = {
        "info": AlertSeverity.INFO,
        "low": AlertSeverity.LOW,
        "medium": AlertSeverity.MEDIUM,
        "high": AlertSeverity.HIGH,
        "critical": AlertSeverity.CRITICAL,
    }
    return mapping[level]


def _alert_category(action: RecommendedAction) -> AlertCategory:
    if action == RecommendedAction.AVOID:
        return AlertCategory.RISK
    if action in {RecommendedAction.OBSERVE_MORE, RecommendedAction.REQUEST_ADDITIONAL_SPECTRAL_OBSERVATION}:
        return AlertCategory.UNCERTAINTY
    if action == RecommendedAction.UPDATE_SURVIVAL_MAP:
        return AlertCategory.MAP_UPDATE
    return AlertCategory.OBSERVATION_REQUEST


def _alert_message(obj: SimulatedGWANObject, decision: GWANScoringDecision) -> str:
    return f"{obj.object_name}: {decision.recommended_action.value}. {decision.reason_summary}"


def _priority_from_alert(level: str, decision: GWANScoringDecision) -> float:
    base = {"info": 0.30, "low": 0.45, "medium": 0.65, "high": 0.82, "critical": 0.95}[level]
    return min(1.0, round(base + 0.03 * decision.scores.survival_priority_score, 2))


def _spatial_object(obj: SimulatedGWANObject, decision: GWANScoringDecision) -> SpatialObject:
    return SpatialObject(
        object_id=obj.object_id,
        object_name=obj.object_name,
        object_type=obj.object_type,
        relative_position_3d=obj.position,
        distance_au=obj.distance_au,
        velocity_context=obj.velocity_context,
        display_category=obj.display_category,
        visual_marker_type=obj.visual_marker_type,
        marker_style=MarkerStyle(
            color_group=obj.marker_color_group,
            outline=obj.marker_outline,
            pattern=obj.marker_pattern,
            number_badge=decision.scores.survival_priority_score,
            label=decision.recommended_action.value,
        ),
        confidence_label=obj.confidence_label,
        data_classification=obj.data_classification,
        uncertainty_score=decision.scores.uncertainty_score,
        recommended_action=decision.recommended_action,
    )


def _select_sidebar_target(pairs: list[IntegratedSimulationObjectDecision]) -> IntegratedSimulationObjectDecision:
    """Pick the most useful non-risk object for focused sidebar reasoning."""

    candidates = [pair for pair in pairs if pair.simulated_object.display_category != DisplayCategory.RISK_ZONE]
    return max(candidates, key=lambda pair: pair.decision.scores.survival_priority_score)


def _uncertainty_reason(obj: SimulatedGWANObject, decision: GWANScoringDecision) -> str:
    if obj.uncertainty_reason:
        return obj.uncertainty_reason
    return f"Uncertainty score is {decision.scores.uncertainty_score:.2f}, so GWAN requires additional confirmation."


def generate_integrated_simulation_result(
    request: GWANSimulationRequest | None = None,
) -> IntegratedSimulationResult:
    request = request or GWANSimulationRequest()
    now = datetime.now(UTC)

    pairs = [
        IntegratedSimulationObjectDecision(
            simulated_object=obj,
            decision=recommend_action(obj.to_scoring_case()),
        )
        for obj in default_simulated_objects()
    ]

    spatial_package = SpatialVisualizationPackage(
        package_id="spatial-pkg-integrated-sim-001",
        range_scale=RangeScale.REGIONAL_0_01_TO_1_AU,
        reference_radius_au=0.5,
        objects=[_spatial_object(pair.simulated_object, pair.decision) for pair in pairs],
    )

    selected_pair = _select_sidebar_target(pairs)
    selected_obj = selected_pair.simulated_object
    selected_decision = selected_pair.decision
    provenance = [
        ProvenanceRecord(
            source_type="integrated_simulation",
            source_id=selected_obj.provenance_source_id,
            data_classification=selected_obj.data_classification,
        )
    ]

    sidebar_package = SidebarIntelligencePackage(
        package_id="sidebar-pkg-integrated-sim-001",
        selected_object_id=selected_obj.object_id,
        headline=f"{selected_obj.object_name}: {selected_decision.recommended_action.value}",
        summary=selected_decision.reason_summary,
        scores=selected_decision.scores,
        spectrum_summary=selected_obj.spectrum_summary,
        interpretation_summary=selected_obj.interpretation_summary,
        data_classification=selected_obj.data_classification,
        provenance=provenance,
        uncertainty_reason=selected_obj.uncertainty_reason,
        recommended_action=selected_decision.recommended_action,
        required_follow_up_observation=selected_obj.follow_up_observation,
    )

    alerts: list[AlertItem] = []
    for pair in pairs:
        level = pair.decision.alert_level
        if level == "none":
            continue
        obj = pair.simulated_object
        decision = pair.decision
        alerts.append(
            AlertItem(
                alert_id=f"alert-{obj.object_id}",
                object_id=obj.object_id,
                severity=_alert_severity(level),
                category=_alert_category(decision.recommended_action),
                message=_alert_message(obj, decision),
                recommended_operator_response=obj.follow_up_observation or decision.reason_summary,
                priority_score=_priority_from_alert(level, decision),
                created_at=now,
            )
        )

    alert_package = AlertFeedPackage(package_id="alert-pkg-integrated-sim-001", alerts=alerts)

    uncertainty_records: list[UncertaintyRecord] = []
    for pair in pairs:
        obj = pair.simulated_object
        decision = pair.decision
        if not decision.needs_uncertainty_record:
            continue
        uncertainty_records.append(
            UncertaintyRecord(
                uncertainty_id=f"unc-{obj.object_id}",
                object_id=obj.object_id,
                uncertainty_type=obj.uncertainty_type or UncertaintyType.SIMULATED_ONLY,
                uncertainty_reason=_uncertainty_reason(obj, decision),
                impact_on_decision=decision.reason_summary,
                suggested_resolution=obj.follow_up_observation or "Collect additional observation before committing action.",
                confidence_label=obj.confidence_label,
            )
        )

    uncertainty_package = UncertaintyPackage(
        package_id="uncertainty-pkg-integrated-sim-001",
        items=uncertainty_records,
    )

    report_package = DecisionReportPackage(
        package_id="report-pkg-integrated-sim-001",
        report_id="decision-report-integrated-sim-001",
        object_id=selected_obj.object_id,
        decision_summary=f"GWAN recommends {selected_decision.recommended_action.value} for {selected_obj.object_name}.",
        reasoning_steps=[
            "GWAN generated deterministic simulated objects for the regional scan.",
            "Each simulated object was converted into a GWANScoringCase.",
            "The shared scoring rule produced scores, alert level, and recommended action.",
            f"The selected sidebar target is {selected_obj.object_id} because it has the strongest non-risk survival priority.",
            selected_decision.reason_summary,
        ],
        recommended_action=selected_decision.recommended_action,
        memory_update=MemoryUpdate(
            store_as="integrated_simulation_candidate_set",
            update_survival_map=True,
            notes="Store scoring-linked payload generation result for regression testing.",
        ),
        provenance=provenance,
    )

    payload = GWANInterfacePayload(
        generated_at=now,
        mission_context=MissionContext(
            mission_id=request.mission_id,
            observer=request.observer,
            operator_intent=request.operator_intent,
            mission_phase=request.mission_phase,
            priority_context=request.priority_context,
        ),
        coordinate_reference=CoordinateReference(origin="spacecraft", frame="spacecraft_relative_cartesian", unit="AU"),
        packages=GWANOutputPackages(
            spatial_visualization_package=spatial_package,
            sidebar_intelligence_package=sidebar_package,
            alert_feed_package=alert_package,
            uncertainty_package=uncertainty_package,
            decision_report_package=report_package,
        ),
    )

    return IntegratedSimulationResult(payload=payload, object_decisions=pairs)


def generate_first_simulation_payload(request: GWANSimulationRequest | None = None) -> GWANInterfacePayload:
    """Backward-compatible helper returning only the interface payload."""

    return generate_integrated_simulation_result(request).payload


class StrictPreventionReading(PreventionReading):
    """요청 전용 strict 거울 (D6 '문 전체 엄격').

    config 만 extra=forbid 로 덮어쓴다 — 필드·검증 로직은 전부 상속(복제 없음).
    원본 PreventionReading 은 내부 유연성을 위해 무수정 유지.
    """

    model_config = ConfigDict(extra="forbid")


class StrictPreventionInput(PreventionInput):
    """요청 전용 strict 거울 (D6). 외부 문에서 오타 필드가 조용히 무시되는 착시를 차단한다."""

    model_config = ConfigDict(extra="forbid")
    readings: list[StrictPreventionReading] = Field(..., min_length=1)


class SimulationWithPreventionRequest(ContractBaseModel):
    """POST /gwan/simulate-with-prevention 요청 봉투 (extra=forbid — ContractBaseModel 상속)."""

    prevention_input: StrictPreventionInput
    request: GWANSimulationRequest | None = None


def generate_simulation_with_prevention(
    prevention_input: PreventionInput,
    request: GWANSimulationRequest | None = None,
) -> IntegratedSimulationResult:
    """중간 연결(H4): 기존 빌더 위에 예방 평가를 얇게 얹어 payload.prevention 을 채운다.

    기존 빌더(generate_integrated_simulation_result)는 '호출'만 하고 수정하지 않는다.
    prevention_input 은 호출자가 명시 제공(길 A, 데이터 날조 0). severity_context 는 그 값을 그대로 쓴다
    (자동 동기화·교차검증 없음). 행동 게이트도 만들지 않는다(SPEC 부록 M0~M2).
    """
    result = generate_integrated_simulation_result(request)  # 기존 빌더 무수정, 호출만
    report = to_prevention_report(assess_prevention(prevention_input))
    enriched_payload = result.payload.model_copy(update={"prevention": report})
    return result.model_copy(update={"payload": enriched_payload})
