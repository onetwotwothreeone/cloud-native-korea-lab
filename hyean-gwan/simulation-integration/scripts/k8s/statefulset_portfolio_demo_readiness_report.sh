#!/usr/bin/env bash
set -euo pipefail

# Portfolio demo readiness markers
# HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE
# DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
# READINESS_STATUS=SUMMARY_ONLY
# BACKUP_FRESHNESS_STATUS=PASSED
# DATA_INTEGRITY_STATUS=PASSED
# FINAL_APPROVAL_GATE_STATUS=BLOCKED
# PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
# MIGRATION_EXECUTION_ALLOWED=false
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# STATEFULSET_STATUS=NOT_CREATED
# POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC
# Do not execute real migration
# Do not export Secret values
# Do not create active PostgreSQL StatefulSet
# statefulset_final_preflight_check.sh
# 70_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Script

NAMESPACE="${NAMESPACE:-hyean-gwan}"
ROOT="${ROOT:-$HOME/cloud-native-korea-lab/hyean-gwan/simulation-integration}"
REPORT_DIR="$ROOT/.local/demo-reports"
REPORT_FILE="$REPORT_DIR/statefulset-portfolio-demo-readiness-report.env"

mkdir -p "$REPORT_DIR"

echo "Checking GWAN StatefulSet portfolio demo readiness in namespace: ${NAMESPACE}"

HYEAN_SERVICE_GOAL="PREVENTIVE_SURVIVAL_INTELLIGENCE"
DEMO_STATUS="READY_FOR_PORTFOLIO_REVIEW"
CURRENT_DECISION="NO_GO"
APPROVED_BY_OPERATOR="false"
FINAL_DECISION="NO_GO"
OPERATOR_FINAL_APPROVAL_STATUS="NOT_APPROVED"
READINESS_STATUS="SUMMARY_ONLY"
BACKUP_FRESHNESS_STATUS="PASSED"
DATA_INTEGRITY_STATUS="PASSED"
FINAL_APPROVAL_GATE_STATUS="BLOCKED"
PREFLIGHT_STATUS="PASSED_BUT_BLOCKED"
MIGRATION_EXECUTION_ALLOWED="false"
REAL_MIGRATION_EXECUTED="false"
SECRET_VALUES_EXPORTED="false"
STATEFULSET_STATUS="NOT_CREATED"
POSTGRES_CURRENT_MODE="DEPLOYMENT_WITH_PVC"

echo
echo "[1] Portfolio safety documents"

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
  "docs/68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check.md"
  "docs/69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report.md"
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
  echo "FAILED: portfolio demo evidence document is missing"
  exit 1
fi

echo
echo "[2] Kubernetes current state"
kubectl -n "$NAMESPACE" get deploy,pod,svc,pvc,secret,configmap

echo
echo "[3] PostgreSQL and GWAN API rollout status"
kubectl -n "$NAMESPACE" rollout status deployment/postgres --timeout=60s
kubectl -n "$NAMESPACE" rollout status deployment/gwan-api --timeout=60s

echo
echo "[4] StatefulSet non-execution check"
if kubectl -n "$NAMESPACE" get statefulset postgres >/dev/null 2>&1; then
  echo "FAILED: active postgres StatefulSet exists. Portfolio demo expects migration to remain blocked."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Final preflight re-check"
if [[ ! -x "$ROOT/scripts/k8s/statefulset_final_preflight_check.sh" ]]; then
  echo "FAILED: final preflight check script is missing or not executable"
  exit 1
fi

PREFLIGHT_OUTPUT="$(mktemp)"
"$ROOT/scripts/k8s/statefulset_final_preflight_check.sh" | tee "$PREFLIGHT_OUTPUT"

grep -q "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED" "$PREFLIGHT_OUTPUT"
grep -q "MIGRATION_EXECUTION_ALLOWED=false" "$PREFLIGHT_OUTPUT"
grep -q "REAL_MIGRATION_EXECUTED=false" "$PREFLIGHT_OUTPUT"
grep -q "SECRET_VALUES_EXPORTED=false" "$PREFLIGHT_OUTPUT"
grep -q "FINAL_APPROVAL_GATE_STATUS=BLOCKED" "$PREFLIGHT_OUTPUT"

echo "OK: final preflight evidence confirms blocked migration"

echo
echo "[6] Portfolio demo readiness report"
cat > "$REPORT_FILE" <<REPORT
HYEAN_SERVICE_GOAL=${HYEAN_SERVICE_GOAL}
DEMO_STATUS=${DEMO_STATUS}
CURRENT_DECISION=${CURRENT_DECISION}
APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}
FINAL_DECISION=${FINAL_DECISION}
OPERATOR_FINAL_APPROVAL_STATUS=${OPERATOR_FINAL_APPROVAL_STATUS}
READINESS_STATUS=${READINESS_STATUS}
BACKUP_FRESHNESS_STATUS=${BACKUP_FRESHNESS_STATUS}
DATA_INTEGRITY_STATUS=${DATA_INTEGRITY_STATUS}
FINAL_APPROVAL_GATE_STATUS=${FINAL_APPROVAL_GATE_STATUS}
PREFLIGHT_STATUS=${PREFLIGHT_STATUS}
MIGRATION_EXECUTION_ALLOWED=${MIGRATION_EXECUTION_ALLOWED}
REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}
SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}
STATEFULSET_STATUS=${STATEFULSET_STATUS}
POSTGRES_CURRENT_MODE=${POSTGRES_CURRENT_MODE}
REPORT

cat "$REPORT_FILE"

echo
echo "[7] Safety result"
echo "- portfolio demo readiness report created"
echo "- HYEAN/GWAN preventive service goal is documented"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active PostgreSQL StatefulSet does not exist yet"
echo "- Secret values were not exported"
echo "- final approval gate remains blocked"
echo "- final preflight passed but migration remains blocked"
echo "- demo is ready for portfolio review"
echo "- next step: 70_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Script"

echo
echo "== 69단계 완료: Portfolio Demo Readiness Report created =="
