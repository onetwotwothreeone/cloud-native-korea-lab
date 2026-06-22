# Codex task: 16_GWAN_API_Documentation_and_README_Polish

## Goal

Polish the HYEAN/GWAN README and API documentation after PostgreSQL Query API was added.

## Add or update files

```text
README.md
docs/API_REFERENCE.md
docs/LOCAL_RUNBOOK.md
docs/README_REVIEW_CHECKLIST.md
docs/16_GWAN_API_Documentation_and_README_Polish.md
tests/test_gwan_api_documentation.py
```

## Requirements

1. README must explain HYEAN/GWAN in beginner-readable language.
2. README must show Python-only setup.
3. README must show Docker Compose PostgreSQL setup.
4. README must use port `55432` for PostgreSQL.
5. API reference must list all current routes.
6. Local runbook must include `/docs` verification order.
7. Troubleshooting must mention `FATAL: role "hyean" does not exist`.
8. Add tests that check documentation contains critical endpoints and commands.

## Success command

```bash
pytest -q
```
