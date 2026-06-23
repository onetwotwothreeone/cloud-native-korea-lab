# HYEAN / GWAN Prototype

HYEAN is a survival-oriented space intelligence service for mobile human habitats.

GWAN is the core observation, interpretation, scoring, decision, and memory engine inside HYEAN.

This repository is the current backend prototype for GWAN simulation, scoring, memory, persistence, and query workflows.

## Beginner summary

This project asks a simple question:

```text
If a mobile human habitat is traveling through space,
how can it observe nearby objects,
score risks/resources/uncertainty,
recommend actions,
and remember what it learned?
```

Current prototype flow:

```text
Synthetic space scenario
→ GWAN scoring rule
→ recommended action
→ Operator Interface payload
→ MemorySnapshot
→ JSONL or PostgreSQL storage
→ memory query API
```

## What this prototype can do now

- Validate GWAN → HYEAN Operator Interface payloads
- Generate simulated space scenarios
- Score resource, risk, exploration value, uncertainty, and survival priority
- Recommend actions such as `avoid`, `observe_more`, `send_micro_probe`, and `update_survival_map`
- Convert simulation results into MemorySnapshot records
- Save memory to JSONL
- Query JSONL memory
- Design PostgreSQL tables
- Run local PostgreSQL through Docker Compose
- Persist MemorySnapshot records to PostgreSQL
- Query PostgreSQL memory records by risk, uncertainty, object ID, and recommended action

## Important limitation

This prototype uses synthetic and simulated data only.

It does **not** claim real spacecraft control, real sensor integration, or confirmed scientific discovery.

The goal is to make GWAN's data contract, scoring behavior, uncertainty handling, memory structure, and API workflow testable.

## Current test status

```bash
pytest -q
```

Expected result:

```text
70 passed
```

## Project structure

```text
app/
  api/routes_gwan.py
  db/gwan_memory_models.py
  db/session.py
  schemas/gwan_interface.py
  services/gwan_scoring.py
  services/gwan_simulation.py
  services/gwan_memory.py
  services/gwan_memory_persistence.py
  services/gwan_memory_query.py
  services/gwan_memory_postgres_design.py
  services/gwan_memory_postgres_persistence.py
  services/gwan_memory_postgres_query.py

docs/
  API_REFERENCE.md
  LOCAL_RUNBOOK.md
  README_REVIEW_CHECKLIST.md
  troubleshooting/

tests/
  fixtures/
  test_*.py

docker-compose.yml
requirements.txt
pyproject.toml
```

## Quick start: Python only

This checks the code without Docker.

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

Expected:

```text
70 passed
```

## Quick start: FastAPI docs

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Quick start: PostgreSQL with Docker Compose

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

Set the database URL:

```bash
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
```

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Recommended `/docs` execution order

### 1. Basic API check

```text
GET /health
```

### 2. Simulation and scoring

```text
POST /gwan/simulate-integrated
GET  /gwan/scoring-test-cases
```

### 3. Memory snapshot

```text
GET /gwan/memory/simulated-snapshot
```

### 4. JSONL persistence and query

```text
POST /gwan/memory/persist-simulated-snapshot
GET  /gwan/memory/persistence-status
GET  /gwan/memory/query/high-risk
GET  /gwan/memory/query/high-uncertainty
GET  /gwan/memory/query/object/candidate-ice-weak-signal-001
```

### 5. PostgreSQL design and persistence

```text
GET  /gwan/memory/postgres-design
GET  /gwan/memory/postgres-insert-plan
GET  /gwan/memory/db-status
POST /gwan/memory/db-create-tables
POST /gwan/memory/db-persist-simulated-snapshot
GET  /gwan/memory/db-snapshots
```

### 6. PostgreSQL query

```text
GET /gwan/memory/db-query/high-risk
GET /gwan/memory/db-query/high-uncertainty
GET /gwan/memory/db-query/object/candidate-ice-weak-signal-001
GET /gwan/memory/db-query/action/send_micro_probe
```

## API documentation

See:

```text
docs/API_REFERENCE.md
docs/LOCAL_RUNBOOK.md
```

## Key object IDs for checking results

| Object ID | Meaning | Expected action |
|---|---|---|
| `candidate-resource-stable-001` | Stable resource candidate | `send_micro_probe` |
| `risk-radiation-critical-001` | High-risk radiation region | `avoid` |
| `candidate-ice-weak-signal-001` | Weak signal / uncertain resource candidate | `observe_more` |
| `nav-reference-stable-001` | Stable navigation reference | `update_survival_map` |

## Common troubleshooting

### `docker: command not found`

Docker Desktop may be running, but the Docker CLI may not be on PATH.

Check Docker Desktop CLI settings or add the CLI path to your shell.

### `FATAL: role "hyean" does not exist`

Most likely FastAPI is reaching the wrong PostgreSQL server or an old Docker volume.

Fix:

```bash
docker compose down -v
docker compose up -d postgres
export DATABASE_URL="postgresql+psycopg://hyean:hyean_password@127.0.0.1:55432/hyean_gwan"
uvicorn app.main:app --reload
```

See:

```text
docs/troubleshooting/2026-06-22_postgres_role_and_port_troubleshooting.md
```

## Current implementation steps

```text
05 Data Contract
→ 06 Pydantic Models
→ 07 First Simulation Logic
→ 08 Scoring Test Cases
→ 09 Simulation + Scoring Integration
→ 10 Memory Map Update Model
→ 11 Memory Persistence JSONL
→ 12 Memory Query API
→ 13 Memory PostgreSQL Design
→ 14 PostgreSQL Local Docker Compose
→ 15 PostgreSQL Query API
→ 16 API Documentation and README Polish
```

## Next recommended step

```text
17_GWAN_GitHub_Actions_CI
```

The project now has enough tests and documentation to benefit from automated CI. The next step should run `pytest -q` automatically on every push or pull request.

## 17. JSONL local log to PostgreSQL sync

GWAN now supports the first Sync Layer behavior.

```text
local JSONL memory log
→ sync missing snapshots
→ PostgreSQL long-term memory database
```

New APIs:

```text
GET  /gwan/memory/sync-status
POST /gwan/memory/sync-jsonl-to-db
```

Recommended check:

```text
1. POST /gwan/memory/persist-simulated-snapshot
2. GET  /gwan/memory/sync-status
3. POST /gwan/memory/sync-jsonl-to-db
4. GET  /gwan/memory/sync-status
5. GET  /gwan/memory/db-query/action/send_micro_probe
```

This keeps the onboard-first idea clear: GWAN can record locally first, then synchronize to PostgreSQL when connection is available.

## 18. Long-term memory to onboard pull and recommendation

This prototype now supports the reverse direction of the Sync Layer.

Previous direction:

```text
JSONL local log -> PostgreSQL long-term memory
```

New direction:

```text
PostgreSQL long-term memory -> onboard GWAN knowledge package
```

New APIs:

```text
POST /gwan/sync/pull/manual
POST /gwan/sync/recommend
GET  /gwan/sync/recommendation-settings
POST /gwan/sync/recommendation-settings
```

Use this flow after PostgreSQL has at least one persisted MemorySnapshot:

```text
1. POST /gwan/memory/db-create-tables
2. POST /gwan/memory/db-persist-simulated-snapshot
3. POST /gwan/sync/pull/manual
4. POST /gwan/sync/recommend
```

Manual pull is for operator-requested search. Proactive recommendation is for GWAN to suggest useful long-term memory based on route, risk, uncertainty, and operator intent.

## 19. GitHub Actions CI

GWAN now has a GitHub Actions CI workflow.

```text
local pytest
→ GitHub Actions pytest
→ safer portfolio project
```

New file:

```text
.github/workflows/gwan-ci.yml
```

The workflow runs on:

```text
push
pull_request
workflow_dispatch
```

It checks:

```text
Python 3.13
pip install -r requirements.txt
pytest -q
required documentation files
```

CI uses SQLite for fast automated testing:

```text
DATABASE_URL=sqlite+pysqlite:////tmp/hyean-gwan-ci.db
```

PostgreSQL remains the local manual check for Docker Compose and long-term memory behavior.

## 20. Docker image build CI

GWAN CI now verifies not only Python tests but also Docker image packaging.

```text
pytest -q
→ docker build
→ docker run
→ curl /health
```

Important: GitHub Actions workflows must live at the repository root.

```text
.github/workflows/gwan-ci.yml
```

The Docker build context is:

```text
hyean-gwan/simulation-integration
```

Manual local check:

```bash
cd hyean-gwan/simulation-integration
docker build -t hyean-gwan-simulation:local .
docker run --rm -p 8000:8000 hyean-gwan-simulation:local
```

Then check:

```text
http://127.0.0.1:8000/health
```

## 20. Docker image build CI

GWAN CI now verifies not only Python tests but also Docker image packaging.

```text
pytest -q
→ docker build
→ docker run
→ curl /health
```

Important: GitHub Actions workflows must live at the repository root.

```text
.github/workflows/gwan-ci.yml
```

The Docker build context is:

```text
hyean-gwan/simulation-integration
```

Manual local check:

```bash
cd hyean-gwan/simulation-integration
docker build -t hyean-gwan-simulation:local .
docker run --rm -p 8000:8000 hyean-gwan-simulation:local
```

Then check:

```text
http://127.0.0.1:8000/health
```

## 21. Docker Compose CI

GWAN CI now verifies the API and PostgreSQL together with Docker Compose.

```text
pytest -q
→ docker build
→ docker run /health
→ docker compose up API + PostgreSQL
→ /health
→ /gwan/memory/db-status
```

Manual local check:

```bash
cd hyean-gwan/simulation-integration
docker compose -f docker-compose.ci.yml up -d --build
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
docker compose -f docker-compose.ci.yml down -v --remove-orphans
```

This step proves that the FastAPI container and PostgreSQL container can run together through Docker Compose.

## 22. GHCR image push

GWAN CI now publishes the tested Docker image to GitHub Container Registry.

```text
pytest
→ Docker build
→ container smoke test
→ Docker Compose API + PostgreSQL test
→ GHCR image push
```

Image name:

```text
ghcr.io/<github-owner>/hyean-gwan-simulation
```

The workflow pushes images only on `push` to `main`. Pull requests still run tests and builds, but do not push images.

After the workflow passes, check:

```text
GitHub repository → Packages → hyean-gwan-simulation
```

## 23. GWAN Kubernetes manifests

This step adds the first Kubernetes manifests for the GWAN simulation integration prototype.

The manifests are under:

```text
k8s/base/
```

They define:

```text
Namespace
PostgreSQL Secret
PostgreSQL Service
PostgreSQL Deployment
GWAN API Service
GWAN API Deployment
Kustomization entrypoint
```

Local check with kubectl and kustomize-compatible rendering:

```bash
kubectl kustomize k8s/base
```

Apply to a local Kubernetes cluster, such as Docker Desktop Kubernetes, only after confirming the GHCR image is available:

```bash
kubectl apply -k k8s/base
kubectl -n hyean-gwan get pods
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
curl http://127.0.0.1:8000/health
```

This step begins the Kubernetes path after Docker image build, Docker Compose CI, and GHCR image push.

## 24. GWAN Kubernetes local run

This step adds a local Kubernetes runbook and helper scripts for the GWAN API and PostgreSQL manifests.

Manual check:

```bash
cd hyean-gwan/simulation-integration
kubectl kustomize k8s/base
kubectl apply -k k8s/base
kubectl -n hyean-gwan rollout status deployment/postgres --timeout=180s
kubectl -n hyean-gwan rollout status deployment/gwan-api --timeout=180s
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
```

In another terminal:

```bash
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
```

Scripted check:

```bash
scripts/k8s/apply_local.sh
scripts/k8s/status.sh
scripts/k8s/port_forward_health_check.sh
scripts/k8s/cleanup_local.sh
```

## 25. GWAN Kubernetes overlays: local and production

This step separates Kubernetes configuration by environment.

```text
k8s/base
k8s/overlays/local
k8s/overlays/production
```

Local Docker Desktop Kubernetes should use the local overlay:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
```

The local overlay sets:

```text
imagePullPolicy: Never
```

Production-like deployment should use the production overlay:

```bash
kubectl apply -k k8s/overlays/production
```

The production overlay keeps:

```text
imagePullPolicy: IfNotPresent
```

This prevents local-only image settings from leaking into production-like manifests.

## 26. Kubernetes CI with kind

GWAN now validates Kubernetes manifests inside GitHub Actions by creating a temporary kind cluster.

The workflow now checks:

```text
Python tests
Docker build
Docker Compose API + PostgreSQL integration
kind cluster creation
Docker image loaded into kind
kubectl apply -k k8s/overlays/local
PostgreSQL rollout
GWAN API rollout
/health check through port-forward
/gwan/memory/db-status check through port-forward
```

This means Kubernetes validation no longer depends only on the local Docker Desktop cluster.
GitHub Actions can now create a disposable Kubernetes cluster and verify that the GWAN manifests work.

## 27. Kubernetes production GHCR pull

The project now validates the production-style Kubernetes path.

Local/kind CI path:

```text
Build image in CI
→ kind load docker-image
→ k8s/overlays/local
```

Production-style path:

```text
Build and push image to GHCR
→ create Kubernetes ghcr-pull-secret
→ k8s/overlays/production
→ Kubernetes pulls the image from GHCR
```

New files:

```text
k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml
docs/27_GWAN_Kubernetes_Production_GHCR_Pull.md
tests/test_gwan_kubernetes_production_ghcr_pull.py
```

Manual production-like check:

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl -n hyean-gwan create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  --docker-email=YOUR_EMAIL
kubectl apply -k k8s/overlays/production
```

## 28. Kubernetes production secrets and config

GWAN Kubernetes configuration now separates runtime settings into ConfigMap and Secret.

```text
ConfigMap = non-sensitive settings
Secret = sensitive settings
Deployment = references both
```

New file:

```text
k8s/base/gwan-api-configmap.yaml
```

ConfigMap values:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
HYEAN_MEMORY_JSONL_PATH
```

Secret value:

```text
POSTGRES_PASSWORD
```

The API Deployment now composes `DATABASE_URL` from environment variables instead of hardcoding the full connection string in one line.

Check:

```bash
kubectl kustomize k8s/overlays/local
kubectl kustomize k8s/overlays/production
python -m pytest -q
```

## 29. Kubernetes health, readiness, and observability baseline

This step adds the first Kubernetes operations baseline for GWAN.

It adds:

```text
startupProbe
readinessProbe
livenessProbe
rollout check script
health/readiness check script
diagnostics script
```

Local check:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
```

In another terminal:

```bash
scripts/k8s/health_readiness_check.sh
```

If something fails:

```bash
scripts/k8s/diagnostics.sh
```

## 30. Kubernetes resource requests and limits

This step adds baseline Kubernetes CPU and memory requests/limits for the GWAN API and PostgreSQL pods.

```text
requests = minimum resources Kubernetes should reserve
limits   = maximum resources the container should be allowed to use
```

Local check:

```bash
cd hyean-gwan/simulation-integration
python -m pytest -q

docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/resource_check.sh
```

This helps GWAN move from "it runs" to "it runs with an explicit resource baseline."


## 31. GWAN Kubernetes Namespace ResourceQuota and LimitRange

This step adds namespace-level resource boundaries for the HYEAN/GWAN Kubernetes environment.

Added files:

```text
k8s/base/resourcequota.yaml
k8s/base/limitrange.yaml
scripts/k8s/namespace_policy_check.sh
docs/31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange.md
```

Local check:

```bash
cd hyean-gwan/simulation-integration

docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/namespace_policy_check.sh
```

Simple meaning:

```text
ResourceQuota = total resource fence for the namespace
LimitRange = default resource rule for containers
```


## 31. GWAN Kubernetes Namespace ResourceQuota and LimitRange

This step adds namespace-level resource boundaries for the HYEAN/GWAN Kubernetes environment.

Added files:

```text
k8s/base/resourcequota.yaml
k8s/base/limitrange.yaml
scripts/k8s/namespace_policy_check.sh
docs/31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange.md
```

Local check:

```bash
cd hyean-gwan/simulation-integration

docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/namespace_policy_check.sh
```

Simple meaning:

```text
ResourceQuota = total resource fence for the namespace
LimitRange = default resource rule for containers
```
