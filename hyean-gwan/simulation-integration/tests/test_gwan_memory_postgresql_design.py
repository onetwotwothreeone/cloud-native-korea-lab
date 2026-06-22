from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect

from app.main import app

from app.db.gwan_memory_models import Base
from app.services.gwan_memory import generate_simulated_memory_snapshot
from app.services.gwan_memory_postgres_design import (
    generate_simulated_memory_insert_plan,
    get_memory_postgres_design,
    get_sqlalchemy_table_names,
    memory_snapshot_to_insert_plan,
)

EXPECTED_TABLES = {
    "memory_snapshots",
    "observation_records",
    "score_records",
    "decision_records",
    "uncertainty_records",
    "map_update_records",
}


def test_postgres_design_lists_expected_tables():
    design = get_memory_postgres_design()

    assert {table.table_name for table in design.tables} == EXPECTED_TABLES
    assert design.design_version == "hyean.gwan.memory.postgres.v0.1"


def test_sqlalchemy_metadata_contains_expected_tables():
    assert set(get_sqlalchemy_table_names()) == EXPECTED_TABLES


def test_sqlalchemy_tables_can_be_created_in_sqlite_memory():
    # SQLite is used only as a fast structural check.
    # The production target remains PostgreSQL.
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    assert set(inspector.get_table_names()) == EXPECTED_TABLES


def test_memory_snapshot_converts_to_database_insert_plan():
    snapshot = generate_simulated_memory_snapshot()
    plan = memory_snapshot_to_insert_plan(snapshot)

    assert plan.snapshot["snapshot_id"] == snapshot.snapshot_id
    assert len(plan.observations) == len(snapshot.observations)
    assert len(plan.scores) == len(snapshot.scores)
    assert len(plan.decisions) == len(snapshot.decisions)
    assert len(plan.uncertainties) == len(snapshot.uncertainties)
    assert len(plan.map_updates) == len(snapshot.map_updates)
    assert plan.total_child_rows() == (
        len(snapshot.observations)
        + len(snapshot.scores)
        + len(snapshot.decisions)
        + len(snapshot.uncertainties)
        + len(snapshot.map_updates)
    )


def test_insert_plan_has_query_friendly_columns():
    plan = generate_simulated_memory_insert_plan()

    risk_row = next(row for row in plan.scores if row["object_id"] == "risk-radiation-critical-001")
    decision_row = next(row for row in plan.decisions if row["object_id"] == "risk-radiation-critical-001")
    map_row = next(row for row in plan.map_updates if row["object_id"] == "risk-radiation-critical-001")

    assert risk_row["risk_score"] >= 0.75
    assert decision_row["recommended_action"] == "avoid"
    assert map_row["map_layer"] == "risk_zones"


def test_postgres_design_endpoint():
    client = TestClient(app)
    response = client.get("/gwan/memory/postgres-design")

    assert response.status_code == 200
    data = response.json()
    assert data["design_version"] == "hyean.gwan.memory.postgres.v0.1"
    assert len(data["tables"]) == 6


def test_postgres_insert_plan_endpoint():
    client = TestClient(app)
    response = client.get("/gwan/memory/postgres-insert-plan")

    assert response.status_code == 200
    data = response.json()
    assert data["snapshot"]["snapshot_id"] == "memory-snapshot-sim-001"
    assert len(data["observations"]) == 4
    assert len(data["map_updates"]) == 4
