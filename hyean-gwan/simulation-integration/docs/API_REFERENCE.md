# HYEAN/GWAN API Reference

This document is the human-readable API map for the current GWAN prototype.

## Core idea

```text
GWAN Engine
→ scoring / simulation / memory
→ structured payloads
→ HYEAN Operator Interface and Memory & Map System
```

## API groups

| Group | Purpose |
|---|---|
| Health | Confirm the FastAPI app is running |
| Interface Payload | Validate GWAN output against the data contract |
| Simulation | Generate synthetic GWAN scenarios and payloads |
| Scoring | Test transparent scoring rules and expected recommendations |
| Memory Snapshot | Convert integrated simulation results into memory records |
| JSONL Persistence | Save and read memory snapshots from JSONL |
| JSONL Query | Search JSONL memory snapshots |
| PostgreSQL Design | Inspect the future database table design |
| PostgreSQL Persistence | Create tables and persist memory snapshots to PostgreSQL |
| PostgreSQL Query | Search memory records directly from PostgreSQL |

## Recommended local execution order

Use this order when checking the full prototype in `/docs`.

```text
1. GET  /health
2. POST /gwan/simulate-integrated
3. GET  /gwan/memory/simulated-snapshot
4. POST /gwan/memory/persist-simulated-snapshot
5. GET  /gwan/memory/persistence-status
6. GET  /gwan/memory/query/high-risk
7. GET  /gwan/memory/query/high-uncertainty
8. GET  /gwan/memory/postgres-design
9. GET  /gwan/memory/postgres-insert-plan
10. GET  /gwan/memory/db-status
11. POST /gwan/memory/db-create-tables
12. POST /gwan/memory/db-persist-simulated-snapshot
13. GET  /gwan/memory/db-snapshots
14. GET  /gwan/memory/db-query/high-risk
15. GET  /gwan/memory/db-query/high-uncertainty
16. GET  /gwan/memory/db-query/action/send_micro_probe
```

## Endpoint table

| Method | Endpoint | Role in HYEAN/GWAN | Expected success check |
|---|---|---|---|
| GET | `/health` | Confirms the API process is alive | `{"status": "ok"}` |
| POST | `/gwan/interface-payload` | Validates a GWAN → Operator Interface payload | Returns the same valid payload |
| POST | `/gwan/simulate` | Generates a GWAN interface payload from simulation | `packages` contains spatial/sidebar/alert/uncertainty/report |
| POST | `/gwan/simulate-integrated` | Generates payload plus object-level scoring decisions | Response contains `payload` and `object_decisions` |
| POST | `/gwan/score` | Scores one scenario and returns a recommended action | Response contains `recommended_action` |
| GET | `/gwan/scoring-test-cases` | Runs default scoring cases | All `passed` values are `true` |
| POST | `/gwan/memory/snapshot` | Converts integrated simulation result to memory records | Response contains observations/scores/decisions |
| GET | `/gwan/memory/simulated-snapshot` | Generates default simulated memory snapshot | Response contains `map_updates` |
| POST | `/gwan/memory/persist-snapshot` | Saves provided MemorySnapshot to JSONL | Response contains `record_count` |
| POST | `/gwan/memory/persist-simulated-snapshot` | Generates and saves default MemorySnapshot to JSONL | `record_count` increases |
| GET | `/gwan/memory/persisted-snapshots` | Lists JSONL snapshots | Returns list of MemorySnapshot records |
| GET | `/gwan/memory/persistence-status` | Checks JSONL persistence file | Shows file path and record count |
| POST | `/gwan/memory/query` | Flexible JSONL memory query | Response contains `matches` |
| GET | `/gwan/memory/query/object/{object_id}` | JSONL object history lookup | Returns records for the object |
| GET | `/gwan/memory/query/high-risk` | JSONL high-risk lookup | Finds risk-zone records |
| GET | `/gwan/memory/query/high-uncertainty` | JSONL high-uncertainty lookup | Finds weak-signal records |
| GET | `/gwan/memory/postgres-design` | Shows PostgreSQL table design | Shows six memory tables |
| GET | `/gwan/memory/postgres-insert-plan` | Converts simulated memory to DB row plan | Shows snapshot/observations/scores/decisions/uncertainties/map_updates |
| GET | `/gwan/memory/db-status` | Checks DATABASE_URL connection and tables | `connected: true` after DB is ready |
| POST | `/gwan/memory/db-create-tables` | Creates PostgreSQL memory tables | Returns created table names |
| POST | `/gwan/memory/db-persist-snapshot` | Persists provided MemorySnapshot to PostgreSQL | Returns table counts |
| POST | `/gwan/memory/db-persist-simulated-snapshot` | Persists default simulated MemorySnapshot to PostgreSQL | `inserted: true` or duplicate-safe `false` |
| GET | `/gwan/memory/db-snapshots` | Lists PostgreSQL snapshots | Shows snapshot counts |
| POST | `/gwan/memory/db-query` | Flexible PostgreSQL memory query | Response contains `matches` |
| GET | `/gwan/memory/db-query/object/{object_id}` | PostgreSQL object history lookup | Returns records for the object |
| GET | `/gwan/memory/db-query/high-risk` | PostgreSQL high-risk lookup | Finds `risk-radiation-critical-001` |
| GET | `/gwan/memory/db-query/high-uncertainty` | PostgreSQL high-uncertainty lookup | Finds `candidate-ice-weak-signal-001` |
| GET | `/gwan/memory/db-query/action/{recommended_action}` | PostgreSQL recommended-action lookup | `send_micro_probe` finds resource candidate |

## Key sample object IDs

| Object ID | Meaning | Expected action |
|---|---|---|
| `candidate-resource-stable-001` | Stable resource candidate | `send_micro_probe` |
| `risk-radiation-critical-001` | High-risk radiation region | `avoid` |
| `candidate-ice-weak-signal-001` | Weak spectral signal / uncertain resource candidate | `observe_more` |
| `nav-reference-stable-001` | Stable navigation reference | `update_survival_map` |

## Common success responses

### PostgreSQL persistence success

```json
{
  "snapshot_id": "memory-snapshot-sim-001",
  "inserted": true,
  "table_counts": {
    "memory_snapshots": 1,
    "observation_records": 4,
    "score_records": 4,
    "decision_records": 4,
    "uncertainty_records": 1,
    "map_update_records": 4
  },
  "message": "MemorySnapshot persisted to database."
}
```

### PostgreSQL status success after table creation

```json
{
  "connected": true,
  "tables_created": true
}
```

## Common errors

| Error | Meaning | Fix |
|---|---|---|
| `docker: command not found` | Docker CLI is not on PATH | Add Docker CLI path or configure Docker Desktop CLI tools |
| `FATAL: role "hyean" does not exist` | FastAPI is reaching wrong/stale PostgreSQL or old volume | Use `55432:5432`, reset volume, update `DATABASE_URL` |
| `connected: true, tables_created: false` | DB connection works but tables are not created yet | Run `POST /gwan/memory/db-create-tables` |
| `inserted: false` | Snapshot already exists | Normal duplicate protection |

## Current limitation

This prototype uses synthetic and simulated data only. It proves structure, scoring consistency, memory persistence, and query behavior. It does not claim real spacecraft operation or confirmed scientific discovery.

## 17. JSONL to PostgreSQL Sync

These APIs connect the local JSONL memory log to the PostgreSQL long-term memory database.

| Method | Path | Purpose |
|---|---|---|
| GET | `/gwan/memory/sync-status` | Compare JSONL snapshot IDs with PostgreSQL snapshot IDs. |
| POST | `/gwan/memory/sync-jsonl-to-db` | Insert JSONL snapshots that are not already in PostgreSQL. |

Recommended sync flow:

```text
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/sync-status
POST /gwan/memory/sync-jsonl-to-db
GET  /gwan/memory/sync-status
GET  /gwan/memory/db-query/action/send_micro_probe
```

Example sync body:

```json
{
  "dry_run": false,
  "limit": 100
}
```

Use `dry_run: true` when you want to see what would be inserted without writing to the database.

## 18. Long-term memory to onboard pull and recommendation

These APIs implement the reverse direction of the Sync Layer.

```text
PostgreSQL long-term memory -> onboard GWAN knowledge package
```

### POST /gwan/sync/pull/manual

Operator-requested long-term memory pull.

Example body:

```json
{
  "query_type": "high_risk",
  "limit": 5
}
```

Useful query types:

```text
object_history
high_risk
high_uncertainty
recommended_action
resource_candidates
map_layer
general
```

### POST /gwan/sync/recommend

Proactive memory recommendation based on current onboard context.

Example body:

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

### GET /gwan/sync/recommendation-settings

Returns current proactive recommendation settings.

### POST /gwan/sync/recommendation-settings

Updates in-process recommendation settings.

Example body:

```json
{
  "frequency": "normal",
  "enabled_triggers": ["on_route_change", "on_high_risk", "on_high_uncertainty"],
  "max_recommendations_per_cycle": 3,
  "min_relevance_score": 0.55,
  "include_low_confidence": true
}
```

Frequency modes:

```text
manual_only
low_frequency
normal
high_frequency
critical_only
```
