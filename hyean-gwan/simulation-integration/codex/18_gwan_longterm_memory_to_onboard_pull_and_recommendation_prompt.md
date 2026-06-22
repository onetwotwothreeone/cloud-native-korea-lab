# Codex task: 18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation

## Goal

Add reverse sync direction for HYEAN/GWAN.

Previous direction:

```text
JSONL local log -> PostgreSQL long-term memory
```

New direction:

```text
PostgreSQL long-term memory -> onboard GWAN knowledge package
```

## Add features

- Manual long-term memory pull
- Proactive long-term memory recommendation
- Recommendation frequency settings
- Onboard knowledge package response

## Required APIs

```text
POST /gwan/sync/pull/manual
POST /gwan/sync/recommend
GET  /gwan/sync/recommendation-settings
POST /gwan/sync/recommendation-settings
```

## Required files

```text
app/services/gwan_longterm_memory_pull.py
tests/test_gwan_longterm_memory_pull.py
docs/18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation.md
```

## Success criteria

```bash
pytest -q
```

All tests must pass.
