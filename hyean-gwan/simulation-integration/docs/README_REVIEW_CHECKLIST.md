# README Review Checklist

Use this checklist before sharing the HYEAN/GWAN prototype with another person.

## Project identity

- [ ] README says HYEAN is not a simple demo app.
- [ ] README says GWAN is the observation, interpretation, scoring, decision, and memory engine.
- [ ] README explains that this prototype uses synthetic/simulated data.
- [ ] README does not overclaim real spacecraft capability.

## Setup clarity

- [ ] Python setup command is included.
- [ ] `pytest -q` is included.
- [ ] Docker Compose setup is included.
- [ ] PostgreSQL uses host port `55432`.
- [ ] `DATABASE_URL` uses `127.0.0.1:55432`.

## API clarity

- [ ] API groups are listed.
- [ ] Recommended `/docs` execution order is listed.
- [ ] JSONL flow and PostgreSQL flow are separated.
- [ ] Query examples are included.
- [ ] Common troubleshooting cases are included.

## Portfolio readability

- [ ] A reviewer can understand the project in 3 minutes.
- [ ] A reviewer can run tests in one command.
- [ ] A reviewer can see how the system supports HYEAN/GWAN.
- [ ] A reviewer can see next steps.

## Step 17 Sync Checklist

- [ ] README explains JSONL to PostgreSQL sync.
- [ ] API reference includes `/gwan/memory/sync-status`.
- [ ] API reference includes `/gwan/memory/sync-jsonl-to-db`.
- [ ] Local runbook explains pending and already-synced snapshot IDs.
- [ ] Sync docs explain dry-run mode.

## Step 18 checklist

- [ ] README mentions long-term memory to onboard pull.
- [ ] API reference includes `/gwan/sync/pull/manual`.
- [ ] API reference includes `/gwan/sync/recommend`.
- [ ] API reference includes recommendation settings routes.
- [ ] Local runbook explains how to test manual pull and proactive recommendation.
