#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-hyean-gwan}"
TIMEOUT="${2:-180s}"

echo "Checking Kubernetes rollout status in namespace: ${NAMESPACE}"
kubectl -n "${NAMESPACE}" rollout status deployment/postgres --timeout="${TIMEOUT}"
kubectl -n "${NAMESPACE}" rollout status deployment/gwan-api --timeout="${TIMEOUT}"
kubectl -n "${NAMESPACE}" get deployments
kubectl -n "${NAMESPACE}" get pods
kubectl -n "${NAMESPACE}" get services
