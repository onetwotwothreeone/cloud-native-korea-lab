#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-hyean-gwan}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

APPROVAL_DOC="$ROOT/docs/52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md"
GATE_DOC="$ROOT/docs/53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate.md"
BACKUP_DOC="$ROOT/docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md"
ROLLBACK_DOC="$ROOT/docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md"
DRAFT_FILE="$ROOT/k8s/drafts/postgres-statefulset-draft.yaml"

echo "Checking GWAN StatefulSet operator approval gate in namespace: $NS"
echo

echo "[1] Required document check"
test -f "$APPROVAL_DOC"
test -f "$GATE_DOC"
test -f "$BACKUP_DOC"
test -f "$ROLLBACK_DOC"
test -f "$DRAFT_FILE"
echo "Required documents and draft exist"
echo

CURRENT_DECISION="$(grep -E '^CURRENT_DECISION=' "$APPROVAL_DOC" | tail -1 | cut -d= -f2 || true)"
APPROVED_BY_OPERATOR="$(grep -E '^APPROVED_BY_OPERATOR=' "$APPROVAL_DOC" | tail -1 | cut -d= -f2 || true)"
FINAL_DECISION="$(grep -E '^FINAL_DECISION=' "$APPROVAL_DOC" | tail -1 | cut -d= -f2 || true)"

echo "[2] Approval record"
echo "CURRENT_DECISION=${CURRENT_DECISION:-missing}"
echo "APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR:-missing}"
echo "FINAL_DECISION=${FINAL_DECISION:-missing}"
echo

echo "[3] Current PostgreSQL workload check"
if kubectl -n "$NS" get deployment postgres >/dev/null 2>&1; then
  echo "Current PostgreSQL is still Deployment: OK"
else
  echo "PostgreSQL Deployment not found"
fi

if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: Active PostgreSQL StatefulSet already exists"
else
  echo "No active PostgreSQL StatefulSet exists yet: OK"
fi
echo

echo "[4] Operator approval gate result"
if [[ "$CURRENT_DECISION" == "GO" && "$APPROVED_BY_OPERATOR" == "true" && "$FINAL_DECISION" == "GO" ]]; then
  echo "APPROVAL_GATE=OPEN"
  echo "Real migration may be considered by the operator."
else
  echo "APPROVAL_GATE=CLOSED"
  echo "Real migration must remain blocked."
fi

echo
echo "[5] Safety result"
echo "- this script does not execute real migration"
echo "- this script only checks operator approval readiness"
echo "- next recommended step: 54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check"
