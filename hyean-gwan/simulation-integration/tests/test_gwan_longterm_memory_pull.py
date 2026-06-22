from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.db.session import create_memory_tables
from app.main import app
from app.services.gwan_longterm_memory_pull import (
    LongTermMemoryPullRequest,
    LongTermMemoryRecommendationRequest,
    MemoryPullQueryType,
    RecommendationFrequency,
    RecommendationSettings,
    RecommendationTrigger,
    get_recommendation_settings,
    pull_longterm_memory_for_onboard,
    recommend_longterm_memory_for_onboard,
    update_recommendation_settings,
)
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_postgres_persistence import persist_memory_snapshot_to_database


def sqlite_url(tmp_path: Path) -> str:
    return f"sqlite+pysqlite:///{tmp_path / 'gwan_longterm_pull_test.db'}"


def seed_database(tmp_path: Path) -> str:
    url = sqlite_url(tmp_path)
    create_memory_tables(url)
    persist_memory_snapshot_to_database(generate_simulated_memory_snapshot(), database_url=url)
    return url


def reset_settings() -> None:
    update_recommendation_settings(RecommendationSettings())


def test_manual_pull_high_risk_returns_onboard_package(tmp_path):
    reset_settings()
    url = seed_database(tmp_path)

    response = pull_longterm_memory_for_onboard(
        LongTermMemoryPullRequest(query_type=MemoryPullQueryType.HIGH_RISK),
        database_url=url,
    )

    assert response.package.mode == "manual"
    assert response.package.total_items == 1
    item = response.package.items[0]
    assert item.object_id == "risk-radiation-critical-001"
    assert item.recommended_action == "avoid"
    assert item.relevance_score >= 0.90
    assert "high-risk" in item.reason_for_onboard


def test_manual_pull_object_history_requires_object_id():
    with pytest.raises(ValidationError):
        LongTermMemoryPullRequest(query_type=MemoryPullQueryType.OBJECT_HISTORY)


def test_manual_pull_recommended_action_finds_micro_probe_candidate(tmp_path):
    reset_settings()
    url = seed_database(tmp_path)

    response = pull_longterm_memory_for_onboard(
        LongTermMemoryPullRequest(
            query_type=MemoryPullQueryType.RECOMMENDED_ACTION,
            recommended_action="send_micro_probe",
        ),
        database_url=url,
    )

    assert response.package.total_items == 1
    assert response.package.items[0].object_id == "candidate-resource-stable-001"


def test_proactive_recommendation_uses_context_and_settings(tmp_path):
    reset_settings()
    url = seed_database(tmp_path)

    request = LongTermMemoryRecommendationRequest(
        operator_intent="resource route planning",
        predicted_route_object_ids=["candidate-resource-stable-001", "risk-radiation-critical-001"],
        triggers=[RecommendationTrigger.ON_ROUTE_CHANGE],
        limit=5,
    )
    response = recommend_longterm_memory_for_onboard(request, database_url=url)

    assert response.package.mode == "proactive"
    assert response.package.total_items >= 2
    object_ids = [item.object_id for item in response.package.items]
    assert "candidate-resource-stable-001" in object_ids
    assert "risk-radiation-critical-001" in object_ids
    assert response.package.items[0].relevance_score >= response.package.items[-1].relevance_score


def test_manual_only_frequency_blocks_proactive_recommendations(tmp_path):
    url = seed_database(tmp_path)
    update_recommendation_settings(RecommendationSettings(frequency=RecommendationFrequency.MANUAL_ONLY))

    response = recommend_longterm_memory_for_onboard(
        LongTermMemoryRecommendationRequest(operator_intent="resource route planning"),
        database_url=url,
    )

    assert response.package.total_items == 0
    assert "manual_only" in response.package.operator_message
    reset_settings()


def test_critical_only_frequency_allows_high_risk_context(tmp_path):
    url = seed_database(tmp_path)
    update_recommendation_settings(
        RecommendationSettings(
            frequency=RecommendationFrequency.CRITICAL_ONLY,
            min_relevance_score=0.50,
        )
    )

    response = recommend_longterm_memory_for_onboard(
        LongTermMemoryRecommendationRequest(
            operator_intent="risk review",
            current_risk_score=0.91,
            triggers=[RecommendationTrigger.ON_HIGH_RISK],
        ),
        database_url=url,
    )

    assert response.package.total_items >= 1
    assert any(item.object_id == "risk-radiation-critical-001" for item in response.package.items)
    reset_settings()


def test_recommendation_settings_can_be_updated():
    new_settings = RecommendationSettings(
        frequency=RecommendationFrequency.LOW_FREQUENCY,
        enabled_triggers=[RecommendationTrigger.ON_HIGH_UNCERTAINTY],
        max_recommendations_per_cycle=2,
        min_relevance_score=0.70,
    )

    updated = update_recommendation_settings(new_settings)

    assert updated.frequency == RecommendationFrequency.LOW_FREQUENCY
    assert updated.max_recommendations_per_cycle == 2
    assert get_recommendation_settings().min_relevance_score == 0.70
    reset_settings()


def test_longterm_memory_pull_api_routes(monkeypatch, tmp_path):
    reset_settings()
    monkeypatch.setenv("DATABASE_URL", sqlite_url(tmp_path))
    client = TestClient(app)

    assert client.post("/gwan/memory/db-create-tables").status_code == 200
    assert client.post("/gwan/memory/db-persist-simulated-snapshot").status_code == 200

    manual_response = client.post(
        "/gwan/sync/pull/manual",
        json={"query_type": "high_risk", "limit": 5},
    )
    assert manual_response.status_code == 200
    assert manual_response.json()["package"]["items"][0]["object_id"] == "risk-radiation-critical-001"

    settings_response = client.post(
        "/gwan/sync/recommendation-settings",
        json={
            "frequency": "normal",
            "enabled_triggers": ["on_route_change", "on_high_risk"],
            "max_recommendations_per_cycle": 3,
            "min_relevance_score": 0.50,
            "include_low_confidence": True,
        },
    )
    assert settings_response.status_code == 200

    recommend_response = client.post(
        "/gwan/sync/recommend",
        json={
            "operator_intent": "resource route planning",
            "predicted_route_object_ids": ["candidate-resource-stable-001", "risk-radiation-critical-001"],
            "triggers": ["on_route_change"],
            "limit": 5,
        },
    )
    assert recommend_response.status_code == 200
    body = recommend_response.json()
    assert body["package"]["total_items"] >= 1
    assert any(item["object_id"] == "candidate-resource-stable-001" for item in body["package"]["items"])
    reset_settings()
