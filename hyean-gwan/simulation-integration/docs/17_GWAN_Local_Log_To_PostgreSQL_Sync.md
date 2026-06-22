# 17_GWAN_Local_Log_To_PostgreSQL_Sync

## Purpose

This step connects the local JSONL memory log to the PostgreSQL memory database.

Previous steps proved two separate persistence paths:

```text
JSONL local memory log
PostgreSQL long-term memory database
```

This step adds the first Sync Layer behavior:

```text
Read local JSONL MemorySnapshots
→ compare with PostgreSQL snapshot IDs
→ insert only missing snapshots
→ skip duplicates safely
→ report sync results
```

## Why this matters

A mobile human habitat cannot assume constant connection to a ground/cloud database.

GWAN should first record urgent decisions locally. Later, when connection and power are stable, local records can be synchronized to the long-term PostgreSQL memory store.

## Added files

```text
app/services/gwan_memory_sync.py
tests/test_gwan_local_log_to_postgresql_sync.py
docs/17_GWAN_Local_Log_To_PostgreSQL_Sync.md
codex/17_gwan_local_log_to_postgresql_sync_prompt.md
```

## Added API

```text
GET  /gwan/memory/sync-status
POST /gwan/memory/sync-jsonl-to-db
```

## API meaning

| API | Meaning |
|---|---|
| `GET /gwan/memory/sync-status` | Compare JSONL local log and database snapshots. Shows pending and already-synced IDs. |
| `POST /gwan/memory/sync-jsonl-to-db` | Insert JSONL snapshots that are not already in PostgreSQL. |

## Sync rules

- Existing database snapshots are skipped.
- Duplicate snapshot IDs inside the JSONL file are skipped after the first insert.
- `dry_run: true` reports what would be inserted without writing to the database.
- The sync result includes inserted count, skipped count, pending count, and table counts.

## Manual run flow

```text
1. POST /gwan/memory/persist-simulated-snapshot
2. GET  /gwan/memory/sync-status
3. POST /gwan/memory/sync-jsonl-to-db
4. GET  /gwan/memory/sync-status
5. GET  /gwan/memory/db-query/action/send_micro_probe
```

## Example request

```json
{
  "dry_run": false,
  "limit": 100
}
```

## Expected result shape

```json
{
  "jsonl_record_count": 1,
  "processed_count": 1,
  "inserted_count": 1,
  "skipped_count": 0,
  "pending_count_after_sync": 0
}
```

## Completion criteria

- JSONL snapshots can be compared with database snapshots.
- Only missing snapshots are inserted.
- Duplicate sync runs do not duplicate DB rows.
- Dry-run mode works.
- Synced records can be queried through PostgreSQL query APIs.
