#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-hyean-gwan}"

echo "Checking GWAN StatefulSet pre-migration final gate in namespace: ${NS}"

echo
echo "[1] Current PostgreSQL Deployment"
kubectl -n "$NS" get deployment postgres

echo
echo "[2] Current PostgreSQL Pod"
kubectl -n "$NS" get pods -l app.kubernetes.io/name=gwan-postgres

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "$NS" get pvc postgres-data

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "$NS" get service postgres

echo
echo "[5] Current PostgreSQL Secret"
kubectl -n "$NS" get secret gwan-postgres-secret

echo
echo "[6] Current GWAN API ConfigMap"
kubectl -n "$NS" get configmap gwan-api-config

echo
echo "[7] Active PostgreSQL StatefulSet check"
if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: Active PostgreSQL StatefulSet already exists."
  echo "FINAL_DECISION=NO_GO"
  exit 1
else
  echo "OK: No active PostgreSQL StatefulSet exists yet."
fi

echo
echo "[8] Required document assets"
required_docs=(
  "docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md"
  "docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md"
  "docs/49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate.md"
  "docs/51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md"
  "docs/52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md"
  "docs/53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate.md"
  "docs/54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check.md"
)

for file in "${required_docs[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required document: $file"
    echo "FINAL_DECISION=NO_GO"
    exit 1
  fi
done

echo "Required documents exist."

echo
echo "[9] Approval status"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"

echo
echo "[10] Result"
echo "- PostgreSQL Deployment exists"
echo "- PostgreSQL Pod exists"
echo "- postgres-data PVC exists"
echo "- PostgreSQL Service exists"
echo "- PostgreSQL Secret exists"
echo "- GWAN API ConfigMap exists"
echo "- required safety documents exist"
echo "- active PostgreSQL StatefulSet does not exist yet"
echo "- real migration remains blocked"
echo "- next step: 55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review"
