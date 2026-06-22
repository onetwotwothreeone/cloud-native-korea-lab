# 12_GWAN_Memory_Query_API

## Purpose

The previous step stored GWAN MemorySnapshot records in JSONL. This step adds a query layer so the stored memory can be searched.

In simple terms:

```text
11 = GWAN writes memory to a log file
12 = GWAN can search that memory log
```

## Why this matters

HYEAN is a living survival map. A living map should not only store records; it should let operators ask useful questions.

Examples:

- Which objects are high risk?
- Which objects are uncertain?
- What do we know about this object_id?
- Which records recommended avoid?
- Which records belong to the risk_zones map layer?

## Added files

```text
app/services/gwan_memory_query.py
tests/test_gwan_memory_query_api.py
docs/12_GWAN_Memory_Query_API.md
codex/12_gwan_memory_query_api_prompt.md
```

## Added endpoints

```text
POST /gwan/memory/query
GET  /gwan/memory/query/object/{object_id}
GET  /gwan/memory/query/high-risk
GET  /gwan/memory/query/high-uncertainty
```

## Query filters

`POST /gwan/memory/query` supports:

- `snapshot_id`
- `mission_id`
- `object_id`
- `map_layer`
- `display_category`
- `recommended_action`
- `alert_level`
- `min_risk_score`
- `min_uncertainty_score`
- `limit`

## Example request

```json
{
  "min_risk_score": 0.75,
  "limit": 10
}
```

## Example result meaning

If the result contains `risk-radiation-critical-001`, it means GWAN found a stored memory object whose risk score is above the requested threshold.

## Current limitation

This is still JSONL-based local memory. It is good for learning, testing, and early design. Later, the same query ideas can move to PostgreSQL.

## Next step

The next step is `13_GWAN_Memory_PostgreSQL_Design`, which defines how the JSONL memory model should become relational tables later.
