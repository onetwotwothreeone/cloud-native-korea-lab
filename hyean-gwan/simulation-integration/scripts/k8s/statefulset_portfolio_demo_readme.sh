#!/usr/bin/env bash
set -euo pipefail

# HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE
# DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO
# DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW
# POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC
# STATEFULSET_STATUS=NOT_CREATED
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
# FINAL_APPROVAL_GATE_STATUS=BLOCKED
# PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
# PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED
# PORTFOLIO_DEMO_README_STATUS=CREATED
# MIGRATION_EXECUTION_ALLOWED=false
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# Do not execute real migration
# Do not export Secret values
# Do not create active PostgreSQL StatefulSet
# 72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook

NAMESPACE="${NAMESPACE:-hyean-gwan}"
ROOT="${ROOT:-$HOME/cloud-native-korea-lab/hyean-gwan/simulation-integration}"
REPORT_DIR="$ROOT/.local/demo-reports"
REPORT_FILE="$REPORT_DIR/statefulset-portfolio-demo-readme.md"

mkdir -p "$REPORT_DIR"

echo "Checking GWAN StatefulSet portfolio demo README in namespace: ${NAMESPACE}"

echo
echo "[1] Required portfolio documents"

required_docs=(
  "docs/63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check.md"
  "docs/64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check.md"
  "docs/65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary.md"
  "docs/66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record.md"
  "docs/67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate.md"
  "docs/68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check.md"
  "docs/69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report.md"
  "docs/70_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Script.md"
  "docs/71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme.md"
)

for doc in "${required_docs[@]}"; do
  if [[ -f "$ROOT/$doc" ]]; then
    echo "OK: $doc"
  else
    echo "FAILED: missing $doc"
    exit 1
  fi
done

echo
echo "[2] Kubernetes current state"
kubectl -n "$NAMESPACE" get deploy,pod,svc,pvc,secret,configmap

echo
echo "[3] Rollout status"
kubectl -n "$NAMESPACE" rollout status deployment/postgres --timeout=60s
kubectl -n "$NAMESPACE" rollout status deployment/gwan-api --timeout=60s

echo
echo "[4] StatefulSet non-execution check"
if kubectl -n "$NAMESPACE" get statefulset postgres >/dev/null 2>&1; then
  echo "FAILED: active postgres StatefulSet exists. README demo expects migration to remain blocked."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Previous portfolio demo script check"

PREVIOUS_SCRIPT_REPORT="$REPORT_DIR/statefulset-portfolio-demo-script.md"

if [[ ! -f "$PREVIOUS_SCRIPT_REPORT" ]]; then
  if [[ -x "$ROOT/scripts/k8s/statefulset_portfolio_demo_script.sh" ]]; then
    "$ROOT/scripts/k8s/statefulset_portfolio_demo_script.sh" >/dev/null
  else
    echo "FAILED: previous portfolio demo script is missing"
    exit 1
  fi
fi

grep -q "PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED" "$PREVIOUS_SCRIPT_REPORT"
grep -q "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW" "$PREVIOUS_SCRIPT_REPORT"
grep -q "MIGRATION_EXECUTION_ALLOWED=false" "$PREVIOUS_SCRIPT_REPORT"
grep -q "REAL_MIGRATION_EXECUTED=false" "$PREVIOUS_SCRIPT_REPORT"

echo "OK: previous portfolio demo script report is valid"

echo
echo "[6] Create README demo report"

cat > "$REPORT_FILE" <<'REPORT'
# HYEAN/GWAN StatefulSet Portfolio Demo README Report

HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE
DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO
DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW
POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC
STATEFULSET_STATUS=NOT_CREATED
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
FINAL_APPROVAL_GATE_STATUS=BLOCKED
PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED
PORTFOLIO_DEMO_README_STATUS=CREATED
MIGRATION_EXECUTION_ALLOWED=false
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false

## Summary

The portfolio README is ready.

The demo explains why HYEAN/GWAN keeps PostgreSQL migration blocked until safety, approval, and final execution gates are satisfied.

## Next Step

72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook
REPORT

cat "$REPORT_FILE"

echo
echo "[7] Safety result"
echo "- portfolio demo README report created"
echo "- HYEAN preventive service goal is documented"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active PostgreSQL StatefulSet does not exist yet"
echo "- final approval gate remains blocked"
echo "- real migration remains disabled"
echo "- Secret values were not exported"
echo "- README is ready for portfolio review"
echo "- next step: 72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook"

echo
echo "== 71단계 완료: Portfolio Demo README created =="
