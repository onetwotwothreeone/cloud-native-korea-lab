# Troubleshooting Log: PostgreSQL role and port conflict

Date: 2026-06-22
Project: HYEAN / GWAN
Step: 14_GWAN_PostgreSQL_Local_Docker_Compose

## 1. Problem

Python tests passed, Docker Desktop was running, and the PostgreSQL container started successfully. However, the FastAPI database status endpoint returned a connection failure.

Main error:

```text
FATAL: role "hyean" does not exist
```

## 2. What this meant

FastAPI tried to connect to PostgreSQL as the `hyean` database user, but the PostgreSQL server it reached did not have that role.

The confusing part was that Docker PostgreSQL did have the `hyean` role when checked from inside the container.

## 3. Root cause

The most likely cause was local port confusion on `localhost:5432`.

Docker PostgreSQL was correct inside the container, but FastAPI was probably reaching a different PostgreSQL server or a stale local connection through port `5432`.

## 4. Evidence

Docker internal check succeeded:

```bash
docker compose exec postgres psql -U hyean -d hyean_gwan -c "SELECT current_user;"
```

Expected result:

```text
current_user
--------------
hyean
```

FastAPI still failed through the original `DATABASE_URL` using `localhost:5432`.

## 5. Fix

Change the Docker Compose host port from `5432` to `55432`.

```yaml
ports:
  - "55432:5432"
```

Then reset the volume and restart PostgreSQL:

```bash
docker compose down -v
docker compose up -d postgres
```

Set the FastAPI database URL to the new host port:

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
```

Restart FastAPI:

```bash
uvicorn app.main:app --reload
```

## 6. Result

After changing the external port to `55432`, FastAPI connected successfully and the simulated MemorySnapshot was persisted to PostgreSQL.

Successful response included:

```json
{
  "snapshot_id": "memory-snapshot-sim-001",
  "inserted": true,
  "table_counts": {
    "memory_snapshots": 1,
    "observation_records": 4,
    "score_records": 4,
    "decision_records": 4,
    "uncertainty_records": 1,
    "map_update_records": 4
  },
  "message": "MemorySnapshot persisted to database."
}
```

## 7. Prevention

Use `55432:5432` for the local PostgreSQL Docker Compose mapping to avoid conflicts with any existing Mac PostgreSQL process.

Use `127.0.0.1` instead of `localhost` in `DATABASE_URL` for clearer local TCP routing:

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
```

## 8. Learning point

A running Docker container does not always mean FastAPI is connecting to that exact database. Always check:

1. Container health
2. Internal database user
3. Host port mapping
4. `DATABASE_URL`
5. FastAPI connection status
