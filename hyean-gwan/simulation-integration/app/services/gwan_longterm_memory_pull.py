"""Long-term memory pull and proactive recommendation for onboard GWAN.

18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation

This module adds the reverse direction of the Sync Layer:

PostgreSQL long-term memory
-> manual operator pull
-> proactive AI recommendation
-> onboard knowledge package

It does not implement real spacecraft networking or background scheduling yet.
It creates the first API-level model for bringing useful long-term memory back
to the onboard GWAN Core when it helps HYEAN's survival, exploration, risk, or
uncertainty handling goals.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from app.schemas.gwan_interface import ContractBaseModel, DisplayCategory, RecommendedAction
from app.services.gwan_memory_query import MemoryQueryMatch, MemoryQueryRequest
from app.services.gwan_memory_postgres_query import query_database_memory_snapshots


class MemoryPullMode(str, Enum):
    """How long-term memory should be pulled back to onboard GWAN."""

    MANUAL = "manual"
    PROACTIVE = "proactive"


class MemoryPullQueryType(str, Enum):
    """Operator-facing manual pull intent."""

    OBJECT_HISTORY = "object_history"
    HIGH_RISK = "high_risk"
    HIGH_UNCERTAINTY = "high_uncertainty"
    RECOMMENDED_ACTION = "recommended_action"
    RESOURCE_CANDIDATES = "resource_candidates"
    MAP_LAYER = "map_layer"
    GENERAL = "general"


class RecommendationFrequency(str, Enum):
    """How often HYEAN should proactively recommend long-term memory."""

    MANUAL_ONLY = "manual_only"
    LOW_FREQUENCY = "low_frequency"
    NORMAL = "normal"
    HIGH_FREQUENCY = "high_frequency"
    CRITICAL_ONLY = "critical_only"


class RecommendationTrigger(str, Enum):
    """Events that can justify proactive memory recommendation."""

    ON_ROUTE_CHANGE = "on_route_change"
    ON_NEW_DETECTION = "on_new_detection"
    ON_HIGH_RISK = "on_high_risk"
    ON_HIGH_UNCERTAINTY = "on_high_uncertainty"
    ON_OPERATOR_IDLE = "on_operator_idle"
    ON_PERIODIC_REVIEW = "on_periodic_review"


class LongTermMemoryPullRequest(ContractBaseModel):
    """Manual pull request from onboard operator or UI.

    Examples:
    - pull object history for a selected candidate
    - pull high-risk records before route planning
    - pull previous send_micro_probe candidates
    """

    query_type: MemoryPullQueryType = MemoryPullQueryType.GENERAL
    object_id: str | None = None
    recommended_action: RecommendedAction | None = None
    display_category: DisplayCategory | None = None
    map_layer: str | None = None
    min_risk_score: float | None = Field(default=None, ge=0, le=1)
    min_uncertainty_score: float | None = Field(default=None, ge=0, le=1)
    limit: int = Field(default=5, ge=1, le=50)

    @model_validator(mode="after")
    def fill_defaults_by_query_type(self) -> Self:
        if self.query_type == MemoryPullQueryType.HIGH_RISK and self.min_risk_score is None:
            self.min_risk_score = 0.75
        if self.query_type == MemoryPullQueryType.HIGH_UNCERTAINTY and self.min_uncertainty_score is None:
            self.min_uncertainty_score = 0.60
        if self.query_type == MemoryPullQueryType.RESOURCE_CANDIDATES and self.display_category is None:
            self.display_category = DisplayCategory.RESOURCE_CANDIDATE
        if self.query_type == MemoryPullQueryType.RECOMMENDED_ACTION and self.recommended_action is None:
            raise ValueError("recommended_action query requires recommended_action.")
        if self.query_type == MemoryPullQueryType.OBJECT_HISTORY and not self.object_id:
            raise ValueError("object_history query requires object_id.")
        if self.query_type == MemoryPullQueryType.MAP_LAYER and not self.map_layer:
            raise ValueError("map_layer query requires map_layer.")
        return self


class RecommendationSettings(ContractBaseModel):
    """Operator-configurable proactive recommendation settings."""

    frequency: RecommendationFrequency = RecommendationFrequency.NORMAL
    enabled_triggers: list[RecommendationTrigger] = Field(
        default_factory=lambda: [
            RecommendationTrigger.ON_ROUTE_CHANGE,
            RecommendationTrigger.ON_HIGH_RISK,
            RecommendationTrigger.ON_HIGH_UNCERTAINTY,
        ]
    )
    max_recommendations_per_cycle: int = Field(default=3, ge=1, le=20)
    min_relevance_score: float = Field(default=0.55, ge=0, le=1)
    include_low_confidence: bool = True


class LongTermMemoryRecommendationRequest(ContractBaseModel):
    """Context used by GWAN to recommend useful long-term memory.

    This is not a final route planner. It is a first context model for deciding
    what long-term memory may help onboard GWAN now.
    """

    current_object_id: str | None = None
    predicted_route_object_ids: list[str] = Field(default_factory=list)
    operator_intent: str = Field(default="survival_navigation")
    current_risk_score: float | None = Field(default=None, ge=0, le=1)
    current_uncertainty_score: float | None = Field(default=None, ge=0, le=1)
    frequency: RecommendationFrequency | None = None
    triggers: list[RecommendationTrigger] = Field(default_factory=list)
    limit: int = Field(default=5, ge=1, le=50)


class OnboardKnowledgeItem(ContractBaseModel):
    """One long-term memory item packaged for onboard use."""

    object_id: str
    object_name: str | None = None
    object_type: str
    display_category: DisplayCategory
    recommended_action: RecommendedAction
    risk_score: float = Field(..., ge=0, le=1)
    uncertainty_score: float = Field(..., ge=0, le=1)
    survival_priority_score: float = Field(..., ge=0, le=1)
    map_layer: str | None = None
    relevance_score: float = Field(..., ge=0, le=1)
    reason_for_onboard: str
    source_snapshot_id: str
    mission_id: str
    uncertainty_reason: str | None = None
    map_update_summary: str | None = None


class OnboardKnowledgePackage(ContractBaseModel):
    """Payload sent from long-term memory back to onboard GWAN."""

    package_id: str
    mode: MemoryPullMode
    generated_at: datetime
    settings: RecommendationSettings
    request_summary: str
    total_candidates_considered: int = Field(..., ge=0)
    total_items: int = Field(..., ge=0)
    items: list[OnboardKnowledgeItem]
    operator_message: str


class LongTermMemoryPullResponse(ContractBaseModel):
    """API response for manual or proactive long-term memory pull."""

    package: OnboardKnowledgePackage


_DEFAULT_RECOMMENDATION_SETTINGS = RecommendationSettings()


def get_recommendation_settings() -> RecommendationSettings:
    """Return current in-process recommendation settings.

    This is intentionally simple for the prototype. Later versions can store
    settings in PostgreSQL or onboard configuration files.
    """

    return _DEFAULT_RECOMMENDATION_SETTINGS.model_copy(deep=True)


def update_recommendation_settings(settings: RecommendationSettings) -> RecommendationSettings:
    """Update in-process recommendation settings for the running API process."""

    global _DEFAULT_RECOMMENDATION_SETTINGS
    _DEFAULT_RECOMMENDATION_SETTINGS = settings
    return get_recommendation_settings()


def _pull_request_to_memory_query(request: LongTermMemoryPullRequest) -> MemoryQueryRequest:
    return MemoryQueryRequest(
        object_id=request.object_id,
        map_layer=request.map_layer,
        display_category=request.display_category,
        recommended_action=request.recommended_action,
        min_risk_score=request.min_risk_score,
        min_uncertainty_score=request.min_uncertainty_score,
        limit=request.limit,
    )


def _reason_for_manual_pull(match: MemoryQueryMatch, query_type: MemoryPullQueryType) -> str:
    if query_type == MemoryPullQueryType.OBJECT_HISTORY:
        return "Operator requested history for this object."
    if query_type == MemoryPullQueryType.HIGH_RISK:
        return "Operator requested high-risk long-term memory."
    if query_type == MemoryPullQueryType.HIGH_UNCERTAINTY:
        return "Operator requested high-uncertainty long-term memory."
    if query_type == MemoryPullQueryType.RECOMMENDED_ACTION:
        return f"Operator requested records with action '{match.recommended_action}'."
    if query_type == MemoryPullQueryType.RESOURCE_CANDIDATES:
        return "Operator requested resource candidate memory."
    if query_type == MemoryPullQueryType.MAP_LAYER:
        return f"Operator requested map layer '{match.map_layer}'."
    return "Operator requested general long-term memory."


def _manual_relevance(match: MemoryQueryMatch) -> float:
    """Manual search relevance favors survival priority, risk, and uncertainty."""

    relevance = max(match.survival_priority_score, match.risk_score, match.uncertainty_score)
    if match.recommended_action == RecommendedAction.SEND_MICRO_PROBE:
        relevance += 0.08
    if match.recommended_action == RecommendedAction.AVOID:
        relevance += 0.10
    return max(0.0, min(1.0, round(relevance, 2)))


def _match_to_item(match: MemoryQueryMatch, *, relevance_score: float, reason: str) -> OnboardKnowledgeItem:
    return OnboardKnowledgeItem(
        object_id=match.object_id,
        object_name=match.object_name,
        object_type=match.object_type,
        display_category=match.display_category,
        recommended_action=match.recommended_action,
        risk_score=match.risk_score,
        uncertainty_score=match.uncertainty_score,
        survival_priority_score=match.survival_priority_score,
        map_layer=match.map_layer,
        relevance_score=relevance_score,
        reason_for_onboard=reason,
        source_snapshot_id=match.snapshot_id,
        mission_id=match.mission_id,
        uncertainty_reason=match.uncertainty_reason,
        map_update_summary=match.map_update_summary,
    )


def pull_longterm_memory_for_onboard(
    request: LongTermMemoryPullRequest | None = None,
    *,
    database_url: str | None = None,
) -> LongTermMemoryPullResponse:
    """Manual pull from long-term memory into an onboard knowledge package."""

    request = request or LongTermMemoryPullRequest()
    query = _pull_request_to_memory_query(request)
    result = query_database_memory_snapshots(query, database_url=database_url)
    settings = get_recommendation_settings()

    items = [
        _match_to_item(
            match,
            relevance_score=_manual_relevance(match),
            reason=_reason_for_manual_pull(match, request.query_type),
        )
        for match in result.matches
    ]
    items.sort(key=lambda item: item.relevance_score, reverse=True)

    package = OnboardKnowledgePackage(
        package_id="onboard-manual-pull-001",
        mode=MemoryPullMode.MANUAL,
        generated_at=datetime.now(UTC),
        settings=settings,
        request_summary=f"manual pull query_type={request.query_type}",
        total_candidates_considered=result.total_matches,
        total_items=len(items),
        items=items,
        operator_message="Manual long-term memory pull completed.",
    )
    return LongTermMemoryPullResponse(package=package)


def _recommendation_query_for_context(request: LongTermMemoryRecommendationRequest) -> MemoryQueryRequest:
    """Build a broad but safe DB query from the current onboard context."""

    min_risk = 0.75 if request.current_risk_score and request.current_risk_score >= 0.60 else None
    min_uncertainty = 0.60 if request.current_uncertainty_score and request.current_uncertainty_score >= 0.50 else None
    return MemoryQueryRequest(
        min_risk_score=min_risk,
        min_uncertainty_score=min_uncertainty,
        limit=max(request.limit, 20),
    )


def _context_relevance(match: MemoryQueryMatch, request: LongTermMemoryRecommendationRequest) -> tuple[float, list[str]]:
    """Score how useful one long-term memory record is for the current onboard context."""

    score = 0.0
    reasons: list[str] = []

    if request.current_object_id and match.object_id == request.current_object_id:
        score += 0.45
        reasons.append("same object as current operator focus")

    if match.object_id in request.predicted_route_object_ids:
        score += 0.35
        reasons.append("object appears in predicted route context")

    if match.risk_score >= 0.75:
        score += 0.25
        reasons.append("high-risk memory may affect survival navigation")

    if match.uncertainty_score >= 0.60:
        score += 0.20
        reasons.append("high-uncertainty memory may require additional observation")

    if match.recommended_action == RecommendedAction.SEND_MICRO_PROBE:
        score += 0.18
        reasons.append("past decision suggests micro-probe exploration value")

    if match.recommended_action == RecommendedAction.AVOID:
        score += 0.22
        reasons.append("past decision suggests avoidance relevance")

    if "resource" in request.operator_intent and match.display_category == DisplayCategory.RESOURCE_CANDIDATE:
        score += 0.18
        reasons.append("operator intent is resource-related")

    if "risk" in request.operator_intent and match.risk_score >= 0.60:
        score += 0.18
        reasons.append("operator intent is risk-related")

    if match.survival_priority_score >= 0.60:
        score += 0.12
        reasons.append("high survival priority memory")

    if not reasons:
        reasons.append("general long-term memory context")

    return max(0.0, min(1.0, round(score, 2))), reasons


def _frequency_allows_recommendation(
    settings: RecommendationSettings,
    request: LongTermMemoryRecommendationRequest,
) -> tuple[bool, str]:
    frequency = request.frequency or settings.frequency

    if frequency == RecommendationFrequency.MANUAL_ONLY:
        return False, "Proactive recommendation disabled by manual_only frequency."

    triggers = set(request.triggers or settings.enabled_triggers)
    if frequency == RecommendationFrequency.CRITICAL_ONLY:
        critical_context = (
            (request.current_risk_score is not None and request.current_risk_score >= 0.85)
            or RecommendationTrigger.ON_HIGH_RISK in triggers
        )
        if not critical_context:
            return False, "critical_only mode requires high-risk or critical trigger context."

    if frequency == RecommendationFrequency.LOW_FREQUENCY and not triggers:
        return False, "low_frequency mode requires at least one trigger."

    return True, "Recommendation allowed by frequency settings."


def recommend_longterm_memory_for_onboard(
    request: LongTermMemoryRecommendationRequest | None = None,
    *,
    database_url: str | None = None,
) -> LongTermMemoryPullResponse:
    """Proactively recommend long-term memory useful to onboard GWAN now."""

    request = request or LongTermMemoryRecommendationRequest()
    settings = get_recommendation_settings()
    allowed, message = _frequency_allows_recommendation(settings, request)

    if not allowed:
        package = OnboardKnowledgePackage(
            package_id="onboard-recommendation-001",
            mode=MemoryPullMode.PROACTIVE,
            generated_at=datetime.now(UTC),
            settings=settings,
            request_summary=f"proactive recommendation blocked: {message}",
            total_candidates_considered=0,
            total_items=0,
            items=[],
            operator_message=message,
        )
        return LongTermMemoryPullResponse(package=package)

    query = _recommendation_query_for_context(request)
    db_result = query_database_memory_snapshots(query, database_url=database_url)

    candidates: list[OnboardKnowledgeItem] = []
    threshold = settings.min_relevance_score
    max_items = min(settings.max_recommendations_per_cycle, request.limit)

    for match in db_result.matches:
        relevance, reasons = _context_relevance(match, request)
        if relevance < threshold:
            continue
        candidates.append(
            _match_to_item(
                match,
                relevance_score=relevance,
                reason="; ".join(reasons),
            )
        )

    candidates.sort(key=lambda item: item.relevance_score, reverse=True)
    items = candidates[:max_items]

    package = OnboardKnowledgePackage(
        package_id="onboard-recommendation-001",
        mode=MemoryPullMode.PROACTIVE,
        generated_at=datetime.now(UTC),
        settings=settings,
        request_summary=(
            f"intent={request.operator_intent}; current_object_id={request.current_object_id}; "
            f"route_objects={len(request.predicted_route_object_ids)}"
        ),
        total_candidates_considered=db_result.total_matches,
        total_items=len(items),
        items=items,
        operator_message="Long-term memory recommendation completed.",
    )
    return LongTermMemoryPullResponse(package=package)
