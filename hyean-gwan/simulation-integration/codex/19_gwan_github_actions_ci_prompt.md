# Codex task: 19_GWAN_GitHub_Actions_CI

## Goal

Add GitHub Actions CI for the HYEAN/GWAN project.

## Required files

```text
.github/workflows/gwan-ci.yml
docs/19_GWAN_GitHub_Actions_CI.md
tests/test_gwan_github_actions_ci.py
README.md
```

## Workflow requirements

The workflow must:

1. Run on push, pull_request, and workflow_dispatch.
2. Use Python 3.13.
3. Install `requirements.txt`.
4. Run `pytest -q`.
5. Set CI-friendly environment variables:
   - `HYEAN_MEMORY_JSONL_PATH=/tmp/hyean-gwan-memory.jsonl`
   - `DATABASE_URL=sqlite+pysqlite:////tmp/hyean-gwan-ci.db`
6. Check that key documentation files exist.

## Success command

```bash
pytest -q
```

## Design rule

Do not require Docker or PostgreSQL service inside CI yet. PostgreSQL remains a local manual check. CI should stay fast and simple.
