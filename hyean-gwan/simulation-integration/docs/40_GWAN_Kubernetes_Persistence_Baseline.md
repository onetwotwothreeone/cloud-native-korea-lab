# 40_GWAN_Kubernetes_Persistence_Baseline

## Goal

This step adds Kubernetes persistence to the GWAN PostgreSQL database.

## Why this matters

Before this step, PostgreSQL used emptyDir.

emptyDir is temporary storage.
It is useful for simple tests, but it is not enough for a database because data can disappear when the Pod is recreated.

This step changes PostgreSQL storage to a PersistentVolumeClaim.

## Simple explanation

emptyDir is like a temporary notebook.
PersistentVolumeClaim is like a dedicated storage box in Kubernetes.
PostgreSQL should use the storage box because it stores memory and state.

## Added files

- k8s/base/postgres-pvc.yaml
- scripts/k8s/persistence_check.sh
- docs/40_GWAN_Kubernetes_Persistence_Baseline.md
- codex/40_gwan_kubernetes_persistence_baseline_prompt.md
- tests/test_gwan_kubernetes_persistence.py

## Expected Kubernetes objects

- Namespace: hyean-gwan
- PVC: postgres-data
- Deployment: postgres
- Volume mount: /var/lib/postgresql/data

## Check commands

kubectl -n hyean-gwan get pvc
kubectl -n hyean-gwan describe pvc postgres-data
kubectl -n hyean-gwan describe deployment postgres
scripts/k8s/persistence_check.sh

## Learning point

A database should not rely on temporary Pod storage.

In cloud native systems, application containers can be replaced at any time.
Persistent data should be separated from the container lifecycle.
