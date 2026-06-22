# Codex task: 17_GWAN_Local_Log_To_PostgreSQL_Sync

Implement JSONL-to-PostgreSQL memory sync for HYEAN/GWAN.

## Goal

Create a Sync Layer step that reads local JSONL `MemorySnapshot` records and inserts only snapshots missing from PostgreSQL.

## Required files

```text
app/services/gwan_memory_sync.py
tests/test_gwan_local_log_to_postgresql_sync.py
docs/17_GWAN_Local_Log_To_PostgreSQL_Sync.md
app/api/routes_gwan.py
README.md
docs/API_REFERENCE.md
docs/LOCAL_RUNBOOK.md
```

## Required APIs

```text
GET  /gwan/memory/sync-status
POST /gwan/memory/sync-jsonl-to-db
```

## Behavior

- Compare JSONL snapshot IDs against DB snapshot IDs.
- Insert only missing snapshots.
- Skip snapshots already in DB.
- Support `dry_run`.
- Return inserted count, skipped count, pending count, table counts, and per-snapshot results.

## Success command

```bash
pytest -q
```
