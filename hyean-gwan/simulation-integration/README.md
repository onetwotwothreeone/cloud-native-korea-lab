# HYEAN / GWAN Prototype

HYEAN is a survival-oriented space intelligence service for mobile human habitats.

GWAN is the core observation, interpretation, scoring, decision, and memory engine inside HYEAN.

This repository is the current backend prototype for GWAN simulation, scoring, memory, persistence, and query workflows.

## Beginner summary

This project asks a simple question:

```text
If a mobile human habitat is traveling through space,
how can it observe nearby objects,
score risks/resources/uncertainty,
recommend actions,
and remember what it learned?
```

Current prototype flow:

```text
Synthetic space scenario
→ GWAN scoring rule
→ recommended action
→ Operator Interface payload
→ MemorySnapshot
→ JSONL or PostgreSQL storage
→ memory query API
```

## What this prototype can do now

- Validate GWAN → HYEAN Operator Interface payloads
- Generate simulated space scenarios
- Score resource, risk, exploration value, uncertainty, and survival priority
- Recommend actions such as `avoid`, `observe_more`, `send_micro_probe`, and `update_survival_map`
- Convert simulation results into MemorySnapshot records
- Save memory to JSONL
- Query JSONL memory
- Design PostgreSQL tables
- Run local PostgreSQL through Docker Compose
- Persist MemorySnapshot records to PostgreSQL
- Query PostgreSQL memory records by risk, uncertainty, object ID, and recommended action

## Important limitation

This prototype uses synthetic and simulated data only.

It does **not** claim real spacecraft control, real sensor integration, or confirmed scientific discovery.

The goal is to make GWAN's data contract, scoring behavior, uncertainty handling, memory structure, and API workflow testable.

## Current test status

```bash
pytest -q
```

Expected result:

```text
70 passed
```

## Project structure

```text
app/
  api/routes_gwan.py
  db/gwan_memory_models.py
  db/session.py
  schemas/gwan_interface.py
  services/gwan_scoring.py
  services/gwan_simulation.py
  services/gwan_memory.py
  services/gwan_memory_persistence.py
  services/gwan_memory_query.py
  services/gwan_memory_postgres_design.py
  services/gwan_memory_postgres_persistence.py
  services/gwan_memory_postgres_query.py

docs/
  API_REFERENCE.md
  LOCAL_RUNBOOK.md
  README_REVIEW_CHECKLIST.md
  troubleshooting/

tests/
  fixtures/
  test_*.py

docker-compose.yml
requirements.txt
pyproject.toml
```

## Quick start: Python only

This checks the code without Docker.

```bash
cd ~/Downloads
rm -rf hyean_gwan_simulation_integration
unzip hyean_gwan_postgresql_query_api_2026-06-22.zip
cd hyean_gwan_simulation_integration

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Expected:

```text
70 passed
```

## Quick start: FastAPI docs

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Quick start: PostgreSQL with Docker Compose

Docker Desktop must be running.

```bash
docker compose down -v
docker compose up -d postgres
docker compose ps
```

Expected port mapping:

```text
0.0.0.0:55432->5432/tcp
```

Set the database URL:

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
```

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Recommended `/docs` execution order

### 1. Basic API check

```text
GET /health
```

### 2. Simulation and scoring

```text
POST /gwan/simulate-integrated
GET  /gwan/scoring-test-cases
```

### 3. Memory snapshot

```text
GET /gwan/memory/simulated-snapshot
```

### 4. JSONL persistence and query

```text
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/persistence-status
GET  /gwan/memory/query/high-risk
GET  /gwan/memory/query/high-uncertainty
GET  /gwan/memory/query/object/candidate-ice-weak-signal-001
```

### 5. PostgreSQL design and persistence

```text
GET  /gwan/memory/postgres-design
GET  /gwan/memory/postgres-insert-plan
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-snapshots
```

### 6. PostgreSQL query

```text
GET /gwan/memory/db-query/high-risk
GET /gwan/memory/db-query/high-uncertainty
GET /gwan/memory/db-query/object/candidate-ice-weak-signal-001
GET /gwan/memory/db-query/action/send_micro_probe
```

## API documentation

See:

```text
docs/API_REFERENCE.md
docs/LOCAL_RUNBOOK.md
```

## Key object IDs for checking results

| Object ID | Meaning | Expected action |
|---|---|---|
| `candidate-resource-stable-001` | Stable resource candidate | `send_micro_probe` |
| `risk-radiation-critical-001` | High-risk radiation region | `avoid` |
| `candidate-ice-weak-signal-001` | Weak signal / uncertain resource candidate | `observe_more` |
| `nav-reference-stable-001` | Stable navigation reference | `update_survival_map` |

## Common troubleshooting

### `docker: command not found`

Docker Desktop may be running, but the Docker CLI may not be on PATH.

Check Docker Desktop CLI settings or add the CLI path to your shell.

### `FATAL: role "hyean" does not exist`

Most likely FastAPI is reaching the wrong PostgreSQL server or an old Docker volume.

Fix:

```bash
docker compose down -v
docker compose up -d postgres
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
uvicorn app.main:app --reload
```

See:

```text
docs/troubleshooting/2026-06-22_postgres_role_and_port_troubleshooting.md
```

## Current implementation steps

```text
05 Data Contract
→ 06 Pydantic Models
→ 07 First Simulation Logic
→ 08 Scoring Test Cases
→ 09 Simulation + Scoring Integration
→ 10 Memory Map Update Model
→ 11 Memory Persistence JSONL
→ 12 Memory Query API
→ 13 Memory PostgreSQL Design
→ 14 PostgreSQL Local Docker Compose
→ 15 PostgreSQL Query API
→ 16 API Documentation and README Polish
```

## Next recommended step

```text
17_GWAN_GitHub_Actions_CI
```

The project now has enough tests and documentation to benefit from automated CI. The next step should run `pytest -q` automatically on every push or pull request.

## 17. JSONL local log to PostgreSQL sync

GWAN now supports the first Sync Layer behavior.

```text
local JSONL memory log
→ sync missing snapshots
→ PostgreSQL long-term memory database
```

New APIs:

```text
GET  /gwan/memory/sync-status
POST /gwan/memory/sync-jsonl-to-db
```

Recommended check:

```text
1. POST /gwan/memory/persist-simulated-snapshot
2. GET  /gwan/memory/sync-status
3. POST /gwan/memory/sync-jsonl-to-db
4. GET  /gwan/memory/sync-status
5. GET  /gwan/memory/db-query/action/send_micro_probe
```

This keeps the onboard-first idea clear: GWAN can record locally first, then synchronize to PostgreSQL when connection is available.

## 18. Long-term memory to onboard pull and recommendation

This prototype now supports the reverse direction of the Sync Layer.

Previous direction:

```text
JSONL local log -> PostgreSQL long-term memory
```

New direction:

```text
PostgreSQL long-term memory -> onboard GWAN knowledge package
```

New APIs:

```text
POST /gwan/sync/pull/manual
POST /gwan/sync/recommend
GET  /gwan/sync/recommendation-settings
POST /gwan/sync/recommendation-settings
```

Use this flow after PostgreSQL has at least one persisted MemorySnapshot:

```text
1. POST /gwan/memory/db-create-tables
2. POST /gwan/memory/db-persist-simulated-snapshot
3. POST /gwan/sync/pull/manual
4. POST /gwan/sync/recommend
```

Manual pull is for operator-requested search. Proactive recommendation is for GWAN to suggest useful long-term memory based on route, risk, uncertainty, and operator intent.

## 19. GitHub Actions CI

GWAN now has a GitHub Actions CI workflow.

```text
local pytest
→ GitHub Actions pytest
→ safer portfolio project
```

New file:

```text
.github/workflows/gwan-ci.yml
```

The workflow runs on:

```text
push
pull_request
workflow_dispatch
```

It checks:

```text
Python 3.13
pip install -r requirements.txt
pytest -q
required documentation files
```

CI uses SQLite for fast automated testing:

```text
DATABASE_URL=sqlite+pysqlite:////tmp/hyean-gwan-ci.db
```

PostgreSQL remains the local manual check for Docker Compose and long-term memory behavior.
