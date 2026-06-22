# Codex task: 11_GWAN_Memory_Persistence_JSONL

## Goal

Add JSONL persistence for GWAN MemorySnapshot records.

## Context

HYEAN/GWAN now creates MemorySnapshot records containing observations, scores, decisions, uncertainties, and map updates. The next step is to persist those records before later migrating to PostgreSQL.

## Files to create or update

```text
app/services/gwan_memory_persistence.py
app/api/routes_gwan.py
tests/test_gwan_memory_persistence_jsonl.py
docs/11_GWAN_Memory_Persistence_JSONL.md
README.md
```

## Required endpoints

```text
POST /gwan/memory/persist-snapshot
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/persisted-snapshots
GET  /gwan/memory/persistence-status
```

## Requirements

1. Store one MemorySnapshot per JSONL line.
2. Reload JSONL lines back into MemorySnapshot Pydantic models.
3. Support path override with `HYEAN_MEMORY_JSONL_PATH`.
4. Add tests for append, read, status, API persistence, and list endpoint.
5. Keep JSONL simple and inspectable.

## Success command

```bash
pytest -q
```
