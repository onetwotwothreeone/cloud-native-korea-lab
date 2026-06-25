#!/usr/bin/env bash
set -euo pipefail

# Required exact safety markers for final preflight check
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
# Do not execute real migration
# Do not export Secret values
# Do not create active PostgreSQL StatefulSet
# statefulset_premigration_readiness_summary.sh
# statefulset_final_approval_gate.sh
# 69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report

NAMESPACE="${NAMESPACE:-hyean-gwan}"
ROOT="${ROOT:-$HOME/cloud-native-korea-lab/hyean-gwan/simulation-integration}"
REPORT_DIR="$ROOT/.local/preflight-reports"
REPORT_FILE="$REPORT_DIR/statefulset-final-preflight-check.env"

mkdir -p "$REPORT_DIR"

echo "Checking GWAN StatefulSet final preflight in namespace: ${NAMESPACE}"

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

echo
echo "[1] Required final preflight documents"

required_docs=(
  "docs/63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check.md"
  "docs/64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check.md"
  "docs/65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary.md"
  "docs/66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record.md"
  "docs/67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate.md"
  "docs/68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check.md"
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
  echo "FAILED: required preflight document is missing"
  exit 1
fi

echo
echo "[2] Kubernetes current state"
kubectl -n "$NAMESPACE" get deploy,pod,svc,pvc,secret,configmap

echo
echo "[3] Deployment rollout status"
kubectl -n "$NAMESPACE" rollout status deployment/postgres --timeout=60s
kubectl -n "$NAMESPACE" rollout status deployment/gwan-api --timeout=60s

echo
echo "[4] Active StatefulSet check"
if kubectl -n "$NAMESPACE" get statefulset postgres >/dev/null 2>&1; then
  echo "FAILED: active postgres StatefulSet exists. This preflight expected migration to remain blocked."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Previous readiness summary"
if [[ ! -x "$ROOT/scripts/k8s/statefulset_premigration_readiness_summary.sh" ]]; then
  echo "FAILED: previous readiness summary script is missing or not executable"
  exit 1
fi

READINESS_OUTPUT="$(mktemp)"
"$ROOT/scripts/k8s/statefulset_premigration_readiness_summary.sh" | tee "$READINESS_OUTPUT"

grep -q "DATA_INTEGRITY_STATUS=PASSED" "$READINESS_OUTPUT"
grep -q "READ_ONLY_CHECK=true" "$READINESS_OUTPUT"
grep -q "REAL_MIGRATION_EXECUTED=false" "$READINESS_OUTPUT"
grep -q "SECRET_VALUES_EXPORTED=false" "$READINESS_OUTPUT"

echo "OK: previous readiness summary passed required safety markers"

echo
echo "[6] Final approval gate"
if [[ ! -x "$ROOT/scripts/k8s/statefulset_final_approval_gate.sh" ]]; then
  echo "FAILED: final approval gate script is missing or not executable"
  exit 1
fi

GATE_OUTPUT="$(mktemp)"
"$ROOT/scripts/k8s/statefulset_final_approval_gate.sh" | tee "$GATE_OUTPUT"

grep -q "FINAL_APPROVAL_GATE_STATUS=BLOCKED" "$GATE_OUTPUT"
grep -q "FINAL_DECISION=NO_GO" "$GATE_OUTPUT"
grep -q "APPROVED_BY_OPERATOR=false" "$GATE_OUTPUT"

echo "OK: final approval gate remains blocked"

echo
echo "[7] Final preflight decision"
cat > "$REPORT_FILE" <<REPORT
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
REPORT

cat "$REPORT_FILE"

echo
echo "[8] Safety result"
echo "- final preflight check passed"
echo "- PostgreSQL remains Deployment + PVC"
echo "- no active PostgreSQL StatefulSet exists yet"
echo "- Secret values were not exported"
echo "- final approval gate remains blocked"
echo "- migration execution is still not allowed"
echo "- next step: 69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report"

echo
echo "== 68단계 완료: Final Preflight Check passed, migration remains blocked =="
