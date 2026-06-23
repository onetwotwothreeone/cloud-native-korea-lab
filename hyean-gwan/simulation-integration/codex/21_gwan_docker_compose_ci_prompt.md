# Codex task: 21_GWAN_Docker_Compose_CI

## Goal

Extend GWAN CI so GitHub Actions verifies API + PostgreSQL together with Docker Compose.

## Required files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/docker-compose.ci.yml
hyean-gwan/simulation-integration/tests/test_gwan_docker_compose_ci.py
hyean-gwan/simulation-integration/docs/21_GWAN_Docker_Compose_CI.md
```

## Requirements

- Keep Python 3.13 tests.
- Keep Docker image build check.
- Keep single-container `/health` smoke test.
- Add Docker Compose integration test using `docker-compose.ci.yml`.
- Compose must run `postgres` and `api` services.
- API must use `DATABASE_URL=postgresql+psycopg://hyean:hyean_password@postgres:5432/hyean_gwan`.
- CI must check `/health` and `/gwan/memory/db-status`.
- CI must always run `docker compose down -v --remove-orphans` for cleanup.

## Success criteria

```bash
python -m pytest -q
```

GitHub Actions should show green check after push.
