"""FastAPI routes for GWAN payload validation, scoring, and simulation."""

from fastapi import APIRouter

from app.db.session import (
    DatabaseCreateTablesResult,
    DatabaseStatus,
    create_memory_tables,
    get_database_status,
)

from app.services.gwan_memory_postgres_query import (
    query_database_memory_snapshots,
    query_database_object_history,
)
from app.services.gwan_memory_postgres_persistence import (
    MemoryPostgresPersistenceResult,
    MemoryPostgresSnapshotList,
    list_database_memory_snapshots,
    persist_memory_snapshot_to_database,
    persist_simulated_memory_snapshot_to_database,
)


from app.services.gwan_longterm_memory_pull import (
    LongTermMemoryPullRequest,
    LongTermMemoryPullResponse,
    LongTermMemoryRecommendationRequest,
    RecommendationSettings,
    get_recommendation_settings,
    pull_longterm_memory_for_onboard,
    recommend_longterm_memory_for_onboard,
    update_recommendation_settings,
)
from app.services.gwan_memory_sync import (
    MemorySyncRequest,
    MemorySyncResult,
    MemorySyncStatus,
    get_memory_sync_status,
    sync_jsonl_memory_to_database,
)
from app.schemas.gwan_interface import GWANInterfacePayload, RecommendedAction
from app.services.gwan_scoring import (
    GWANScoringCase,
    GWANScoringCaseResult,
    GWANScoringDecision,
    evaluate_default_scoring_cases,
    recommend_action,
)
from app.services.gwan_memory import MemorySnapshot, create_memory_snapshot_from_integrated_result, generate_simulated_memory_snapshot
from app.services.gwan_memory_persistence import (
    MemoryPersistenceResult,
    MemoryPersistenceStatus,
    get_memory_persistence_status,
    list_persisted_memory_snapshots,
    persist_memory_snapshot,
    persist_simulated_memory_snapshot,
)
from app.services.gwan_memory_query import (
    MemoryQueryRequest,
    MemoryQueryResponse,
    query_object_history,
    query_persisted_memory_snapshots,
)
from app.services.gwan_memory_postgres_design import (
    MemoryDatabaseInsertPlan,
    MemoryPostgresDesignResponse,
    generate_simulated_memory_insert_plan,
    get_memory_postgres_design,
)
from app.services.gwan_simulation import (
    GWANSimulationRequest,
    IntegratedSimulationResult,
    generate_first_simulation_payload,
    generate_integrated_simulation_result,
)

router = APIRouter(prefix="/gwan", tags=["gwan"])


@router.post("/interface-payload", response_model=GWANInterfacePayload)
def validate_interface_payload(payload: GWANInterfacePayload) -> GWANInterfacePayload:
    """Validate and echo a GWAN -> HYEAN Operator Interface payload."""

    return payload


@router.post("/simulate", response_model=GWANInterfacePayload)
def simulate_gwan_payload(request: GWANSimulationRequest | None = None) -> GWANInterfacePayload:
    """Generate a scoring-integrated GWAN simulation payload."""

    return generate_first_simulation_payload(request)


@router.post("/simulate-integrated", response_model=IntegratedSimulationResult)
def simulate_gwan_payload_with_decisions(
    request: GWANSimulationRequest | None = None,
) -> IntegratedSimulationResult:
    """Generate payload plus object-level scoring decisions for review and tests."""

    return generate_integrated_simulation_result(request)


@router.post("/score", response_model=GWANScoringDecision)
def score_gwan_case(case: GWANScoringCase) -> GWANScoringDecision:
    """Score one GWAN scenario and return a recommended action."""

    return recommend_action(case)


@router.get("/scoring-test-cases", response_model=list[GWANScoringCaseResult])
def get_scoring_test_cases() -> list[GWANScoringCaseResult]:
    """Return the first official GWAN scoring test-case results."""

    return evaluate_default_scoring_cases()


@router.post("/memory/snapshot", response_model=MemorySnapshot)
def create_memory_snapshot(result: IntegratedSimulationResult) -> MemorySnapshot:
    """Create memory and map update records from an integrated simulation result."""

    return create_memory_snapshot_from_integrated_result(result)


@router.get("/memory/simulated-snapshot", response_model=MemorySnapshot)
def get_simulated_memory_snapshot() -> MemorySnapshot:
    """Generate the default integrated simulation and convert it into memory records."""

    return generate_simulated_memory_snapshot()


@router.post("/memory/persist-snapshot", response_model=MemoryPersistenceResult)
def persist_snapshot(snapshot: MemorySnapshot) -> MemoryPersistenceResult:
    """Persist a provided MemorySnapshot to the JSONL memory log."""

    return persist_memory_snapshot(snapshot)


@router.post("/memory/persist-simulated-snapshot", response_model=MemoryPersistenceResult)
def persist_default_simulated_snapshot() -> MemoryPersistenceResult:
    """Generate the default simulated MemorySnapshot and append it to JSONL."""

    return persist_simulated_memory_snapshot()


@router.get("/memory/persisted-snapshots", response_model=list[MemorySnapshot])
def get_persisted_snapshots() -> list[MemorySnapshot]:
    """Read all persisted MemorySnapshot records from the JSONL memory log."""

    return list_persisted_memory_snapshots()


@router.get("/memory/persistence-status", response_model=MemoryPersistenceStatus)
def get_persistence_status() -> MemoryPersistenceStatus:
    """Return JSONL memory persistence status."""

    return get_memory_persistence_status()


@router.post("/memory/query", response_model=MemoryQueryResponse)
def query_memory(request: MemoryQueryRequest | None = None) -> MemoryQueryResponse:
    """Query persisted GWAN memory snapshots with flexible filters."""

    return query_persisted_memory_snapshots(request)


@router.get("/memory/query/object/{object_id}", response_model=MemoryQueryResponse)
def query_memory_by_object(object_id: str, limit: int = 50) -> MemoryQueryResponse:
    """Return persisted memory records for one object ID."""

    return query_object_history(object_id, limit=limit)


@router.get("/memory/query/high-risk", response_model=MemoryQueryResponse)
def query_high_risk_memory(min_risk_score: float = 0.75, limit: int = 50) -> MemoryQueryResponse:
    """Return persisted memory records with risk score above a threshold."""

    return query_persisted_memory_snapshots(MemoryQueryRequest(min_risk_score=min_risk_score, limit=limit))


@router.get("/memory/query/high-uncertainty", response_model=MemoryQueryResponse)
def query_high_uncertainty_memory(min_uncertainty_score: float = 0.60, limit: int = 50) -> MemoryQueryResponse:
    """Return persisted memory records with uncertainty score above a threshold."""

    return query_persisted_memory_snapshots(
        MemoryQueryRequest(min_uncertainty_score=min_uncertainty_score, limit=limit)
    )


@router.get("/memory/postgres-design", response_model=MemoryPostgresDesignResponse)
def get_postgres_design() -> MemoryPostgresDesignResponse:
    """Return the future PostgreSQL table design for GWAN memory."""

    return get_memory_postgres_design()


@router.get("/memory/postgres-insert-plan", response_model=MemoryDatabaseInsertPlan)
def get_postgres_insert_plan() -> MemoryDatabaseInsertPlan:
    """Return database-ready rows from the default simulated memory snapshot."""

    return generate_simulated_memory_insert_plan()


@router.get("/memory/db-status", response_model=DatabaseStatus)
def get_memory_database_status() -> DatabaseStatus:
    """Check local PostgreSQL/DATABASE_URL connection and GWAN memory tables."""

    return get_database_status()


@router.post("/memory/db-create-tables", response_model=DatabaseCreateTablesResult)
def create_memory_database_tables() -> DatabaseCreateTablesResult:
    """Create GWAN memory tables in the configured database."""

    return create_memory_tables()


@router.post("/memory/db-persist-snapshot", response_model=MemoryPostgresPersistenceResult)
def persist_snapshot_to_database(snapshot: MemorySnapshot) -> MemoryPostgresPersistenceResult:
    """Persist a provided MemorySnapshot into database tables."""

    return persist_memory_snapshot_to_database(snapshot)


@router.post("/memory/db-persist-simulated-snapshot", response_model=MemoryPostgresPersistenceResult)
def persist_simulated_snapshot_to_database() -> MemoryPostgresPersistenceResult:
    """Generate the default simulated MemorySnapshot and persist it to database tables."""

    return persist_simulated_memory_snapshot_to_database()


@router.get("/memory/db-snapshots", response_model=MemoryPostgresSnapshotList)
def list_memory_database_snapshots() -> MemoryPostgresSnapshotList:
    """List MemorySnapshot records persisted in the configured database."""

    return list_database_memory_snapshots()


@router.post("/memory/db-query", response_model=MemoryQueryResponse)
def query_memory_database(request: MemoryQueryRequest | None = None) -> MemoryQueryResponse:
    """Query GWAN memory records directly from database tables."""

    return query_database_memory_snapshots(request)


@router.get("/memory/db-query/object/{object_id}", response_model=MemoryQueryResponse)
def query_memory_database_by_object(object_id: str, limit: int = 50) -> MemoryQueryResponse:
    """Return database memory records for one object ID."""

    return query_database_object_history(object_id, limit=limit)


@router.get("/memory/db-query/high-risk", response_model=MemoryQueryResponse)
def query_high_risk_database_memory(min_risk_score: float = 0.75, limit: int = 50) -> MemoryQueryResponse:
    """Return database memory records with risk score above a threshold."""

    return query_database_memory_snapshots(MemoryQueryRequest(min_risk_score=min_risk_score, limit=limit))


@router.get("/memory/db-query/high-uncertainty", response_model=MemoryQueryResponse)
def query_high_uncertainty_database_memory(
    min_uncertainty_score: float = 0.60,
    limit: int = 50,
) -> MemoryQueryResponse:
    """Return database memory records with uncertainty score above a threshold."""

    return query_database_memory_snapshots(MemoryQueryRequest(min_uncertainty_score=min_uncertainty_score, limit=limit))


@router.get("/memory/db-query/action/{recommended_action}", response_model=MemoryQueryResponse)
def query_memory_database_by_action(recommended_action: RecommendedAction, limit: int = 50) -> MemoryQueryResponse:
    """Return database memory records by recommended action."""

    return query_database_memory_snapshots(MemoryQueryRequest(recommended_action=recommended_action, limit=limit))


@router.get("/memory/sync-status", response_model=MemorySyncStatus)
def get_jsonl_to_database_sync_status() -> MemorySyncStatus:
    """Compare local JSONL memory snapshots with database snapshots."""

    return get_memory_sync_status()


@router.post("/memory/sync-jsonl-to-db", response_model=MemorySyncResult)
def sync_jsonl_memory_log_to_database(request: MemorySyncRequest | None = None) -> MemorySyncResult:
    """Sync local JSONL MemorySnapshot records into database tables."""

    return sync_jsonl_memory_to_database(request)


@router.post("/sync/pull/manual", response_model=LongTermMemoryPullResponse)
def pull_longterm_memory_manually(request: LongTermMemoryPullRequest | None = None) -> LongTermMemoryPullResponse:
    """Pull selected long-term memory records back to onboard GWAN."""

    return pull_longterm_memory_for_onboard(request)


@router.post("/sync/recommend", response_model=LongTermMemoryPullResponse)
def recommend_longterm_memory(request: LongTermMemoryRecommendationRequest | None = None) -> LongTermMemoryPullResponse:
    """Recommend useful long-term memory for current onboard context."""

    return recommend_longterm_memory_for_onboard(request)


@router.get("/sync/recommendation-settings", response_model=RecommendationSettings)
def get_sync_recommendation_settings() -> RecommendationSettings:
    """Return current proactive memory recommendation settings."""

    return get_recommendation_settings()


@router.post("/sync/recommendation-settings", response_model=RecommendationSettings)
def update_sync_recommendation_settings(settings: RecommendationSettings) -> RecommendationSettings:
    """Update in-process proactive memory recommendation settings."""

    return update_recommendation_settings(settings)
