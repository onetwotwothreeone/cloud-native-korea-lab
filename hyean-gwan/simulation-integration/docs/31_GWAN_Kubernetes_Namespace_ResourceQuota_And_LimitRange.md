# 31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange

## Purpose

This step adds a namespace-level resource boundary for the HYEAN/GWAN Kubernetes environment.

Previous steps added resource `requests` and `limits` directly to the `gwan-api` and `postgres` containers. That protects each Pod. This step protects the whole `hyean-gwan` namespace.

## Simple explanation

Think of the namespace as a small lab room.

- `ResourceQuota` is the total lab budget.
- `LimitRange` is the default rule for each machine in the lab.

This prevents one experiment from accidentally using too much CPU, memory, Pod count, or Kubernetes objects.

## Added Kubernetes objects

### ResourceQuota

File:

```text
k8s/base/resourcequota.yaml
```

Limits the namespace total:

```text
requests.cpu: 1
requests.memory: 1Gi
limits.cpu: 2
limits.memory: 2Gi
pods: 10
services: 4
secrets: 10
configmaps: 10
```

### LimitRange

File:

```text
k8s/base/limitrange.yaml
```

Defines default container boundaries:

```text
default cpu: 500m
default memory: 512Mi
defaultRequest cpu: 100m
defaultRequest memory: 128Mi
min cpu: 50m
min memory: 64Mi
max cpu: 1
max memory: 1Gi
```

## How to apply locally

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/namespace_policy_check.sh
```

## What to check

```bash
kubectl -n hyean-gwan get resourcequota
kubectl -n hyean-gwan describe resourcequota hyean-gwan-resource-quota
kubectl -n hyean-gwan get limitrange
kubectl -n hyean-gwan describe limitrange hyean-gwan-default-container-limits
```

## Why this matters

This is a small but important operations step. HYEAN/GWAN is not only an API; it is becoming a deployable cloud-native system. A deployable system needs boundaries.

Resource requests and limits define container-level expectations. ResourceQuota and LimitRange define namespace-level guardrails.
