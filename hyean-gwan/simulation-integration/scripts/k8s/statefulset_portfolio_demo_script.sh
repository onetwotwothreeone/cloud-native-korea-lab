#!/usr/bin/env bash
set -euo pipefail

# HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE
# DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO
# DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
# FINAL_APPROVAL_GATE_STATUS=BLOCKED
# PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
# PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED
# MIGRATION_EXECUTION_ALLOWED=false
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# STATEFULSET_STATUS=NOT_CREATED
# POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC
# Do not execute real migration
# Do not export Secret values
# Do not create active PostgreSQL StatefulSet
# 71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme

NAMESPACE="${NAMESPACE:-hyean-gwan}"
ROOT="${ROOT:-$HOME/cloud-native-korea-lab/hyean-gwan/simulation-integration}"
REPORT_DIR="$ROOT/.local/demo-reports"
REPORT_FILE="$REPORT_DIR/statefulset-portfolio-demo-script.md"

mkdir -p "$REPORT_DIR"

echo "Checking GWAN StatefulSet portfolio demo script in namespace: ${NAMESPACE}"

echo
echo "[1] Demo identity"
echo "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE"
echo "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO"
echo "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW"
echo "PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED"

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
  echo "FAILED: active postgres StatefulSet exists. Demo expects migration to remain blocked."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[5] Previous readiness report re-check"
if [[ ! -x "$ROOT/scripts/k8s/statefulset_portfolio_demo_readiness_report.sh" ]]; then
  echo "FAILED: portfolio demo readiness report script is missing or not executable"
  exit 1
fi

READINESS_OUTPUT="$(mktemp)"
"$ROOT/scripts/k8s/statefulset_portfolio_demo_readiness_report.sh" | tee "$READINESS_OUTPUT"

grep -q "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW" "$READINESS_OUTPUT"
grep -q "POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC" "$READINESS_OUTPUT"
grep -q "STATEFULSET_STATUS=NOT_CREATED" "$READINESS_OUTPUT"
grep -q "FINAL_APPROVAL_GATE_STATUS=BLOCKED" "$READINESS_OUTPUT"
grep -q "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED" "$READINESS_OUTPUT"
grep -q "MIGRATION_EXECUTION_ALLOWED=false" "$READINESS_OUTPUT"
grep -q "REAL_MIGRATION_EXECUTED=false" "$READINESS_OUTPUT"
grep -q "SECRET_VALUES_EXPORTED=false" "$READINESS_OUTPUT"

echo "OK: previous readiness report confirms safe blocked state"

echo
echo "[6] Create portfolio demo script report"

cat > "$REPORT_FILE" <<'REPORT'
# HYEAN/GWAN PostgreSQL StatefulSet Safety Demo Script

## Opening

This demo shows how HYEAN/GWAN prepares a high-risk PostgreSQL infrastructure change safely.

HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE

HYEAN is not only a service that reacts after failure. It is designed to observe risk early and help operators make safer decisions before damage happens.

## Current Situation

PostgreSQL is currently running as Deployment + PVC.

POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC

This is acceptable for the current demo stage, but PostgreSQL is a stateful database. In a more production-like Kubernetes design, PostgreSQL should eventually move toward StatefulSet operation.

## Safety Principle

GWAN does not move the database immediately.

It first checks safety.

The current decision is:

CURRENT_DECISION=NO_GO  
FINAL_DECISION=NO_GO  
APPROVED_BY_OPERATOR=false  
OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED  

## What Was Checked

- Kubernetes Deployment state
- PostgreSQL Pod health
- PVC binding
- Service existence
- ConfigMap existence
- Secret metadata only
- Backup freshness
- Read-only database integrity
- Operator approval record
- Final approval gate
- Final preflight check

## Current Safety Result

DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW  
FINAL_APPROVAL_GATE_STATUS=BLOCKED  
PREFLIGHT_STATUS=PASSED_BUT_BLOCKED  
STATEFULSET_STATUS=NOT_CREATED  
MIGRATION_EXECUTION_ALLOWED=false  
REAL_MIGRATION_EXECUTED=false  
SECRET_VALUES_EXPORTED=false  
PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED  

## Demo Message

The important point is not that migration was executed.

The important point is that the system knows when not to execute.

This is what makes the HYEAN/GWAN workflow meaningful as a preventive intelligence system.

## Closing

This demo is ready for portfolio review.

It proves that the project can explain cloud-native safety, database migration risk, Kubernetes operations, and operator approval flow in a beginner-friendly way.

Next step: 71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme
REPORT

cat "$REPORT_FILE"

echo
echo "[7] Safety result"
echo "- portfolio demo script report created"
echo "- HYEAN preventive service goal is included"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active PostgreSQL StatefulSet does not exist yet"
echo "- final approval gate remains blocked"
echo "- migration execution is still not allowed"
echo "- Secret values were not exported"
echo "- demo explanation is ready"
echo "- next step: 71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme"

echo
echo "== 70단계 완료: Portfolio Demo Script created =="
