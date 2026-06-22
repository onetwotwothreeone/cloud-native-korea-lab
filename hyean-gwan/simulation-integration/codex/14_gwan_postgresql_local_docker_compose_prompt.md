# Codex task: 14_GWAN_PostgreSQL_Local_Docker_Compose

## Goal

Add local PostgreSQL support for GWAN memory persistence using Docker Compose and SQLAlchemy.

## Required files

```text
docker-compose.yml
.env.example
app/db/session.py
app/services/gwan_memory_postgres_persistence.py
tests/test_gwan_postgresql_local_docker_compose.py
docs/14_GWAN_PostgreSQL_Local_Docker_Compose.md
README.md
requirements.txt
pyproject.toml
```

## Required API endpoints

```text
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-snapshot
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-snapshots
```

## Success command

```bash
pytest -q
```

## Manual local check

```bash
docker compose up -d postgres
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@localhost:5432/hyean_gwan"
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` and run the DB endpoints.
