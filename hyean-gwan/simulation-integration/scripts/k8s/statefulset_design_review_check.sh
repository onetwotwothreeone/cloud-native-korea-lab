#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN PostgreSQL persistence design in namespace: ${NAMESPACE}"

echo
echo "[1] Workload check"
kubectl -n "${NAMESPACE}" get deployment postgres
kubectl -n "${NAMESPACE}" get statefulset || true

echo
echo "[2] PVC check"
kubectl -n "${NAMESPACE}" get pvc postgres-data
kubectl -n "${NAMESPACE}" describe pvc postgres-data | sed -n '1,80p'

echo
echo "[3] PostgreSQL Deployment storage check"
kubectl -n "${NAMESPACE}" get deployment postgres -o yaml | grep -E "persistentVolumeClaim|claimName|postgres-data|mountPath" || true

echo
echo "[4] Expected design"
echo "- Current baseline uses Deployment + PVC"
echo "- PostgreSQL PVC name should be postgres-data"
echo "- StatefulSet migration is not applied yet"
echo "- StatefulSet migration should be handled later with backup and restore planning"
