# 13_GWAN_Memory_PostgreSQL_Design

## Purpose

This step prepares the GWAN Memory Layer for a future PostgreSQL database.

The current system stores `MemorySnapshot` records in JSONL. JSONL is easy to inspect and good for early learning. PostgreSQL becomes useful when the project needs stronger querying, relationships, concurrency, indexes, migrations, and long-term service storage.

## Easy summary

```text
JSONL = simple space-navigation diary file
PostgreSQL = organized database cabinet for the living survival map
```

This step does not remove JSONL yet. It creates the future database design beside it.

## Added files

```text
app/db/__init__.py
app/db/gwan_memory_models.py
app/services/gwan_memory_postgres_design.py
tests/test_gwan_memory_postgresql_design.py
docs/13_GWAN_Memory_PostgreSQL_Design.md
codex/13_gwan_memory_postgresql_design_prompt.md
```

## New endpoints

```text
GET /gwan/memory/postgres-design
GET /gwan/memory/postgres-insert-plan
```

## Table design

| Table | Purpose |
|---|---|
| `memory_snapshots` | Parent record for one complete GWAN memory run |
| `observation_records` | What GWAN observed or represented in spatial output |
| `score_records` | Energy, resource, risk, exploration, uncertainty, and survival scores |
| `decision_records` | Recommended action, reason summary, and alert level |
| `uncertainty_records` | Uncertainty reason, impact, and suggested resolution |
| `map_update_records` | How each object should update the living survival map |

## Relationship structure

```text
memory_snapshots
├─ observation_records
├─ score_records
├─ decision_records
├─ uncertainty_records
└─ map_update_records
```

Every child table has a `snapshot_id` that points back to `memory_snapshots.snapshot_id`.

## Why this supports HYEAN/GWAN

HYEAN is a living survival map. GWAN is the observation, interpretation, scoring, decision, and memory engine. A database design lets GWAN memory become searchable, durable, and eventually service-ready.

## What this step proves

- The future PostgreSQL table names are clear.
- The SQLAlchemy models can create all tables.
- A simulated `MemorySnapshot` can be converted into database-ready row dictionaries.
- Risk, uncertainty, recommended action, map layer, and object ID become query-friendly columns.

## Current limitation

This step does not connect to a real PostgreSQL container yet.

It is a design and migration-preparation step. The next step can add PostgreSQL with Docker Compose.

## Next recommended step

```text
14_GWAN_PostgreSQL_Local_Docker_Compose
```

That step should add:

- PostgreSQL service in Docker Compose
- database URL setting
- SQLAlchemy engine/session
- table creation or Alembic migration direction
- one write/read test against a local database
