import pytest
from pydantic import ValidationError

from app.schemas.gwan_interface import RecommendedAction
from app.services.gwan_judgment import (
    GWANJudgmentInput,
    calculate_gwan_judgment,
)


def test_high_radiation_blocks_exploration():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.70,
            velocity_risk=0.60,
            radiation_risk=0.95,
            resource_signal=0.90,
            spectral_confidence=0.80,
            trajectory_uncertainty=0.40,
            energy_level=0.70,
            recovery_capacity=0.40,
        )
    )

    assert result.recommended_action == RecommendedAction.AVOID
    assert result.blocked_by_safety_gate is True
    assert result.requires_human_review is True
    assert "HIGH_RADIATION" in result.reason_codes


def test_high_uncertainty_recommends_observe_more():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.20,
            velocity_risk=0.20,
            radiation_risk=0.20,
            resource_signal=0.65,
            spectral_confidence=0.20,
            trajectory_uncertainty=0.85,
            energy_level=0.60,
            recovery_capacity=0.70,
        )
    )

    assert result.recommended_action == RecommendedAction.OBSERVE_MORE
    assert result.requires_human_review is True
    assert "HIGH_UNCERTAINTY" in result.reason_codes
    assert "LOW_SPECTRAL_CONFIDENCE" in result.reason_codes


def test_safe_high_resource_candidate_sends_micro_probe():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.10,
            velocity_risk=0.15,
            radiation_risk=0.10,
            resource_signal=0.90,
            spectral_confidence=0.85,
            trajectory_uncertainty=0.15,
            energy_level=0.80,
            recovery_capacity=0.80,
        )
    )

    assert result.recommended_action == RecommendedAction.SEND_MICRO_PROBE
    assert result.blocked_by_safety_gate is False
    assert result.requires_human_review is False
    assert "HIGH_RESOURCE_SIGNAL" in result.reason_codes
    assert "HIGH_EXPLORATION_VALUE" in result.reason_codes


def test_moderate_exploration_candidate_recommends_approach():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.25,
            velocity_risk=0.25,
            radiation_risk=0.20,
            resource_signal=0.66,
            spectral_confidence=0.72,
            trajectory_uncertainty=0.32,
            energy_level=0.70,
            recovery_capacity=0.70,
        )
    )

    assert result.recommended_action in {
        RecommendedAction.APPROACH,
        RecommendedAction.SEND_MICRO_PROBE,
        RecommendedAction.MARK_AS_LONG_TERM_CANDIDATE,
    }
    assert result.blocked_by_safety_gate is False


def test_low_signal_waits_or_marks_long_term_candidate():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.30,
            velocity_risk=0.30,
            radiation_risk=0.25,
            resource_signal=0.20,
            spectral_confidence=0.50,
            trajectory_uncertainty=0.40,
            energy_level=0.45,
            recovery_capacity=0.50,
        )
    )

    assert result.recommended_action in {
        RecommendedAction.WAIT,
        RecommendedAction.MARK_AS_LONG_TERM_CANDIDATE,
    }
    assert result.blocked_by_safety_gate is False


def test_input_rejects_out_of_range_values():
    with pytest.raises(ValidationError):
        GWANJudgmentInput(
            distance_risk=1.20,
            velocity_risk=0.30,
            radiation_risk=0.20,
            resource_signal=0.40,
            spectral_confidence=0.50,
            trajectory_uncertainty=0.30,
            energy_level=0.60,
            recovery_capacity=0.70,
        )


def test_result_contains_explainable_reason_summary():
    result = calculate_gwan_judgment(
        GWANJudgmentInput(
            distance_risk=0.10,
            velocity_risk=0.10,
            radiation_risk=0.10,
            resource_signal=0.85,
            spectral_confidence=0.80,
            trajectory_uncertainty=0.20,
            energy_level=0.75,
            recovery_capacity=0.75,
        )
    )

    assert result.reason_summary
    assert isinstance(result.reason_codes, list)
    assert 0 <= result.risk_score <= 1
    assert 0 <= result.uncertainty_score <= 1
