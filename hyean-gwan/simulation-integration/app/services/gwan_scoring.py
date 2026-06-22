"""Transparent first-pass GWAN scoring rules.

This module is a test harness, not the final science model.
It makes early GWAN behavior explicit and reviewable.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from app.schemas.gwan_interface import (
    ConfidenceLabel,
    ContractBaseModel,
    DataClassification,
    DisplayCategory,
    RecommendedAction,
    Scores,
    UncertaintyType,
)


AlertLevel = Literal["none", "info", "low", "medium", "high", "critical"]


class ScoringInputs(ContractBaseModel):
    energy_score: float = Field(..., ge=0, le=1)
    resource_score: float = Field(..., ge=0, le=1)
    risk_score: float = Field(..., ge=0, le=1)
    exploration_value_score: float = Field(..., ge=0, le=1)
    uncertainty_score: float = Field(..., ge=0, le=1)


class GWANScoringCase(ContractBaseModel):
    case_id: str = Field(..., min_length=1)
    object_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    display_category: DisplayCategory
    confidence_label: ConfidenceLabel
    data_classification: DataClassification
    scoring_inputs: ScoringInputs
    uncertainty_type: UncertaintyType | None = None
    expected_action: RecommendedAction
    expected_alert: AlertLevel = "none"

    @model_validator(mode="after")
    def validate_uncertainty_case_has_uncertainty_type(self) -> Self:
        if self.confidence_label in {
            ConfidenceLabel.UNCERTAIN,
            ConfidenceLabel.LOW_CONFIDENCE,
            ConfidenceLabel.UNKNOWN,
        } and self.uncertainty_type is None:
            raise ValueError("Uncertain scoring cases require uncertainty_type.")
        return self


class GWANScoringDecision(ContractBaseModel):
    case_id: str
    object_id: str
    scores: Scores
    recommended_action: RecommendedAction
    reason_summary: str
    alert_level: AlertLevel
    needs_uncertainty_record: bool


class GWANScoringCaseResult(ContractBaseModel):
    case: GWANScoringCase
    decision: GWANScoringDecision
    passed: bool


def calculate_survival_priority(inputs: ScoringInputs) -> float:
    """Calculate a transparent placeholder survival priority score."""

    raw_score = (
        0.30 * inputs.resource_score
        + 0.25 * inputs.exploration_value_score
        + 0.20 * inputs.energy_score
        - 0.15 * inputs.risk_score
        - 0.10 * inputs.uncertainty_score
        + 0.20
    )
    return max(0.0, min(1.0, round(raw_score, 2)))


def build_scores(inputs: ScoringInputs) -> Scores:
    return Scores(
        energy_score=inputs.energy_score,
        resource_score=inputs.resource_score,
        risk_score=inputs.risk_score,
        exploration_value_score=inputs.exploration_value_score,
        uncertainty_score=inputs.uncertainty_score,
        survival_priority_score=calculate_survival_priority(inputs),
    )


def recommend_action(case: GWANScoringCase) -> GWANScoringDecision:
    scores = build_scores(case.scoring_inputs)
    inputs = case.scoring_inputs
    needs_uncertainty_record = case.confidence_label in {
        ConfidenceLabel.UNCERTAIN,
        ConfidenceLabel.LOW_CONFIDENCE,
        ConfidenceLabel.UNKNOWN,
    } or inputs.uncertainty_score >= 0.60

    if case.display_category == DisplayCategory.NAVIGATION_REFERENCE:
        action = RecommendedAction.UPDATE_SURVIVAL_MAP
        alert_level: AlertLevel = "none"
        reason = "Stable navigation reference should be stored or refreshed in the survival map."
    elif inputs.risk_score >= 0.75:
        action = RecommendedAction.AVOID
        alert_level = "high" if inputs.risk_score < 0.90 else "critical"
        reason = "Risk score is high, so safety takes priority over resource or exploration value."
    elif inputs.uncertainty_score >= 0.65:
        action = RecommendedAction.OBSERVE_MORE
        alert_level = "medium"
        reason = "Uncertainty is too high for commitment; additional observation is required."
    elif (
        inputs.resource_score >= 0.70
        and inputs.exploration_value_score >= 0.65
        and inputs.risk_score <= 0.35
        and inputs.uncertainty_score <= 0.35
    ):
        action = RecommendedAction.SEND_MICRO_PROBE
        alert_level = "info"
        reason = "Resource and exploration value are high while risk and uncertainty are low."
    elif inputs.exploration_value_score >= 0.60 and inputs.risk_score <= 0.50:
        action = RecommendedAction.APPROACH
        alert_level = "low"
        reason = "Exploration value is meaningful and risk is acceptable for approach planning."
    elif scores.survival_priority_score >= 0.55:
        action = RecommendedAction.MARK_AS_LONG_TERM_CANDIDATE
        alert_level = "info"
        reason = "Survival priority is meaningful, but the target is not ready for immediate action."
    else:
        action = RecommendedAction.WAIT
        alert_level = "none"
        reason = "No immediate action is justified by current scores."

    return GWANScoringDecision(
        case_id=case.case_id,
        object_id=case.object_id,
        scores=scores,
        recommended_action=action,
        reason_summary=reason,
        alert_level=alert_level,
        needs_uncertainty_record=needs_uncertainty_record,
    )


def load_default_scoring_cases() -> list[GWANScoringCase]:
    return [
        GWANScoringCase(
            case_id="case-001-low-risk-resource",
            object_id="candidate-resource-stable-001",
            description="High-value resource candidate with low risk and low uncertainty.",
            display_category=DisplayCategory.RESOURCE_CANDIDATE,
            confidence_label=ConfidenceLabel.LIKELY,
            data_classification=DataClassification.ESTIMATED,
            scoring_inputs=ScoringInputs(
                energy_score=0.42,
                resource_score=0.82,
                risk_score=0.21,
                exploration_value_score=0.78,
                uncertainty_score=0.24,
            ),
            expected_action=RecommendedAction.SEND_MICRO_PROBE,
            expected_alert="info",
        ),
        GWANScoringCase(
            case_id="case-002-high-risk-zone",
            object_id="risk-radiation-critical-001",
            description="Dangerous region with high risk score.",
            display_category=DisplayCategory.RISK_ZONE,
            confidence_label=ConfidenceLabel.LIKELY,
            data_classification=DataClassification.SIMULATED,
            scoring_inputs=ScoringInputs(
                energy_score=0.05,
                resource_score=0.04,
                risk_score=0.91,
                exploration_value_score=0.18,
                uncertainty_score=0.29,
            ),
            expected_action=RecommendedAction.AVOID,
            expected_alert="critical",
        ),
        GWANScoringCase(
            case_id="case-003-weak-spectral-signal",
            object_id="candidate-ice-weak-signal-001",
            description="Possible icy target, but spectral signal is weak and uncertainty is high.",
            display_category=DisplayCategory.RESOURCE_CANDIDATE,
            confidence_label=ConfidenceLabel.UNCERTAIN,
            data_classification=DataClassification.HYPOTHESIS,
            scoring_inputs=ScoringInputs(
                energy_score=0.31,
                resource_score=0.68,
                risk_score=0.27,
                exploration_value_score=0.74,
                uncertainty_score=0.72,
            ),
            uncertainty_type=UncertaintyType.WEAK_SIGNAL,
            expected_action=RecommendedAction.OBSERVE_MORE,
            expected_alert="medium",
        ),
        GWANScoringCase(
            case_id="case-004-navigation-reference",
            object_id="nav-reference-stable-001",
            description="Known navigation reference with low uncertainty.",
            display_category=DisplayCategory.NAVIGATION_REFERENCE,
            confidence_label=ConfidenceLabel.CONFIRMED,
            data_classification=DataClassification.KNOWN,
            scoring_inputs=ScoringInputs(
                energy_score=0.10,
                resource_score=0.02,
                risk_score=0.08,
                exploration_value_score=0.35,
                uncertainty_score=0.05,
            ),
            expected_action=RecommendedAction.UPDATE_SURVIVAL_MAP,
            expected_alert="none",
        ),
        GWANScoringCase(
            case_id="case-005-conflicting-observation",
            object_id="candidate-conflicting-obs-001",
            description="Interesting target with conflicting observations that require follow-up.",
            display_category=DisplayCategory.OBSERVATION_TARGET,
            confidence_label=ConfidenceLabel.LOW_CONFIDENCE,
            data_classification=DataClassification.ESTIMATED,
            scoring_inputs=ScoringInputs(
                energy_score=0.36,
                resource_score=0.58,
                risk_score=0.33,
                exploration_value_score=0.69,
                uncertainty_score=0.67,
            ),
            uncertainty_type=UncertaintyType.CONFLICTING_OBSERVATION,
            expected_action=RecommendedAction.OBSERVE_MORE,
            expected_alert="medium",
        ),
        GWANScoringCase(
            case_id="case-006-low-value-wait",
            object_id="candidate-low-value-001",
            description="Low-value object with no immediate operational value.",
            display_category=DisplayCategory.OBSERVATION_TARGET,
            confidence_label=ConfidenceLabel.LIKELY,
            data_classification=DataClassification.SIMULATED,
            scoring_inputs=ScoringInputs(
                energy_score=0.08,
                resource_score=0.10,
                risk_score=0.18,
                exploration_value_score=0.21,
                uncertainty_score=0.22,
            ),
            expected_action=RecommendedAction.WAIT,
            expected_alert="none",
        ),
    ]


def evaluate_default_scoring_cases() -> list[GWANScoringCaseResult]:
    results: list[GWANScoringCaseResult] = []
    for case in load_default_scoring_cases():
        decision = recommend_action(case)
        passed = decision.recommended_action == case.expected_action and decision.alert_level == case.expected_alert
        results.append(GWANScoringCaseResult(case=case, decision=decision, passed=passed))
    return results
