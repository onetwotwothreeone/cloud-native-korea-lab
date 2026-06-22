import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.schemas.gwan_interface import ConfidenceLabel, RecommendedAction
from app.services.gwan_scoring import (
    GWANScoringCase,
    ScoringInputs,
    calculate_survival_priority,
    evaluate_default_scoring_cases,
    load_default_scoring_cases,
    recommend_action,
)


def test_default_scoring_cases_all_pass_expected_actions() -> None:
    results = evaluate_default_scoring_cases()

    assert len(results) == 6
    assert all(result.passed for result in results)


def test_high_risk_case_recommends_avoid() -> None:
    case = next(case for case in load_default_scoring_cases() if case.case_id == "case-002-high-risk-zone")
    decision = recommend_action(case)

    assert decision.recommended_action == RecommendedAction.AVOID
    assert decision.alert_level == "critical"
    assert decision.scores.risk_score >= 0.90


def test_low_risk_high_resource_case_recommends_micro_probe() -> None:
    case = next(case for case in load_default_scoring_cases() if case.case_id == "case-001-low-risk-resource")
    decision = recommend_action(case)

    assert decision.recommended_action == RecommendedAction.SEND_MICRO_PROBE
    assert decision.scores.resource_score >= 0.80
    assert decision.scores.risk_score <= 0.35
    assert decision.scores.uncertainty_score <= 0.35


def test_high_uncertainty_case_requires_observe_more_and_uncertainty_record() -> None:
    case = next(case for case in load_default_scoring_cases() if case.case_id == "case-003-weak-spectral-signal")
    decision = recommend_action(case)

    assert decision.recommended_action == RecommendedAction.OBSERVE_MORE
    assert decision.needs_uncertainty_record is True
    assert case.uncertainty_type is not None


def test_survival_priority_formula_stays_bounded() -> None:
    priority = calculate_survival_priority(
        ScoringInputs(
            energy_score=1.0,
            resource_score=1.0,
            risk_score=0.0,
            exploration_value_score=1.0,
            uncertainty_score=0.0,
        )
    )

    assert 0 <= priority <= 1
    assert priority == 0.95


def test_score_values_outside_zero_to_one_fail_validation() -> None:
    with pytest.raises(ValidationError):
        ScoringInputs(
            energy_score=0.1,
            resource_score=1.25,
            risk_score=0.2,
            exploration_value_score=0.3,
            uncertainty_score=0.4,
        )


def test_uncertain_case_requires_uncertainty_type() -> None:
    with pytest.raises(ValidationError):
        GWANScoringCase(
            case_id="bad-uncertainty-case",
            object_id="candidate-bad-001",
            description="This should fail because uncertainty_type is missing.",
            display_category="resource_candidate",
            confidence_label=ConfidenceLabel.UNCERTAIN,
            data_classification="hypothesis",
            scoring_inputs={
                "energy_score": 0.2,
                "resource_score": 0.7,
                "risk_score": 0.2,
                "exploration_value_score": 0.7,
                "uncertainty_score": 0.8,
            },
            expected_action="observe_more",
            expected_alert="medium",
        )


def test_scoring_cases_fixture_can_be_validated() -> None:
    fixture_path = Path("tests/fixtures/gwan_scoring_cases.json")
    fixture_cases = [GWANScoringCase.model_validate(item) for item in json.loads(fixture_path.read_text())]

    assert [case.case_id for case in fixture_cases] == [
        "case-001-low-risk-resource",
        "case-002-high-risk-zone",
        "case-003-weak-spectral-signal",
        "case-004-navigation-reference",
    ]


def test_score_endpoint_returns_decision_for_one_case() -> None:
    client = TestClient(app)
    case = load_default_scoring_cases()[0]

    response = client.post("/gwan/score", json=case.model_dump(mode="json"))

    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == case.case_id
    assert data["recommended_action"] == "send_micro_probe"


def test_scoring_test_cases_endpoint_returns_all_passed_results() -> None:
    client = TestClient(app)

    response = client.get("/gwan/scoring-test-cases")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    assert all(item["passed"] is True for item in data)
