#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN StatefulSet cutover approval record in namespace: ${NAMESPACE}"

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
echo "[7] Required document assets"
test -f docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md
test -f docs/44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md
test -f docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md
test -f docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
test -f docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md
test -f docs/48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md
test -f docs/50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record.md

echo
echo "[8] Approval decision"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"

echo
echo "[9] Result"
echo "- approval record exists"
echo "- real migration is still blocked"
echo "- operator approval is required before cutover"
echo "- next step: 51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template"
