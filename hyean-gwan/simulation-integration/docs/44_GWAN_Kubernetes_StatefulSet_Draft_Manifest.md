# 44. GWAN Kubernetes StatefulSet Draft Manifest

## Purpose

This step creates a draft Kubernetes StatefulSet manifest for GWAN PostgreSQL.

This does not migrate the running database yet.

## Simple Explanation

Deployment is like a worker that can be replaced freely.

StatefulSet is like a worker with a fixed name tag and a fixed storage locker.

A database needs a stable identity and stable storage, so StatefulSet is usually a better long-term fit than Deployment.

## Current State

GWAN PostgreSQL currently runs as:

- Deployment
- Service
- Secret
- PVC

This is still active and unchanged.

## Draft Added

This step adds:

- `k8s/drafts/postgres-headless-service-draft.yaml`
- `k8s/drafts/postgres-statefulset-draft.yaml`
- `k8s/drafts/kustomization.yaml`

## Important Safety Rule

The StatefulSet draft is not included in:

- `k8s/base/kustomization.yaml`
- `k8s/overlays/local/kustomization.yaml`
- production overlay

So it is not applied automatically.

## Why Headless Service Exists

StatefulSet uses a governing service to provide stable network identity for Pods.

The draft uses:

- Service name: `postgres-headless`
- StatefulSet serviceName: `postgres-headless`

## Why volumeClaimTemplates Exists

StatefulSet should create stable per-Pod PVCs through `volumeClaimTemplates`.

The draft uses:

- volumeClaimTemplates name: `postgres-data`
- generated PVC pattern later: `postgres-data-postgres-0`

## Migration Decision

Do not apply this StatefulSet directly yet.

Before migration, the project must define:

1. final backup
2. restore verification
3. old Deployment scale-down
4. StatefulSet apply
5. health check
6. rollback plan

## Next Recommended Step

45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run
