# Codex task: 15_GWAN_PostgreSQL_Query_API

Add direct database query APIs for GWAN MemorySnapshot records persisted into SQLAlchemy/PostgreSQL tables.

## Required files

```text
app/services/gwan_memory_postgres_query.py
tests/test_gwan_postgresql_query_api.py
docs/15_GWAN_PostgreSQL_Query_API.md
docs/troubleshooting/2026-06-22_postgres_role_and_port_troubleshooting.md
```

## Required endpoints

```text
POST /gwan/memory/db-query
GET  /gwan/memory/db-query/object/{object_id}
GET  /gwan/memory/db-query/high-risk
GET  /gwan/memory/db-query/high-uncertainty
GET  /gwan/memory/db-query/action/{recommended_action}
```

## Required behavior

- Query relational tables directly through SQLAlchemy.
- Reuse MemoryQueryRequest and MemoryQueryResponse where possible.
- Join snapshots, observations, scores, decisions, uncertainties, and map updates by snapshot_id and object_id.
- Support filters for object_id, risk score, uncertainty score, recommended action, map layer, display category, and alert level.
- Keep tests Docker-independent by using SQLite.
- Update Docker Compose host port to 55432 to avoid local 5432 conflicts.

## Success command

```bash
pytest -q
```
