# Codex task: 12_GWAN_Memory_Query_API

Implement a query layer for persisted GWAN MemorySnapshot records.

## Goal

The previous step persisted MemorySnapshot records into JSONL. Add APIs and tests so users can search that memory.

## Required files

```text
app/services/gwan_memory_query.py
tests/test_gwan_memory_query_api.py
docs/12_GWAN_Memory_Query_API.md
app/api/routes_gwan.py
README.md
```

## Required endpoints

```text
POST /gwan/memory/query
GET  /gwan/memory/query/object/{object_id}
GET  /gwan/memory/query/high-risk
GET  /gwan/memory/query/high-uncertainty
```

## Required filters

- snapshot_id
- mission_id
- object_id
- map_layer
- display_category
- recommended_action
- alert_level
- min_risk_score
- min_uncertainty_score
- limit

## Success criteria

```bash
pytest -q
```

All tests must pass.
