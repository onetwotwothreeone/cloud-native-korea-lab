#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN StatefulSet manual approval record in namespace: ${NAMESPACE}"

echo
echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NAMESPACE}" get deployment postgres

echo
echo "[2] Current PostgreSQL Pod"
kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "${NAMESPACE}" get service postgres

echo
echo "[5] Current PostgreSQL Secret"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret

echo
echo "[6] Current GWAN API ConfigMap"
kubectl -n "${NAMESPACE}" get configmap gwan-api-config

echo
echo "[7] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "ERROR: postgres StatefulSet already exists. Real migration may have been executed."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[8] Required approval documents"
test -f docs/51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md
test -f docs/52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md

echo
echo "[9] Approval record status"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"

echo
echo "[10] Result"
echo "- manual approval record exists"
echo "- operator has not approved migration yet"
echo "- real migration is still blocked"
echo "- next step: 53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template"
