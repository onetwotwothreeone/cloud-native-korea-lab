# 21_GWAN_Docker_Compose_CI

## Purpose

This step extends GWAN CI from a single-container Docker smoke test to a FastAPI container and PostgreSQL container integration check.  multi-container Docker Compose integration test.

Previous step:

```text
pytest
→ docker build
→ docker run single FastAPI container
→ /health check
```

This step:

```text
pytest
→ docker build
→ docker compose up API + PostgreSQL
→ /health check
→ /gwan/memory/db-status check
→ docker compose down cleanup
```

## Why this matters

GWAN memory features depend on both the FastAPI backend and PostgreSQL. A single-container smoke test proves that the API can start. Docker Compose CI proves that the API can also run beside the database service and reach it through the Compose network.

## Added files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/docker-compose.ci.yml
hyean-gwan/simulation-integration/tests/test_gwan_docker_compose_ci.py
hyean-gwan/simulation-integration/docs/21_GWAN_Docker_Compose_CI.md
hyean-gwan/simulation-integration/codex/21_gwan_docker_compose_ci_prompt.md
```

## Compose CI services

| Service | Purpose |
|---|---|
| `postgres` | PostgreSQL 16 database for GWAN memory checks |
| `api` | FastAPI GWAN backend built from the local Dockerfile |

## Important database URL difference

Local host access uses:

```text
127.0.0.1:55432
```

Inside Docker Compose, the API container reaches PostgreSQL by service name:

```text
postgres:5432
```

So the Compose CI API service uses:

```text
DATABASE_URL=postgresql+psycopg://hyean:hyean_password@postgres:5432/hyean_gwan
```

## CI behavior

The workflow checks:

```text
1. Python 3.13 setup
2. pip install -r requirements.txt
3. pytest -q
4. key docs exist
5. docker build
6. single-container /health smoke test
7. docker compose up -d --build
8. /health check through Compose
9. /gwan/memory/db-status check through Compose
10. docker compose down -v cleanup
```

## Manual local check

From the project folder:

```bash
docker compose -f docker-compose.ci.yml up -d --build
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
docker compose -f docker-compose.ci.yml down -v --remove-orphans
```

## Expected success signal

```text
/health returns HTTP 200
/gwan/memory/db-status returns HTTP 200
GitHub Actions shows green check
```

## Completion criteria

- Local `python -m pytest -q` passes.
- `docker-compose.ci.yml` defines API and PostgreSQL services.
- GitHub Actions runs Docker Compose integration check.
- `/gwan/memory/db-status` responds through the API container.
- Cleanup runs even if a previous step fails.
