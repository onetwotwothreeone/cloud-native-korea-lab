#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-hyean-gwan}"

echo "== Kubernetes objects =="
kubectl -n "${NAMESPACE}" get all || true

echo "== Recent events =="
kubectl -n "${NAMESPACE}" get events --sort-by=.lastTimestamp || true

echo "== Deployment descriptions =="
kubectl -n "${NAMESPACE}" describe deployment/gwan-api || true
kubectl -n "${NAMESPACE}" describe deployment/postgres || true

echo "== Pod descriptions =="
kubectl -n "${NAMESPACE}" describe pods || true

echo "== GWAN API logs =="
kubectl -n "${NAMESPACE}" logs deployment/gwan-api --tail=120 || true

echo "== PostgreSQL logs =="
kubectl -n "${NAMESPACE}" logs deployment/postgres --tail=120 || true
