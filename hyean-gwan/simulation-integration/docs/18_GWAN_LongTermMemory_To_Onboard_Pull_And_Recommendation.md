# 18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation

## Purpose

This step adds the reverse direction of the HYEAN/GWAN Sync Layer.

Previous step:

```text
Onboard local JSONL log
→ PostgreSQL long-term memory
```

This step:

```text
PostgreSQL long-term memory
→ Onboard GWAN Core knowledge package
```

## Why this matters

A mobile human habitat cannot assume that all useful knowledge is already onboard. It also cannot assume constant connection to Earth or a ground/cloud system.

So HYEAN/GWAN needs both directions:

1. Upload local observations and decisions to long-term memory.
2. Pull or recommend useful long-term memory back to onboard GWAN when it helps survival, exploration, risk handling, or uncertainty handling.

## New concepts

| Concept | Meaning |
|---|---|
| Manual Pull | Operator asks for specific long-term memory. |
| Proactive Recommendation | GWAN recommends helpful memory based on current context. |
| Recommendation Settings | Controls how often automatic recommendation should happen. |
| Onboard Knowledge Package | Long-term memory prepared for onboard GWAN use. |

## New APIs

```text
POST /gwan/sync/pull/manual
POST /gwan/sync/recommend
GET  /gwan/sync/recommendation-settings
POST /gwan/sync/recommendation-settings
```

## Manual pull examples

Use manual pull when the operator suddenly wants to search long-term memory.

Examples:

```text
Find high-risk records.
Find high-uncertainty records.
Find records for one object_id.
Find previous send_micro_probe candidates.
Find records from one map layer.
```

Example request:

```json
{
  "query_type": "high_risk",
  "limit": 5
}
```

## Proactive recommendation examples

Use proactive recommendation when GWAN sees that long-term memory may help the current situation even if the human operator did not ask.

Example request:

```json
{
  "operator_intent": "resource route planning",
  "predicted_route_object_ids": [
    "candidate-resource-stable-001",
    "risk-radiation-critical-001"
  ],
  "triggers": ["on_route_change"],
  "limit": 5
}
```

## Recommendation frequency modes

| Mode | Meaning |
|---|---|
| manual_only | Only pull when the operator asks. |
| low_frequency | Recommend rarely, only with meaningful triggers. |
| normal | Balanced default mode. |
| high_frequency | Recommend more often during active exploration. |
| critical_only | Recommend only when survival-critical or high-risk. |

## Important limitation

This is not a final background scheduler. It is an API-level prototype.

It proves that long-term memory can be packaged back into an onboard-friendly format. Later versions can add real scheduling, bandwidth limits, conflict handling, and onboard cache management.

## Completion criteria

- Manual pull can retrieve high-risk records from PostgreSQL.
- Manual pull can retrieve send_micro_probe candidates.
- Proactive recommendation can rank records by relevance.
- Recommendation settings can control automatic recommendation behavior.
- manual_only blocks proactive recommendations.
- critical_only allows recommendations during high-risk context.
