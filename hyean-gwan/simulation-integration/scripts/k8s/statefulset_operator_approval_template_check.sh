#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN StatefulSet operator approval template in namespace: ${NAMESPACE}"

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
echo "[7] Required approval template"
test -f docs/51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md

echo
echo "[8] Required safety documents"
test -f docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md
test -f docs/44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md
test -f docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md
test -f docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
test -f docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md
test -f docs/48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md
test -f docs/50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record.md

echo
echo "[9] Approval gate"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"

echo
echo "[10] Result"
echo "- operator approval template exists"
echo "- required safety documents exist"
echo "- real migration is still blocked"
echo "- next step: 52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record"
