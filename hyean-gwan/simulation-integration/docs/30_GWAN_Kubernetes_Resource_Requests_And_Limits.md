# 30_GWAN_Kubernetes_Resource_Requests_And_Limits

## Purpose

This step adds baseline Kubernetes CPU and memory requests/limits for the GWAN API and PostgreSQL pods.

Previous step:

```text
Kubernetes can run GWAN and basic health checks can verify it.
```

This step:

```text
Kubernetes can also understand how much CPU/memory GWAN expects and how much it is allowed to use.
```

## Beginner explanation

Kubernetes resources are like a desk reservation in a shared study room.

- `requests` means: please reserve at least this much room for me.
- `limits` means: do not let me use more than this much room.

Without these values, Kubernetes can run the pod, but it has less information for scheduling and resource control.

## Added resource baseline

### gwan-api

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

### postgres

```yaml
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

## Why PostgreSQL has more memory request than the API

The API mostly handles HTTP requests and GWAN simulation logic.

PostgreSQL keeps database pages, query execution memory, and connection state, so its baseline memory request is slightly higher.

## Local check

Render manifests:

```bash
kubectl kustomize k8s/overlays/local
```

Apply local overlay:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/resource_check.sh
```

## Useful kubectl commands

```bash
kubectl -n hyean-gwan describe deployment gwan-api
kubectl -n hyean-gwan describe deployment postgres
kubectl -n hyean-gwan top pods
```

`kubectl top pods` requires Metrics Server. If Metrics Server is not installed, use `kubectl describe` and manifest rendering first.

## Completion criteria

- `gwan-api` has CPU/memory requests and limits.
- `postgres` has CPU/memory requests and limits.
- Local and production overlays still render.
- Kubernetes rollout still succeeds.
- CI checks the new resource baseline document.
