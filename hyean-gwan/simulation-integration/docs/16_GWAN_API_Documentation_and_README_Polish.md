# 16_GWAN_API_Documentation_and_README_Polish

## Purpose

This step improves project readability after the API surface became large.

The previous steps added simulation, scoring, JSONL memory, PostgreSQL persistence, and PostgreSQL query APIs. The code worked, but the user flow was becoming hard to understand from the README alone.

This step makes the project easier to run, review, and present as a portfolio-quality technical artifact.

## What changed

New documentation:

```text
docs/API_REFERENCE.md
docs/LOCAL_RUNBOOK.md
docs/README_REVIEW_CHECKLIST.md
docs/16_GWAN_API_Documentation_and_README_Polish.md
```

Updated documentation:

```text
README.md
```

New tests:

```text
tests/test_gwan_api_documentation.py
```

## Why this matters

HYEAN/GWAN now has many APIs. Without a clear execution order, a beginner can easily click the wrong endpoint first and misunderstand the result.

This step solves that by documenting:

- what each API does
- which APIs should be checked first
- how JSONL and PostgreSQL flows differ
- what success responses look like
- what common errors mean
- why port `55432` is used for PostgreSQL

## Current API groups

```text
Health
Interface Payload
Simulation
Scoring
Memory Snapshot
JSONL Persistence
JSONL Query
PostgreSQL Design
PostgreSQL Persistence
PostgreSQL Query
```

## Recommended `/docs` check order

```text
GET  /health
POST /gwan/simulate-integrated
GET  /gwan/memory/simulated-snapshot
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/persistence-status
GET  /gwan/memory/query/high-risk
GET  /gwan/memory/query/high-uncertainty
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-query/high-risk
GET  /gwan/memory/db-query/high-uncertainty
GET  /gwan/memory/db-query/action/send_micro_probe
```

## Completion criteria

- README explains HYEAN/GWAN purpose in beginner-readable language.
- README gives clean install and run commands.
- README uses PostgreSQL port `55432`.
- API reference lists all current routes.
- Local runbook includes the PostgreSQL troubleshooting flow.
- Documentation tests pass.
