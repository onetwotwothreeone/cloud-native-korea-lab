# 15_GWAN_PostgreSQL_Query_API

## Purpose

This step adds direct PostgreSQL/SQLAlchemy query APIs for persisted GWAN memory records.

The previous step stored MemorySnapshot records into database tables. This step lets HYEAN/GWAN search those database records by operational conditions.

## What changed

New service:

```text
app/services/gwan_memory_postgres_query.py
```

New tests:

```text
tests/test_gwan_postgresql_query_api.py
```

New API routes:

```text
POST /gwan/memory/db-query
GET  /gwan/memory/db-query/object/{object_id}
GET  /gwan/memory/db-query/high-risk
GET  /gwan/memory/db-query/high-uncertainty
GET  /gwan/memory/db-query/action/{recommended_action}
```

## Query examples

High-risk objects:

```text
GET /gwan/memory/db-query/high-risk?min_risk_score=0.75
```

High-uncertainty objects:

```text
GET /gwan/memory/db-query/high-uncertainty?min_uncertainty_score=0.60
```

Object history:

```text
GET /gwan/memory/db-query/object/candidate-ice-weak-signal-001
```

Recommended action:

```text
GET /gwan/memory/db-query/action/send_micro_probe
```

## Why this matters

GWAN memory is now no longer only stored. It can be searched directly from database tables.

This supports the future HYEAN Operator Interface and Memory & Map System:

- show high-risk records
- show high-uncertainty records
- search by object ID
- search by recommended action
- connect memory history to survival map layers

## Local PostgreSQL port decision

The Docker Compose host port was changed to `55432:5432` to avoid conflicts with any existing PostgreSQL service on the Mac host.

Use:

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
```

## Completion criteria

- PostgreSQL tables can be created.
- Simulated MemorySnapshot can be persisted.
- DB query API can find high-risk objects.
- DB query API can find high-uncertainty objects.
- DB query API can search by object ID.
- DB query API can search by recommended action.
- Tests pass without requiring Docker by using SQLite for structural checks.
