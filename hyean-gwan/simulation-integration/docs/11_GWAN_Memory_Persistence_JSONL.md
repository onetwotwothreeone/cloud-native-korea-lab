# 11_GWAN_Memory_Persistence_JSONL

## Purpose

The previous step created `MemorySnapshot` objects. This step makes those snapshots durable by writing each snapshot to a JSONL file.

## Why JSONL first

JSONL is a simple persistence format where each line is one JSON record.

It is useful at this stage because it is:

- easy to inspect with a text editor
- append-friendly
- simple to test
- easy to migrate to PostgreSQL later

## New files

```text
app/services/gwan_memory_persistence.py
tests/test_gwan_memory_persistence_jsonl.py
docs/11_GWAN_Memory_Persistence_JSONL.md
codex/11_gwan_memory_persistence_jsonl_prompt.md
```

## New endpoints

```text
POST /gwan/memory/persist-snapshot
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/persisted-snapshots
GET  /gwan/memory/persistence-status
```

## Default file path

```text
data/gwan_memory_snapshots.jsonl
```

For tests or local experiments, override it with:

```bash
HYEAN_MEMORY_JSONL_PATH=/tmp/hyean-memory.jsonl
```

## Current flow

```text
Integrated simulation
→ MemorySnapshot
→ JSONL append
→ Reload persisted snapshots
→ Later PostgreSQL migration
```

## What to verify

After running the API, check that the JSONL file contains one snapshot per line.

Each persisted snapshot should preserve:

- observations
- scores
- decisions
- uncertainties
- map_updates

## Completion criteria

- MemorySnapshot can be written to JSONL.
- Persisted snapshots can be loaded back into Pydantic models.
- API endpoint can persist the default simulated snapshot.
- API endpoint can list persisted snapshots.
- API endpoint can report persistence status.
