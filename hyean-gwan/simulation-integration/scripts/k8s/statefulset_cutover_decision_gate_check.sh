#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAMESPACE="hyean-gwan"

echo "Checking GWAN StatefulSet cutover decision gate in namespace: ${NAMESPACE}"
echo

echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NAMESPACE}" get deployment postgres || true
echo

echo "[2] Current PostgreSQL Pod"
kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres -o wide || true
echo

echo "[3] Current PostgreSQL PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data || true
echo

echo "[4] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: active postgres StatefulSet exists."
else
  echo "OK: No active postgres StatefulSet exists yet."
fi
echo

echo "[5] Decision"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo

echo "[6] Safety result"
echo "- this script does not execute real migration"
echo "- this script only checks cutover decision readiness"
echo "- migration remains blocked"
echo "- next step: 50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record"
