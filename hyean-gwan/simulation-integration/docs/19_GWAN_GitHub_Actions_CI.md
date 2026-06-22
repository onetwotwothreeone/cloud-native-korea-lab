# 19_GWAN_GitHub_Actions_CI

## Purpose

This step adds GitHub Actions CI for the HYEAN/GWAN prototype.

Previous state:

```text
The operator runs pytest manually on a local Mac.
```

New state:

```text
GitHub runs pytest automatically on push and pull request.
```

## Why this matters

HYEAN/GWAN now has simulation, scoring, memory persistence, PostgreSQL persistence, bidirectional sync, and documentation checks.

As the project grows, manual testing is no longer enough. CI makes the project safer and more portfolio-ready.

## Added file

```text
.github/workflows/gwan-ci.yml
```

## Workflow triggers

```text
push to main/master/feature/**
pull_request to main/master
manual workflow_dispatch
```

## What CI checks

1. Checkout repository
2. Install Python 3.13
3. Install `requirements.txt`
4. Run `pytest -q`
5. Confirm important docs exist

## CI environment

The workflow uses lightweight local paths so it does not require Docker or a real PostgreSQL server.

```text
HYEAN_MEMORY_JSONL_PATH=/tmp/hyean-gwan-memory.jsonl
DATABASE_URL=sqlite+pysqlite:////tmp/hyean-gwan-ci.db
```

This is intentional. Docker/PostgreSQL remains a local manual check, while CI verifies the code and documentation quickly.

## Why CI uses SQLite

PostgreSQL is still the target long-term memory database for the local prototype. However, for CI, SQLite is useful as a fast structural test database.

This keeps CI simple:

```text
fast
cheap
repeatable
no Docker service required
```

## Manual local check before pushing

Run this before pushing to GitHub:

```bash
source .venv/bin/activate
pytest -q
```

## Expected result

Before this step, the project had 94 passing tests.

After adding the CI workflow and CI documentation tests, the expected local result should increase after running the full project tests.

## Current limitation

This workflow does not deploy HYEAN/GWAN. It only validates tests and required documentation.

Deployment, Docker image build, GHCR push, Kubernetes manifest validation, and Argo CD checks can be added in later steps.

## Next recommended step

```text
20_GWAN_Docker_Image_Build_CI
```

That step should add Docker image build validation in GitHub Actions.
