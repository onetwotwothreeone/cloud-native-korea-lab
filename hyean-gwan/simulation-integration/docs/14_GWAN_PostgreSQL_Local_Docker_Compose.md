# 14_GWAN_PostgreSQL_Local_Docker_Compose

## Purpose

This step moves GWAN memory persistence from design-only PostgreSQL tables to a local runnable PostgreSQL environment.

The goal is not to remove JSONL yet. JSONL remains useful as a simple log. PostgreSQL is added for structured storage, query speed, relationships, and future service operation.

## What was added

```text
docker-compose.yml
.env.example
app/db/session.py
app/services/gwan_memory_postgres_persistence.py
tests/test_gwan_postgresql_local_docker_compose.py
```

## Local PostgreSQL start

```bash
docker compose up -d postgres
```

Check container:

```bash
docker compose ps
```

## Python setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment

```bash
cp .env.example .env
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@localhost:5432/hyean_gwan"
```

## Run tests

```bash
pytest -q
```

The tests use SQLite for fast structural checks, so Docker does not need to be running for the automated test suite.

## Run API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## New endpoints

```text
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-snapshot
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-snapshots
```

## Recommended manual check order

1. Start PostgreSQL with Docker Compose.
2. Run `GET /gwan/memory/db-status`.
3. Run `POST /gwan/memory/db-create-tables`.
4. Run `POST /gwan/memory/db-persist-simulated-snapshot`.
5. Run `GET /gwan/memory/db-snapshots`.

## What success means

If the simulated snapshot is persisted, GWAN memory can now move from an append-only JSONL file into relational tables:

```text
memory_snapshots
├─ observation_records
├─ score_records
├─ decision_records
├─ uncertainty_records
└─ map_update_records
```

## Current limitation

This is local development infrastructure only. It does not yet include production migration tooling, backups, authentication, cloud deployment, or monitoring.

## Next recommended step

15_GWAN_PostgreSQL_Query_API

This will query real PostgreSQL tables by object_id, risk score, uncertainty score, recommended_action, and map_layer.
