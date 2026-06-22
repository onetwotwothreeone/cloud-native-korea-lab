# Codex task: 10_GWAN_Memory_Map_Update_Model

## Goal

Add the first GWAN memory and survival-map update model.

## Context

The project already has:

- GWAN data contract models
- scoring test cases
- integrated simulation payload generation

Now add memory records so each GWAN run can preserve what it observed, scored, decided, and changed in the survival map.

## Required files

```text
app/services/gwan_memory.py
tests/test_gwan_memory_map_update.py
docs/10_GWAN_Memory_Map_Update_Model.md
codex/10_gwan_memory_map_update_model_prompt.md
app/api/routes_gwan.py
README.md
```

## Required models

- ObservationRecord
- ScoreRecord
- DecisionRecord
- MemoryUncertaintyRecord
- MapUpdateRecord
- MemorySnapshot

## Required endpoints

```text
POST /gwan/memory/snapshot
GET  /gwan/memory/simulated-snapshot
```

## Success criteria

```bash
pytest -q
```

All tests must pass.
