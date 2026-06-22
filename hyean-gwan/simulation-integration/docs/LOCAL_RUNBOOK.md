# HYEAN/GWAN Local Runbook

This runbook is the step-by-step local execution guide for the current GWAN prototype.

## 1. Clean install

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

Expected result:

```text
70 passed
```

## 2. Start PostgreSQL with Docker Compose

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

## 3. Confirm PostgreSQL user inside container

```bash
docker compose exec postgres psql -U hyean -d hyean_gwan -c "SELECT current_user;"
```

Expected result:

```text
current_user
--------------
hyean
```

## 4. Set DATABASE_URL

Use `127.0.0.1` and port `55432`.

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
echo $DATABASE_URL
```

## 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 6. Verify DB APIs in `/docs`

Run in this order:

```text
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
GET  /gwan/memory/db-status
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-snapshots
GET  /gwan/memory/db-query/high-risk
GET  /gwan/memory/db-query/high-uncertainty
GET  /gwan/memory/db-query/action/send_micro_probe
```

## 7. Reset everything

Use this when the DB state is confusing.

```bash
Ctrl + C  # stop uvicorn if running

docker compose down -v
docker compose up -d postgres
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
uvicorn app.main:app --reload
```

Then create tables again in `/docs`.

## 8. Quick terminal checks

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/gwan/memory/db-status | python3 -m json.tool
```

After tables and one simulated snapshot are created:

```bash
curl http://127.0.0.1:8000/gwan/memory/db-query/high-risk | python3 -m json.tool
```

## 9. Troubleshooting reminder

If FastAPI says:

```text
FATAL: role "hyean" does not exist
```

Check these in order:

1. `docker compose ps`
2. `docker compose exec postgres psql -U hyean -d hyean_gwan -c "SELECT current_user;"`
3. `echo $DATABASE_URL`
4. Make sure it uses `127.0.0.1:55432`, not `localhost:5432`.
5. Run `docker compose down -v` if old volume state is suspected.

## JSONL to PostgreSQL Sync Check

After PostgreSQL is running and tables are created, you can test the local-log sync path.

1. Create a local JSONL memory record:

```text
POST /gwan/memory/persist-simulated-snapshot
```

2. Check pending sync status:

```text
GET /gwan/memory/sync-status
```

Expected before sync:

```json
{
  "pending_snapshot_ids": ["memory-snapshot-sim-001"]
}
```

3. Sync JSONL to PostgreSQL:

```text
POST /gwan/memory/sync-jsonl-to-db
```

Example body:

```json
{
  "dry_run": false
}
```

4. Check status again:

```text
GET /gwan/memory/sync-status
```

Expected after sync:

```json
{
  "pending_snapshot_ids": [],
  "already_synced_snapshot_ids": ["memory-snapshot-sim-001"]
}
```

5. Query the synced database record:

```text
GET /gwan/memory/db-query/action/send_micro_probe
```

## 18. Check long-term memory pull back to onboard GWAN

After PostgreSQL is running and tables are created:

```text
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-simulated-snapshot
```

Then test manual pull:

```text
POST /gwan/sync/pull/manual
```

Example body:

```json
{
  "query_type": "high_risk",
  "limit": 5
}
```

Expected result:

```text
risk-radiation-critical-001
recommended_action: avoid
```

Then test proactive recommendation:

```text
POST /gwan/sync/recommend
```

Example body:

```json
{
  "operator_intent": "resource route planning",
  "predicted_route_object_ids": [
    "candidate-resource-stable-001",
    "risk-radiation-critical-001"
  ],
  "triggers": ["on_route_change"],
  "limit": 5
}
```

Expected result:

```text
candidate-resource-stable-001
risk-radiation-critical-001
```

This confirms that PostgreSQL long-term memory can be packaged back into onboard-useful knowledge.
