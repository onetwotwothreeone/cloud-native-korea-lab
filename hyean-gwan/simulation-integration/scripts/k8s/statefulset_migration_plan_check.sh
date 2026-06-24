#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN PostgreSQL StatefulSet migration readiness in namespace: ${NAMESPACE}"

echo
echo "[1] Current PostgreSQL workload"
kubectl -n "${NAMESPACE}" get deployment postgres

echo
echo "[2] Current PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data

echo
echo "[3] Current PostgreSQL Service"
kubectl -n "${NAMESPACE}" get service postgres

echo
echo "[4] Current Secret and ConfigMap"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret
kubectl -n "${NAMESPACE}" get configmap gwan-api-config

echo
echo "[5] Current NetworkPolicy"
kubectl -n "${NAMESPACE}" get networkpolicy || true

echo
echo "[6] StatefulSet status"
kubectl -n "${NAMESPACE}" get statefulset || true

echo
echo "[7] Migration decision"
echo "- PostgreSQL is still Deployment + PVC"
echo "- StatefulSet migration is not applied yet"
echo "- Backup and restore baseline should come before StatefulSet migration"
echo "- Next recommended step: 43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline"
