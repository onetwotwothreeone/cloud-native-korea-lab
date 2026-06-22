# 10_GWAN_Memory_Map_Update_Model

## Purpose

This step adds the first GWAN memory and survival-map update model.

Before this step, GWAN could generate interface payloads and scoring decisions. This step asks the next question:

```text
GWAN observed, scored, and recommended an action.
What should be remembered?
What should update the survival map?
```

## New model groups

```text
ObservationRecord
ScoreRecord
DecisionRecord
MemoryUncertaintyRecord
MapUpdateRecord
MemorySnapshot
```

## Data flow

```text
IntegratedSimulationResult
→ ObservationRecord
→ ScoreRecord
→ DecisionRecord
→ MemoryUncertaintyRecord
→ MapUpdateRecord
→ MemorySnapshot
```

## New endpoints

```text
POST /gwan/memory/snapshot
GET  /gwan/memory/simulated-snapshot
```

## What MemorySnapshot contains

- observations: what GWAN saw or represented spatially
- scores: how each object was scored
- decisions: what GWAN recommended
- uncertainties: why some points remain uncertain
- map_updates: how the living survival map should change

## Why this matters

HYEAN is not only a one-time response system. It should become a living survival map.

That means each GWAN run must leave memory behind:

- resource candidate records
- risk zone records
- navigation reference updates
- uncertainty records
- decision audit trail

## Current limitation

This step uses in-memory Python models only. It does not yet store records in PostgreSQL.

## Next step

The next implementation step should be:

```text
11_GWAN_Memory_Persistence_PostgreSQL_or_JSONL
```

A lightweight first option is JSONL persistence. A later cloud-native option is PostgreSQL.
