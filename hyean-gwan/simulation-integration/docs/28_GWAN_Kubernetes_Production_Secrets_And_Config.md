# 28_GWAN_Kubernetes_Production_Secrets_And_Config

## Purpose

This step separates Kubernetes application configuration into ConfigMap and Secret resources.

Previous structure:

```text
Deployment env values
+ Secret only for password
```

Improved structure:

```text
ConfigMap = non-sensitive runtime configuration
Secret = sensitive runtime configuration
Deployment = references ConfigMap and Secret
```

## Why this matters

HYEAN/GWAN now runs through Docker, Docker Compose, GHCR, Kubernetes local overlays, kind CI, and production-like GHCR pull.

As the system moves closer to production-like deployment, runtime configuration should not be mixed directly into the Deployment manifest.

## What belongs in ConfigMap

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
HYEAN_MEMORY_JSONL_PATH
```

These values are configuration values. They are important, but they are not passwords.

## What belongs in Secret

```text
POSTGRES_PASSWORD
```

This is sensitive and should stay in a Kubernetes Secret.

## Database URL construction

The API deployment now builds `DATABASE_URL` from environment variables:

```text
postgresql+psycopg://$(DATABASE_USER):$(POSTGRES_PASSWORD)@$(DATABASE_HOST):$(DATABASE_PORT)/$(DATABASE_NAME)
```

This keeps the full database connection string out of the static Deployment manifest.

## New file

```text
k8s/base/gwan-api-configmap.yaml
```

## Updated files

```text
k8s/base/kustomization.yaml
k8s/base/gwan-api-deployment.yaml
```

## Manual check

```bash
kubectl kustomize k8s/overlays/local | grep -n "gwan-api-config" -A 20
kubectl apply -k k8s/overlays/local
kubectl -n hyean-gwan rollout status deployment/gwan-api --timeout=180s
```

## Success criteria

- `gwan-api-config` ConfigMap is rendered.
- Deployment uses `configMapKeyRef` for non-sensitive values.
- Deployment uses `secretKeyRef` for `POSTGRES_PASSWORD`.
- Local and production overlays still render correctly.
- API still responds through Kubernetes port-forward.
