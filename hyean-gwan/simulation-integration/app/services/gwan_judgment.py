"""Safety-first GWAN Judgment Model v0.1.

This module is not a deep learning model.

It is a transparent rule-based judgment layer for HYEAN/GWAN.
The goal is to make early GWAN decisions safe, testable, and explainable.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.gwan_interface import ContractBaseModel, RecommendedAction


JudgmentConfidence = Literal["high", "medium", "low"]
JudgmentSeverity = Literal["normal", "watch", "adjust", "restrict", "abort"]


class GWANJudgmentInput(ContractBaseModel):
    """Input signals for GWAN Judgment Model v0.1.

    Every value uses a 0.0 to 1.0 scale.

    Higher distance_risk, velocity_risk, radiation_risk, and uncertainty mean danger.
    Higher resource_signal, spectral_confidence, energy_level, and recovery_capacity mean opportunity or resilience.
    """

    distance_risk: float = Field(..., ge=0, le=1)
    velocity_risk: float = Field(..., ge=0, le=1)
    radiation_risk: float = Field(..., ge=0, le=1)
    resource_signal: float = Field(..., ge=0, le=1)
    spectral_confidence: float = Field(..., ge=0, le=1)
    trajectory_uncertainty: float = Field(..., ge=0, le=1)
    energy_level: float = Field(..., ge=0, le=1)
    recovery_capacity: float = Field(..., ge=0, le=1)


class GWANJudgmentResult(ContractBaseModel):
    """Explainable result from GWAN Judgment Model v0.1."""

    risk_score: float = Field(..., ge=0, le=1)
    resource_score: float = Field(..., ge=0, le=1)
    exploration_score: float = Field(..., ge=0, le=1)
    uncertainty_score: float = Field(..., ge=0, le=1)
    survival_priority_score: float = Field(..., ge=0, le=1)
    recommended_action: RecommendedAction
    severity: JudgmentSeverity
    confidence: JudgmentConfidence
    blocked_by_safety_gate: bool
    requires_human_review: bool
    reason_codes: list[str]
    reason_summary: str


def _clamp_score(value: float) -> float:
    return max(0.0, min(1.0, round(value, 2)))


def calculate_risk_score(data: GWANJudgmentInput) -> float:
    """Calculate risk score from distance, velocity, radiation, and uncertainty."""

    return _clamp_score(
        0.25 * data.distance_risk
        + 0.25 * data.velocity_risk
        + 0.35 * data.radiation_risk
        + 0.15 * data.trajectory_uncertainty
    )


def calculate_resource_score(data: GWANJudgmentInput) -> float:
    """Calculate resource score from resource signal and spectral confidence."""

    return _clamp_score(
        0.70 * data.resource_signal
        + 0.30 * data.spectral_confidence
    )


def calculate_exploration_score(data: GWANJudgmentInput) -> float:
    """Calculate exploration score.

    Exploration becomes less attractive when risk and uncertainty are high.
    """

    return _clamp_score(
        0.45 * data.resource_signal
        + 0.30 * data.spectral_confidence
        + 0.25 * data.energy_level
        - 0.20 * data.trajectory_uncertainty
    )


def calculate_uncertainty_score(data: GWANJudgmentInput) -> float:
    """Calculate uncertainty score.

    Low spectral confidence increases uncertainty.
    """

    return _clamp_score(
        0.60 * data.trajectory_uncertainty
        + 0.40 * (1.0 - data.spectral_confidence)
    )


def calculate_survival_priority_score(
    risk_score: float,
    resource_score: float,
    exploration_score: float,
    uncertainty_score: float,
    data: GWANJudgmentInput,
) -> float:
    """Calculate survival priority score.

    This score rewards resource value and recovery capacity,
    but penalizes risk and uncertainty.
    """

    return _clamp_score(
        0.25 * resource_score
        + 0.20 * exploration_score
        + 0.25 * data.energy_level
        + 0.20 * data.recovery_capacity
        - 0.25 * risk_score
        - 0.15 * uncertainty_score
        + 0.20
    )


def calculate_gwan_judgment(data: GWANJudgmentInput) -> GWANJudgmentResult:
    """Calculate the first safety-first GWAN judgment."""

    risk_score = calculate_risk_score(data)
    resource_score = calculate_resource_score(data)
    exploration_score = calculate_exploration_score(data)
    uncertainty_score = calculate_uncertainty_score(data)
    survival_priority_score = calculate_survival_priority_score(
        risk_score=risk_score,
        resource_score=resource_score,
        exploration_score=exploration_score,
        uncertainty_score=uncertainty_score,
        data=data,
    )

    reason_codes: list[str] = []

    if risk_score >= 0.80:
        reason_codes.append("HIGH_RISK")
    if uncertainty_score >= 0.65:
        reason_codes.append("HIGH_UNCERTAINTY")
    if data.radiation_risk >= 0.80:
        reason_codes.append("HIGH_RADIATION")
    if data.recovery_capacity <= 0.30:
        reason_codes.append("LOW_RECOVERY_CAPACITY")
    if resource_score >= 0.70:
        reason_codes.append("HIGH_RESOURCE_SIGNAL")
    if exploration_score >= 0.65:
        reason_codes.append("HIGH_EXPLORATION_VALUE")
    if data.spectral_confidence <= 0.35:
        reason_codes.append("LOW_SPECTRAL_CONFIDENCE")

    blocked_by_safety_gate = False
    requires_human_review = False

    if risk_score >= 0.90 or data.radiation_risk >= 0.90:
        recommended_action = RecommendedAction.AVOID
        severity: JudgmentSeverity = "abort"
        confidence: JudgmentConfidence = "high"
        blocked_by_safety_gate = True
        requires_human_review = True
        reason_summary = "Critical risk detected. GWAN blocks exploration and recommends avoid."
    elif risk_score >= 0.80 and uncertainty_score >= 0.50:
        recommended_action = RecommendedAction.AVOID
        severity = "restrict"
        confidence = "high"
        blocked_by_safety_gate = True
        requires_human_review = True
        reason_summary = "Risk and uncertainty are both high. Safety gate blocks action."
    elif uncertainty_score >= 0.65:
        recommended_action = RecommendedAction.OBSERVE_MORE
        severity = "watch"
        confidence = "medium"
        requires_human_review = True
        reason_summary = "Uncertainty is too high. GWAN requests more observation before action."
    elif (
        resource_score >= 0.70
        and exploration_score >= 0.65
        and risk_score <= 0.35
        and uncertainty_score <= 0.35
    ):
        recommended_action = RecommendedAction.SEND_MICRO_PROBE
        severity = "normal"
        confidence = "high"
        reason_summary = "Resource and exploration value are high while risk and uncertainty are low."
    elif exploration_score >= 0.60 and risk_score <= 0.55:
        recommended_action = RecommendedAction.APPROACH
        severity = "adjust"
        confidence = "medium"
        reason_summary = "Exploration value is meaningful, but approach should remain cautious."
    elif survival_priority_score >= 0.55:
        recommended_action = RecommendedAction.MARK_AS_LONG_TERM_CANDIDATE
        severity = "watch"
        confidence = "medium"
        reason_summary = "Survival priority is meaningful, but immediate action is not justified."
    else:
        recommended_action = RecommendedAction.WAIT
        severity = "normal"
        confidence = "low"
        reason_summary = "Current signals do not justify immediate action."

    return GWANJudgmentResult(
        risk_score=risk_score,
        resource_score=resource_score,
        exploration_score=exploration_score,
        uncertainty_score=uncertainty_score,
        survival_priority_score=survival_priority_score,
        recommended_action=recommended_action,
        severity=severity,
        confidence=confidence,
        blocked_by_safety_gate=blocked_by_safety_gate,
        requires_human_review=requires_human_review,
        reason_codes=reason_codes,
        reason_summary=reason_summary,
    )
