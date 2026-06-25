#!/usr/bin/env bash
set -euo pipefail

# Required exact test markers for operator final approval record
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
# READINESS_STATUS=SUMMARY_ONLY
# BACKUP_FRESHNESS_STATUS=PASSED
# DATA_INTEGRITY_STATUS=PASSED
# READ_ONLY_CHECK=true
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# statefulset_premigration_readiness_summary.sh
# .local/operator-approvals/statefulset-final-approval-record.env
# 67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate

NAMESPACE="${NAMESPACE:-hyean-gwan}"

CURRENT_DECISION="NO_GO"
APPROVED_BY_OPERATOR="false"
FINAL_DECISION="NO_GO"
OPERATOR_FINAL_APPROVAL_STATUS="NOT_APPROVED"
READINESS_STATUS="SUMMARY_ONLY"
BACKUP_FRESHNESS_STATUS="PASSED"
DATA_INTEGRITY_STATUS="PASSED"
READ_ONLY_CHECK="true"
REAL_MIGRATION_EXECUTED="false"
SECRET_VALUES_EXPORTED="false"

RECORD_DIR=".local/operator-approvals"
RECORD_FILE="${RECORD_DIR}/statefulset-final-approval-record.env"

echo "== 66단계: GWAN Kubernetes StatefulSet Operator Final Approval Record 시작 =="
echo "Checking operator final approval record in namespace: ${NAMESPACE}"

echo
echo "[1] Required previous documents"

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
)

for doc in "${required_docs[@]}"; do
  if [[ -f "${doc}" ]]; then
    echo "OK: ${doc}"
  else
    echo "MISSING: ${doc}"
    exit 1
  fi
done

echo
echo "[2] Kubernetes current state"
kubectl -n "${NAMESPACE}" get deploy,pod,svc,pvc,secret,configmap

echo
echo "[3] PostgreSQL rollout status"
kubectl -n "${NAMESPACE}" rollout status deployment/postgres --timeout=180s
kubectl -n "${NAMESPACE}" rollout status deployment/gwan-api --timeout=180s

echo
echo "[4] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "BLOCKED: postgres StatefulSet already exists."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Previous readiness summary re-check"
scripts/k8s/statefulset_premigration_readiness_summary.sh

echo
echo "[6] Create local non-secret operator approval record"
mkdir -p "${RECORD_DIR}"

cat > "${RECORD_FILE}" <<RECORD
CURRENT_DECISION=${CURRENT_DECISION}
APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}
FINAL_DECISION=${FINAL_DECISION}
OPERATOR_FINAL_APPROVAL_STATUS=${OPERATOR_FINAL_APPROVAL_STATUS}
READINESS_STATUS=${READINESS_STATUS}
BACKUP_FRESHNESS_STATUS=${BACKUP_FRESHNESS_STATUS}
DATA_INTEGRITY_STATUS=${DATA_INTEGRITY_STATUS}
READ_ONLY_CHECK=${READ_ONLY_CHECK}
REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}
SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}
NEXT_STEP=67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate
RECORD

echo "OK: local approval record created at ${RECORD_FILE}"

echo
echo "[7] Decision state"
echo "CURRENT_DECISION=${CURRENT_DECISION}"
echo "APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}"
echo "FINAL_DECISION=${FINAL_DECISION}"
echo "OPERATOR_FINAL_APPROVAL_STATUS=${OPERATOR_FINAL_APPROVAL_STATUS}"
echo "READINESS_STATUS=${READINESS_STATUS}"
echo "BACKUP_FRESHNESS_STATUS=${BACKUP_FRESHNESS_STATUS}"
echo "DATA_INTEGRITY_STATUS=${DATA_INTEGRITY_STATUS}"
echo "READ_ONLY_CHECK=${READ_ONLY_CHECK}"
echo "REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}"
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"

echo
echo "[8] Safety result"
echo "- this script does not execute real migration"
echo "- operator final approval has not been granted"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active StatefulSet does not exist yet"
echo "- real migration remains blocked"
echo "- secret values were not exported"
echo "- next step: 67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate"

echo
echo "== 66단계 완료: Operator Final Approval Record 생성 및 NO-GO 유지 =="
