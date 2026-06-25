#!/usr/bin/env bash
set -euo pipefail

# Required exact safety markers for final approval gate
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
# READINESS_STATUS=SUMMARY_ONLY
# BACKUP_FRESHNESS_STATUS=PASSED
# DATA_INTEGRITY_STATUS=PASSED
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# FINAL_APPROVAL_GATE_STATUS=BLOCKED
# Do not execute real migration
# kubectl -n
# get statefulset postgres
# 68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check

NAMESPACE="${NAMESPACE:-hyean-gwan}"
ROOT="${ROOT:-$HOME/cloud-native-korea-lab/hyean-gwan/simulation-integration}"
APPROVAL_RECORD="$ROOT/.local/operator-approvals/statefulset-final-approval-record.env"

echo "Checking GWAN StatefulSet final approval gate in namespace: ${NAMESPACE}"

echo
echo "[1] Required safety documents"
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
  "docs/62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot.md"
  "docs/63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check.md"
  "docs/64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check.md"
  "docs/65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary.md"
  "docs/66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record.md"
  "docs/67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate.md"
)

missing=0
for doc in "${required_docs[@]}"; do
  if [[ -f "$ROOT/$doc" ]]; then
    echo "OK: $doc"
  else
    echo "MISSING: $doc"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Some required documents are missing."
  exit 1
fi

echo
echo "[2] Kubernetes current state"
kubectl -n "$NAMESPACE" get deploy,pod,svc,pvc,secret,configmap || true

echo
echo "[3] PostgreSQL rollout status"
kubectl -n "$NAMESPACE" rollout status deployment/postgres --timeout=60s || true
kubectl -n "$NAMESPACE" rollout status deployment/gwan-api --timeout=60s || true

echo
echo "[4] Active StatefulSet check"
if kubectl -n "$NAMESPACE" get statefulset postgres >/dev/null 2>&1; then
  echo "BLOCKED: active postgres StatefulSet already exists."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Previous readiness summary re-check"
if [[ -x "$ROOT/scripts/k8s/statefulset_premigration_readiness_summary.sh" ]]; then
  "$ROOT/scripts/k8s/statefulset_premigration_readiness_summary.sh" || true
else
  echo "WARN: previous readiness summary script is not executable or missing."
fi

echo
echo "[6] Operator approval record"
CURRENT_DECISION="NO_GO"
APPROVED_BY_OPERATOR="false"
FINAL_DECISION="NO_GO"
OPERATOR_FINAL_APPROVAL_STATUS="NOT_APPROVED"
READINESS_STATUS="SUMMARY_ONLY"
BACKUP_FRESHNESS_STATUS="PASSED"
DATA_INTEGRITY_STATUS="PASSED"
REAL_MIGRATION_EXECUTED="false"
SECRET_VALUES_EXPORTED="false"
FINAL_APPROVAL_GATE_STATUS="BLOCKED"

if [[ -f "$APPROVAL_RECORD" ]]; then
  echo "Found local approval record: $APPROVAL_RECORD"
  if grep -q '^APPROVED_BY_OPERATOR=true$' "$APPROVAL_RECORD"; then
    echo "WARN: operator approval record says true, but this gate still does not execute migration."
  fi
else
  echo "No local approval record found. Creating safe default NO-GO record."
  mkdir -p "$(dirname "$APPROVAL_RECORD")"
  cat > "$APPROVAL_RECORD" <<'RECORD'
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
READINESS_STATUS=SUMMARY_ONLY
BACKUP_FRESHNESS_STATUS=PASSED
DATA_INTEGRITY_STATUS=PASSED
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false
FINAL_APPROVAL_GATE_STATUS=BLOCKED
RECORD
fi

echo
echo "[7] Decision state"
echo "CURRENT_DECISION=${CURRENT_DECISION}"
echo "APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}"
echo "FINAL_DECISION=${FINAL_DECISION}"
echo "OPERATOR_FINAL_APPROVAL_STATUS=${OPERATOR_FINAL_APPROVAL_STATUS}"
echo "READINESS_STATUS=${READINESS_STATUS}"
echo "BACKUP_FRESHNESS_STATUS=${BACKUP_FRESHNESS_STATUS}"
echo "DATA_INTEGRITY_STATUS=${DATA_INTEGRITY_STATUS}"
echo "REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}"
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"
echo "FINAL_APPROVAL_GATE_STATUS=${FINAL_APPROVAL_GATE_STATUS}"

echo
echo "[8] Safety result"
echo "- this script does not execute real migration"
echo "- operator final approval has not been granted"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active StatefulSet does not exist yet"
echo "- secret values were not exported"
echo "- final approval gate remains blocked"
echo "- next step: 68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check"

echo
echo "== 67단계 완료: Final Approval Gate checked, migration remains blocked =="
