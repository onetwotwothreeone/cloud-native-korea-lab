from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.gwan_interface import (
    AlertFeedPackage,
    AlertItem,
    AlertSeverity,
    ConfidenceLabel,
    CoordinateReference,
    DataClassification,
    DisplayCategory,
    GWANInterfacePayload,
    GWANOutputPackages,
    MarkerStyle,
    MissionContext,
    Position3D,
    RangeScale,
    SpatialObject,
    SpatialVisualizationPackage,
    UncertaintyPackage,
    VisualMarkerType,
)
from app.services.gwan_simulation import generate_first_simulation_payload


def test_integrated_sample_payload_validates() -> None:
    payload = generate_first_simulation_payload()

    assert payload.schema_version == "hyean.gwan.interface.v0.1"
    assert payload.alert_count() >= 3
    assert len(payload.packages.spatial_visualization_package.objects) == 4


def test_position_cannot_mix_au_and_km() -> None:
    with pytest.raises(ValidationError, match="Do not mix AU and km"):
        Position3D(x_au=0.1, y_au=0.2, z_au=0.3, x_km=1, y_km=2, z_km=3)


def test_uncertain_spatial_object_requires_uncertainty_record() -> None:
    obj = SpatialObject(
        object_id="uncertain-object-001",
        object_type="small_body_candidate",
        relative_position_3d=Position3D(x_au=0.1, y_au=0.0, z_au=0.0),
        display_category=DisplayCategory.RESOURCE_CANDIDATE,
        visual_marker_type=VisualMarkerType.PIN,
        marker_style=MarkerStyle(color_group="resource"),
        confidence_label=ConfidenceLabel.UNCERTAIN,
        data_classification=DataClassification.HYPOTHESIS,
        uncertainty_score=0.9,
    )
    spatial = SpatialVisualizationPackage(
        package_id="spatial-test",
        range_scale=RangeScale.REGIONAL_0_01_TO_1_AU,
        reference_radius_au=0.5,
        objects=[obj],
    )

    with pytest.raises(ValidationError, match="Uncertain spatial objects require uncertainty records"):
        GWANInterfacePayload(
            generated_at=datetime.now(UTC),
            mission_context=MissionContext(
                mission_id="test",
                observer="test",
                operator_intent="test",
            ),
            coordinate_reference=CoordinateReference(),
            packages=GWANOutputPackages(
                spatial_visualization_package=spatial,
                uncertainty_package=UncertaintyPackage(package_id="unc-empty", items=[]),
            ),
        )


def test_alerts_can_be_sorted_by_severity_and_priority() -> None:
    now = datetime.now(UTC)
    package = AlertFeedPackage(
        package_id="alerts",
        alerts=[
            AlertItem(
                alert_id="medium",
                severity=AlertSeverity.MEDIUM,
                category="uncertainty",
                message="medium",
                recommended_operator_response="observe",
                priority_score=0.9,
                created_at=now,
            ),
            AlertItem(
                alert_id="critical",
                severity=AlertSeverity.CRITICAL,
                category="risk",
                message="critical",
                recommended_operator_response="avoid",
                priority_score=0.2,
                created_at=now,
            ),
        ],
    )

    assert package.sorted_alerts()[0].alert_id == "critical"
