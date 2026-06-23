# 25_GWAN_Kubernetes_Overlays_Local_And_Production

## Purpose

This step separates Kubernetes configuration by environment.

Step 24 proved that the GWAN API and PostgreSQL can run on local Docker Desktop Kubernetes. During that test, GHCR image pulling failed because the package was private. The local workaround was to build the image on the Mac and set:

```text
imagePullPolicy: Never
```

That is correct for local practice, but it should not be the shared base manifest or production behavior.

## What changed

New overlay directories:

```text
k8s/overlays/local
k8s/overlays/production
```

The base manifest is restored to:

```text
imagePullPolicy: IfNotPresent
```

The local overlay patches the API deployment to:

```text
imagePullPolicy: Never
```

The production overlay keeps:

```text
imagePullPolicy: IfNotPresent
```

## Why this matters

The same Kubernetes system must support different execution situations:

| Environment | Image source | Pull policy |
|---|---|---|
| local Docker Desktop | Mac local Docker image | `Never` |
| production-like | GHCR image | `IfNotPresent` |

Without overlays, a setting that helps local practice can accidentally break production-like deployment.

## New usage

Local Docker Desktop:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
```

Production-like:

```bash
kubectl apply -k k8s/overlays/production
```

## Updated scripts

The local helper scripts now use:

```text
k8s/overlays/local
```

Specifically:

```text
scripts/k8s/apply_local.sh
scripts/k8s/cleanup_local.sh
```

## Completion criteria

- `k8s/base` remains shared and production-safe.
- `k8s/overlays/local` exists and sets `imagePullPolicy: Never`.
- `k8s/overlays/production` exists and sets `imagePullPolicy: IfNotPresent`.
- Local scripts use `k8s/overlays/local`.
- Tests confirm overlay structure and key image pull policies.
