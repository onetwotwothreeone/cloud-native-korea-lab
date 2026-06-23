# 23_GWAN_Kubernetes_Manifests

## Purpose

This step adds the first Kubernetes manifests for the GWAN simulation integration prototype.

Previous steps proved:

```text
pytest CI
Docker image build CI
Docker Compose CI
GHCR image push
```

This step prepares the next runtime target:

```text
GHCR image
→ Kubernetes Deployment
→ Kubernetes Service
→ /health check through port-forward
```

## What changed

New files:

```text
k8s/base/namespace.yaml
k8s/base/postgres-secret.yaml
k8s/base/postgres-service.yaml
k8s/base/postgres-deployment.yaml
k8s/base/gwan-api-service.yaml
k8s/base/gwan-api-deployment.yaml
k8s/base/kustomization.yaml
tests/test_gwan_kubernetes_manifests.py
```

## Kubernetes objects

| Object | Purpose |
|---|---|
| Namespace `hyean-gwan` | Isolated Kubernetes space for the prototype |
| Secret `gwan-postgres-secret` | PostgreSQL user, password, and DB name |
| Service `postgres` | Stable internal address for PostgreSQL |
| Deployment `postgres` | Runs the PostgreSQL container |
| Service `gwan-api` | Stable internal address for FastAPI |
| Deployment `gwan-api` | Runs the GWAN API container from GHCR |
| Kustomization | One entrypoint for `kubectl apply -k` |

## Important concept

In Docker Compose, the API connects to PostgreSQL through:

```text
postgres:5432
```

In Kubernetes, the API also connects to PostgreSQL through the Service name:

```text
postgres:5432
```

This is different from local host access:

```text
127.0.0.1:55432
```

## Local check

Render manifests before applying:

```bash
kubectl kustomize k8s/base
```

Apply to local Kubernetes:

```bash
kubectl apply -k k8s/base
kubectl -n hyean-gwan get pods
kubectl -n hyean-gwan get svc
```

Port-forward the API:

```bash
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
curl http://127.0.0.1:8000/health
```

## Current limitation

This is a first local/dev Kubernetes manifest set. It uses `emptyDir` for PostgreSQL data, so data disappears when the Pod is recreated.

Later versions should add:

```text
PersistentVolumeClaim
Kustomize overlays for dev/staging/prod
GHCR image tag pinning
Kubernetes CI with kind
Ingress
Resource requests and limits
```

## Completion criteria

- Kubernetes manifests exist under `k8s/base`.
- `kustomization.yaml` includes API and PostgreSQL resources.
- GWAN API image points to GHCR.
- API connects to PostgreSQL through Kubernetes Service DNS.
- Tests confirm the manifest structure.
