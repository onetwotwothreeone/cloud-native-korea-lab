# Codex task: 13_GWAN_Memory_PostgreSQL_Design

## Goal

Prepare the GWAN Memory Layer for future PostgreSQL persistence.

## Context

The project currently stores `MemorySnapshot` records in JSONL and supports memory queries. The next step is to design the relational database structure without replacing JSONL yet.

## Add or update these files

```text
app/db/__init__.py
app/db/gwan_memory_models.py
app/services/gwan_memory_postgres_design.py
tests/test_gwan_memory_postgresql_design.py
docs/13_GWAN_Memory_PostgreSQL_Design.md
app/api/routes_gwan.py
requirements.txt
pyproject.toml
README.md
```

## Required tables

```text
memory_snapshots
observation_records
score_records
decision_records
uncertainty_records
map_update_records
```

## Required behavior

1. Define SQLAlchemy 2.0 ORM models.
2. Keep enum-like values as strings for early migration simplicity.
3. Use one parent table: `memory_snapshots`.
4. Link child tables by `snapshot_id`.
5. Add query-friendly columns for object_id, risk_score, uncertainty_score, recommended_action, alert_level, map_layer, and data_classification.
6. Add a function that converts a `MemorySnapshot` into database-ready row dictionaries.
7. Add tests that create all tables in SQLite memory as a structural check.
8. Add `/gwan/memory/postgres-design` and `/gwan/memory/postgres-insert-plan` endpoints.

## Success command

```bash
pytest -q
```

## Design rule

JSONL remains the simple local memory log for now. PostgreSQL is the future organized storage layer for the living survival map.
