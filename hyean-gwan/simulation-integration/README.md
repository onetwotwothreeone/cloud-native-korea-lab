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
## 32. GWAN Kubernetes HPA Autoscaling Baseline

This step adds a baseline HorizontalPodAutoscaler for the GWAN API Deployment.

The HPA targets `deployment/gwan-api` and uses:

```text
minReplicas: 1
maxReplicas: 3
CPU averageUtilization: 70
```

Local check:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
```

Note: local Docker Desktop or kind clusters may show HPA CPU metrics as `<unknown>` unless metrics-server is installed. This step focuses on adding and validating the HPA object.


---

## 33. GWAN Kubernetes Metrics Server and HPA Readiness

This step checks the metrics side of HPA.

Step 32 added the `gwan-api-hpa` object. Step 33 explains and checks whether the Kubernetes cluster can provide CPU and memory usage through the Metrics API.

### Why this matters

HPA needs metrics to make scaling decisions.

```text
Metrics Server
→ Metrics API
→ HPA
→ Deployment replica count
```

If Metrics Server is missing, HPA can still exist, but CPU values may show `<unknown>`.

### Check locally

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
scripts/k8s/metrics_server_check.sh
```

Optional local install:

```bash
scripts/k8s/install_metrics_server_local.sh
scripts/k8s/metrics_server_check.sh
```

### Test

```bash
python -m pytest -q
```

## 34. GWAN Kubernetes HPA Behavior Policy

This step adds controlled HPA scaling behavior for the GWAN API.

The HPA now defines:

- scaleUp behavior
- scaleDown behavior
- stabilization windows
- Pod-based scaling policies

This prevents the GWAN API from scaling too aggressively.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
scripts/k8s/hpa_behavior_check.sh


## 35. GWAN Kubernetes PodDisruptionBudget

This step adds a PodDisruptionBudget for the GWAN API.

The PDB protects GWAN API availability during voluntary Kubernetes disruptions.

Current policy:

minAvailable: 1

Meaning:

- At least 1 GWAN API Pod should remain available during voluntary disruption.
- If GWAN API has only 1 replica, ALLOWED DISRUPTIONS may be 0.
- This is expected because the PDB is protecting the only available Pod.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/pdb_check.sh


## 35.1. GWAN Kubernetes HPA Behavior and PDB CI Checks

This step strengthens GWAN CI.

The workflow now explicitly checks:

- HPA behavior policy documentation
- PodDisruptionBudget documentation
- HPA behavior check script
- PDB check script

This makes sure the Kubernetes reliability rules are not only written, but also verified in CI.

## 35.2. HYEAN/GWAN Prevention Layer Alignment

This step aligns the current GWAN Kubernetes implementation with the updated Prevention Layer project source.

HYEAN/GWAN is not only a response system.

It is a prevention-oriented survival intelligence architecture.

GWAN should later expand beyond current risk scoring and include:

- trend_score
- imbalance_score
- early_warning_score
- recovery_capacity
- preventive_action_priority

This means Kubernetes work should be explained as preventive operational infrastructure.

Examples:

- HPA supports changing demand.
- HPA behavior policy prevents unstable scaling.
- PDB protects availability during voluntary disruption.
- NetworkPolicy will prevent unnecessary Pod communication risk.

Next step:

36_GWAN_Kubernetes_NetworkPolicy_Baseline

## 36. GWAN Kubernetes NetworkPolicy Baseline

This step adds baseline Kubernetes NetworkPolicy rules for GWAN.

NetworkPolicy is preventive communication control.

For HYEAN/GWAN, this means unnecessary Pod communication paths are reduced before they become operational risk paths.

Baseline:

- GWAN API allows ingress on TCP 8000.
- GWAN API allows egress to PostgreSQL on TCP 5432.
- GWAN API allows DNS egress on TCP/UDP 53.
- GWAN PostgreSQL allows ingress only from GWAN API on TCP 5432.

Important:

NetworkPolicy enforcement depends on the Kubernetes CNI plugin.
Local Docker Desktop or kind may create NetworkPolicy objects even if actual packet blocking is not enforced.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/network_policy_check.sh

## 37. GWAN Kubernetes ServiceAccount RBAC Baseline

This step adds dedicated Kubernetes ServiceAccounts and minimal RBAC baseline for GWAN.

ServiceAccount is the workload identity.
RBAC is the permission rule.

For HYEAN/GWAN, RBAC is preventive identity control.

Baseline:

- GWAN API uses gwan-api-sa.
- PostgreSQL uses gwan-postgres-sa.
- ServiceAccount token automount is false.
- Minimal Roles have no Kubernetes API permissions.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/rbac_check.sh

## 38. GWAN Kubernetes SecurityContext Baseline

This step adds Kubernetes SecurityContext baseline settings for GWAN.

SecurityContext is preventive runtime control.

For HYEAN/GWAN, this means containers should not run with unnecessary Linux privileges.

Baseline:

- GWAN API runs as non-root.
- GWAN API disables privilege escalation.
- GWAN API uses read-only root filesystem.
- GWAN API drops Linux capabilities.
- GWAN API mounts /tmp as emptyDir for temporary writes.
- PostgreSQL uses RuntimeDefault seccomp.
- PostgreSQL disables privilege escalation.
- PostgreSQL drops Linux capabilities.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/security_context_check.sh


## 39. GWAN Kubernetes Config and Secret Refinement

This step separates normal runtime configuration from sensitive credentials.

ConfigMap stores non-sensitive values:

- DATABASE_HOST
- DATABASE_PORT
- DATABASE_NAME
- DATABASE_DIALECT
- HYEAN_MEMORY_JSONL_PATH

Secret stores sensitive PostgreSQL credentials:

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

This keeps GWAN easier to move across local, staging, and production environments.

Local check:

```bash
scripts/k8s/config_secret_check.sh
```

Next step:

```text
40_GWAN_Kubernetes_PersistentVolume_Baseline
```

---

## 40_GWAN_Kubernetes_Persistence_Baseline

GWAN PostgreSQL now has a Kubernetes persistence baseline.

This step changes PostgreSQL storage from temporary emptyDir storage to a PersistentVolumeClaim.

Key files:

- k8s/base/postgres-pvc.yaml
- k8s/base/postgres-deployment.yaml
- scripts/k8s/persistence_check.sh
- docs/40_GWAN_Kubernetes_Persistence_Baseline.md

Check commands:

kubectl -n hyean-gwan get pvc
scripts/k8s/persistence_check.sh

Next step:

41_GWAN_Kubernetes_StatefulSet_Design_Review
## 41. GWAN Kubernetes StatefulSet Design Review

GWAN PostgreSQL persistence baseline was reviewed.

Current decision:

- Keep PostgreSQL as Deployment + PersistentVolumeClaim for the local baseline.
- Do not migrate to StatefulSet yet.
- Use this stage to confirm persistence, Secret, ConfigMap, RBAC, NetworkPolicy, SecurityContext, HPA, and PDB basics first.
- Plan StatefulSet migration later with backup and restore strategy.

Why this matters:

StatefulSet is better suited for stateful workloads, but it should not be added blindly.  
The project first records why the current architecture is acceptable and what must be prepared before migration.

Related files:

- `hyean-gwan/simulation-integration/docs/41_GWAN_Kubernetes_StatefulSet_Design_Review.md`
- `hyean-gwan/simulation-integration/codex/41_gwan_kubernetes_statefulset_design_review_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_design_review_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_design_review.py`
## 42. GWAN Kubernetes StatefulSet Migration Plan

GWAN PostgreSQL StatefulSet migration planning was added.

Current decision:

- Do not migrate PostgreSQL to StatefulSet yet.
- Keep the current Deployment + PVC baseline.
- Prepare backup, restore, rollback, and storage behavior review first.
- Treat StatefulSet migration as a controlled database migration, not a simple YAML replacement.

Why this matters:

A database workload must protect data first.  
Before changing the Kubernetes workload type, the project must prove that data can be backed up, restored, and safely rolled back.

Related files:

- `hyean-gwan/simulation-integration/docs/42_GWAN_Kubernetes_StatefulSet_Migration_Plan.md`
- `hyean-gwan/simulation-integration/codex/42_gwan_kubernetes_statefulset_migration_plan_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_migration_plan_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_migration_plan.py`

## 43. GWAN Kubernetes PostgreSQL Backup/Restore Baseline

GWAN PostgreSQL backup and restore baseline was added.

Current decision:

- PostgreSQL is still Deployment + PVC.
- StatefulSet migration is not applied yet.
- Backup is created with `pg_dump`.
- Restore is tested in a temporary database.
- Main database is not overwritten.
- Backup files are stored under `.local/postgres-backups` and excluded from Git.

Why this matters:

A database backup is only meaningful when restore also works.  
This step proves that GWAN can protect database data before attempting StatefulSet migration.

Related files:

- `hyean-gwan/simulation-integration/docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md`
- `hyean-gwan/simulation-integration/codex/43_gwan_kubernetes_postgresql_backup_restore_baseline_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/postgres_backup_restore_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_postgresql_backup_restore.py`

## 44. GWAN Kubernetes StatefulSet Draft Manifest

GWAN PostgreSQL StatefulSet draft manifest was added.

Current decision:

- PostgreSQL still runs as Deployment.
- StatefulSet is not applied yet.
- A draft Headless Service was created.
- A draft StatefulSet was created.
- The draft uses `volumeClaimTemplates`.
- The draft is kept outside active Kustomize overlays.

Why this matters:

StatefulSet migration should not be rushed.  
The project now has a safe draft manifest that can be reviewed before actual migration.

Related files:

- `hyean-gwan/simulation-integration/k8s/drafts/postgres-headless-service-draft.yaml`
- `hyean-gwan/simulation-integration/k8s/drafts/postgres-statefulset-draft.yaml`
- `hyean-gwan/simulation-integration/k8s/drafts/kustomization.yaml`
- `hyean-gwan/simulation-integration/docs/44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md`
- `hyean-gwan/simulation-integration/codex/44_gwan_kubernetes_statefulset_draft_manifest_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_draft_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_draft.py`

Next step:

- `45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run`

## 45. GWAN Kubernetes StatefulSet Migration Dry Run

GWAN PostgreSQL StatefulSet migration dry-run process was added.

Current decision:

- PostgreSQL is still running as Deployment.
- StatefulSet draft exists.
- StatefulSet is not applied yet.
- Backup/restore baseline exists.
- Migration readiness can now be checked safely.

Added files:

- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_migration_dry_run_check.sh`
- `hyean-gwan/simulation-integration/docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md`
- `hyean-gwan/simulation-integration/codex/45_gwan_kubernetes_statefulset_migration_dry_run_prompt.md`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_migration_dry_run.py`

Next step:

- `46_GWAN_Kubernetes_StatefulSet_Migration_Runbook`

## 46. GWAN Kubernetes StatefulSet Migration Runbook

GWAN PostgreSQL StatefulSet migration runbook was added.

This step does not execute the actual migration.

Added safety gates:

- test gate
- Kubernetes health gate
- backup/restore gate
- StatefulSet draft gate
- rollback plan
- stop conditions

Added files:

- `hyean-gwan/simulation-integration/docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md`
- `hyean-gwan/simulation-integration/codex/46_gwan_kubernetes_statefulset_migration_runbook_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_migration_runbook_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_migration_runbook.py`

Next step:

- `47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run`

## 47. GWAN Kubernetes StatefulSet Migration Rollback Dry Run

GWAN PostgreSQL StatefulSet rollback dry-run baseline was added.

This step checks rollback readiness without executing rollback or migration.

Added checks:

- current PostgreSQL Deployment exists
- current PostgreSQL PVC exists
- current PostgreSQL Service exists
- current PostgreSQL Secret exists
- StatefulSet draft renders
- backup/restore baseline exists
- migration runbook contains rollback safety rule
- real rollback is not executed
- real migration is not executed

Added files:

- `hyean-gwan/simulation-integration/docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md`
- `hyean-gwan/simulation-integration/codex/47_gwan_kubernetes_statefulset_migration_rollback_dry_run_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_migration_rollback_dry_run_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_migration_rollback_dry_run.py`

Next step:

- `48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist`

## 48. GWAN Kubernetes StatefulSet Migration Cutover Checklist

GWAN PostgreSQL StatefulSet migration cutover checklist was added.

This step prepares the final pre-cutover gate.

It does not execute real migration.

Checked conditions:

- PostgreSQL Deployment is available
- PostgreSQL Pod is running
- PostgreSQL PVC is Bound
- PostgreSQL Service exists
- PostgreSQL Secret exists
- GWAN API ConfigMap exists
- StatefulSet draft renders
- backup/restore baseline exists
- rollback dry run exists
- active StatefulSet does not exist yet
- manual GO/NO-GO decision is required

Added files:

- `hyean-gwan/simulation-integration/docs/48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md`
- `hyean-gwan/simulation-integration/codex/48_gwan_kubernetes_statefulset_migration_cutover_checklist_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_migration_cutover_checklist.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_migration_cutover_checklist.py`

Next step:

- `49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate`

## 51. GWAN Kubernetes StatefulSet Operator Approval Template

This step adds a manual operator approval template before any real PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION: NO_GO
- APPROVED_BY_OPERATOR: false
- FINAL_DECISION: NO_GO

The real migration is still blocked.

Next step:

52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record

## 52. GWAN Kubernetes StatefulSet Manual Approval Record

This step records the current manual approval state before any real PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION: NO_GO
- APPROVED_BY_OPERATOR: false
- FINAL_DECISION: NO_GO

The active PostgreSQL workload is still Deployment.

No real StatefulSet migration is executed in this step.

Next step:

53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template

## 55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review

This step adds the final approval review before any real PostgreSQL StatefulSet migration.

Safety rule:

- Do not execute real migration in this step.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Confirm that operator approval and required documents are still required.

## 56_GWAN_Kubernetes_StatefulSet_Final_Go_NoGo_Decision

This step records the final GO / NO-GO decision before any real PostgreSQL StatefulSet migration.

Current decision:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO

This step does not execute real migration.
PostgreSQL remains on the current Deployment + PVC baseline.

## 57_GWAN_Kubernetes_StatefulSet_Approved_Migration_Execution_Plan

This step documents the approved migration execution plan for a future PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO

This step does not execute real migration.
PostgreSQL remains on the current Deployment + PVC baseline.

## 58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run

This step documents and validates the dry-run command plan for a future PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO

This step does not execute real migration.
This step only checks that migration commands are prepared and safe to review.

## 59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review

This step reviews the command order for a future PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO
- COMMAND_REVIEW_STATUS=REVIEW_ONLY

This step does not execute real migration.
This step only reviews the prepared command plan.

## 60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register

This step creates a risk register before a future PostgreSQL Deployment to StatefulSet migration.

Current decision:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO
- RISK_REGISTER_STATUS=REVIEW_ONLY

This step does not execute real migration.
This step documents possible risks, prevention actions, and recovery actions.

### 61. GWAN Kubernetes StatefulSet Risk Mitigation Checklist

This step converts the migration risk register into a concrete mitigation checklist.

Current decision:

```text
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
REAL_MIGRATION_EXECUTED=false
```

Verified items:

- PostgreSQL Deployment is still active
- postgres-data PVC is Bound
- PostgreSQL Service exists
- PostgreSQL Secret exists
- GWAN API ConfigMap exists
- Active PostgreSQL StatefulSet does not exist yet
- Data loss risk is mitigated
- Downtime risk is mitigated
- Workload conflict risk is mitigated
- Rollback risk is mitigated
- Approval bypass risk is mitigated

Next step:

```text
62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot
```

### 62. GWAN Kubernetes StatefulSet Pre-Execution Safety Snapshot

This step creates a local safety snapshot before any real PostgreSQL StatefulSet migration.

Current decision:

~~~text
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
REAL_MIGRATION_EXECUTED=false
PREEXECUTION_SNAPSHOT_CREATED=true
SECRET_VALUES_EXPORTED=false
~~~

Verified items:

- PostgreSQL Deployment is available
- PostgreSQL Pod is running
- postgres-data PVC is Bound
- PostgreSQL Service exists
- PostgreSQL Secret metadata exists
- GWAN API ConfigMap exists
- Active PostgreSQL StatefulSet does not exist yet
- Secret values are not exported
- Real migration remains blocked

Snapshot location:

~~~text
.local/k8s-safety-snapshots/
~~~

Next step:

~~~text
63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check
~~~

## 63. GWAN Kubernetes StatefulSet Backup Freshness Check

This step checks whether a recent PostgreSQL backup exists before any real StatefulSet migration is considered.

Safety rules:

- real migration is not executed
- latest backup file must exist
- backup age must be within acceptable window
- PostgreSQL Deployment must still be available
- PostgreSQL PVC must be Bound
- secret values must not be exported
- FINAL_DECISION remains NO_GO

Next step:

64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check

## 64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check

This step adds a read-only data integrity check before any real PostgreSQL StatefulSet migration.

Safety status:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO
- DATA_INTEGRITY_STATUS=REVIEW_ONLY
- READ_ONLY_CHECK=true
- REAL_MIGRATION_EXECUTED=false
- SECRET_VALUES_EXPORTED=false

Checks:

- PostgreSQL Deployment
- PostgreSQL Pod
- postgres-data PVC
- PostgreSQL Service
- PostgreSQL Secret metadata
- GWAN API ConfigMap
- latest backup file
- pg_isready
- SELECT current_database()
- information_schema.tables
- local read-only integrity report

Next step:

- 65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary

## 66. GWAN Kubernetes StatefulSet Operator Final Approval Record

This step records the final operator approval state before PostgreSQL Deployment to StatefulSet migration.

Safety status:

- CURRENT_DECISION=NO_GO
- APPROVED_BY_OPERATOR=false
- FINAL_DECISION=NO_GO
- OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
- READINESS_STATUS=SUMMARY_ONLY
- BACKUP_FRESHNESS_STATUS=PASSED
- DATA_INTEGRITY_STATUS=PASSED
- READ_ONLY_CHECK=true
- REAL_MIGRATION_EXECUTED=false
- SECRET_VALUES_EXPORTED=false

This step does not execute real migration.

Next step:

- 67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate

## 68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check

- Purpose: PostgreSQL Deployment to StatefulSet migration 직전 최종 사전점검을 수행한다.
- Current decision: CURRENT_DECISION=NO_GO
- Approval: APPROVED_BY_OPERATOR=false
- Final gate: FINAL_APPROVAL_GATE_STATUS=BLOCKED
- Preflight: PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
- Execution: MIGRATION_EXECUTION_ALLOWED=false
- Safety: 실제 StatefulSet migration은 아직 실행하지 않는다.
- Portfolio meaning: 운영자가 승인하기 전에는 기술적으로 준비되어도 실제 인프라 변경을 막는 안전한 운영 구조를 증명한다.
- Next: 69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report
