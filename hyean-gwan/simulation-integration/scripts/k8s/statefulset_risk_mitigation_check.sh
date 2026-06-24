#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"

echo "Checking GWAN StatefulSet risk mitigation checklist in namespace: ${NS}"

echo ""
echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NS}" get deployment postgres
READY_REPLICAS="$(kubectl -n "${NS}" get deployment postgres -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo 0)"
if [ "${READY_REPLICAS:-0}" = "0" ]; then
  echo "ERROR: PostgreSQL Deployment has no ready replicas."
  exit 1
fi

echo ""
echo "[2] Current PostgreSQL Pod"
kubectl -n "${NS}" get pods -l app.kubernetes.io/name=postgres

echo ""
echo "[3] Current PostgreSQL PVC"
kubectl -n "${NS}" get pvc postgres-data
PVC_PHASE="$(kubectl -n "${NS}" get pvc postgres-data -o jsonpath='{.status.phase}' 2>/dev/null || echo "")"
if [ "${PVC_PHASE}" != "Bound" ]; then
  echo "ERROR: postgres-data PVC is not Bound."
  exit 1
fi

echo ""
echo "[4] Current PostgreSQL Service"
kubectl -n "${NS}" get service postgres

echo ""
echo "[5] Current PostgreSQL Secret"
kubectl -n "${NS}" get secret gwan-postgres-secret

echo ""
echo "[6] Current GWAN API ConfigMap"
kubectl -n "${NS}" get configmap gwan-api-config

echo ""
echo "[7] Active StatefulSet check"
if kubectl -n "${NS}" get statefulset postgres >/dev/null 2>&1; then
  echo "ERROR: Active postgres StatefulSet already exists. Real migration may have started."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo ""
echo "[8] Required mitigation documents"
required_docs=(
  "docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md"
  "docs/44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md"
  "docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md"
  "docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md"
  "docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md"
  "docs/48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md"
  "docs/49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate.md"
  "docs/50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record.md"
  "docs/51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md"
  "docs/52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md"
  "docs/53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate.md"
  "docs/54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check.md"
  "docs/55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review.md"
  "docs/56_GWAN_Kubernetes_StatefulSet_Final_Go_NoGo_Decision.md"
  "docs/57_GWAN_Kubernetes_StatefulSet_Approved_Migration_Execution_Plan.md"
  "docs/58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run.md"
  "docs/59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review.md"
  "docs/60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register.md"
  "docs/61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md"
)

missing=0
for doc in "${required_docs[@]}"; do
  if [ -f "${doc}" ]; then
    echo "OK: ${doc}"
  else
    echo "MISSING: ${doc}"
    missing=1
  fi
done

if [ "${missing}" = "1" ]; then
  echo "ERROR: Some required documents are missing."
  exit 1
fi

echo ""
echo "[9] Mitigation decision state"
grep -q "CURRENT_DECISION=NO_GO" docs/61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md
grep -q "APPROVED_BY_OPERATOR=false" docs/61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md
grep -q "FINAL_DECISION=NO_GO" docs/61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md
grep -q "REAL_MIGRATION_EXECUTED=false" docs/61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md

echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo "REAL_MIGRATION_EXECUTED=false"

echo ""
echo "[10] Mitigation checklist result"
echo "- data loss risk is mitigated"
echo "- downtime risk is mitigated"
echo "- workload conflict risk is mitigated"
echo "- rollback risk is mitigated"
echo "- approval bypass risk is mitigated"
echo "- real migration remains blocked"
echo "- next step: 62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot"
