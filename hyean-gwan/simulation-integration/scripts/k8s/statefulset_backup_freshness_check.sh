#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"
BACKUP_DIR="${BACKUP_DIR:-.local/postgres-backups}"
BACKUP_MAX_AGE_SECONDS="${BACKUP_MAX_AGE_SECONDS:-86400}"

CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
BACKUP_FRESHNESS_STATUS=REVIEW_ONLY
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false

echo "Checking GWAN PostgreSQL backup freshness in namespace: ${NAMESPACE}"

echo
echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NAMESPACE}" get deployment postgres

echo
echo "[2] Current PostgreSQL Pod"
kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres

RUNNING_POD_COUNT="$(kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l | tr -d ' ')"
if [ "${RUNNING_POD_COUNT}" -lt 1 ]; then
  echo "ERROR: no running PostgreSQL pod found"
  exit 1
fi

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data

PVC_PHASE="$(kubectl -n "${NAMESPACE}" get pvc postgres-data -o jsonpath='{.status.phase}')"
if [ "${PVC_PHASE}" != "Bound" ]; then
  echo "ERROR: postgres-data PVC is not Bound"
  exit 1
fi

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "${NAMESPACE}" get service postgres

echo
echo "[5] Current PostgreSQL Secret metadata"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"

echo
echo "[6] Current GWAN API ConfigMap"
kubectl -n "${NAMESPACE}" get configmap gwan-api-config

echo
echo "[7] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "ERROR: active postgres StatefulSet already exists"
  exit 1
else
  echo "OK: no active postgres StatefulSet exists yet."
fi

echo
echo "[8] Required backup documents"
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
)

for doc in "${required_docs[@]}"; do
  if [ ! -f "${doc}" ]; then
    echo "MISSING: ${doc}"
    exit 1
  fi
  echo "OK: ${doc}"
done

echo
echo "[9] Backup freshness check"

if [ ! -d "${BACKUP_DIR}" ]; then
  echo "ERROR: backup directory does not exist: ${BACKUP_DIR}"
  echo "Run first: scripts/k8s/postgres_backup_restore_check.sh"
  exit 1
fi

LATEST_BACKUP_FILE="$(find "${BACKUP_DIR}" -type f -name '*.sql' -print 2>/dev/null | sort | tail -n 1 || true)"

if [ -z "${LATEST_BACKUP_FILE}" ]; then
  echo "ERROR: latest backup file does not exist"
  echo "Run first: scripts/k8s/postgres_backup_restore_check.sh"
  exit 1
fi

echo "LATEST_BACKUP_FILE=${LATEST_BACKUP_FILE}"

BACKUP_AGE_SECONDS="$(python - <<PY
from pathlib import Path
import time

path = Path("${LATEST_BACKUP_FILE}")
age = int(time.time() - path.stat().st_mtime)
print(age)
PY
)"

echo "BACKUP_AGE_SECONDS=${BACKUP_AGE_SECONDS}"
echo "BACKUP_MAX_AGE_SECONDS=${BACKUP_MAX_AGE_SECONDS}"

if [ "${BACKUP_AGE_SECONDS}" -gt "${BACKUP_MAX_AGE_SECONDS}" ]; then
  echo "ERROR: latest backup is too old"
  echo "Run first: scripts/k8s/postgres_backup_restore_check.sh"
  exit 1
fi

echo
echo "[10] Decision state"
echo "CURRENT_DECISION=${CURRENT_DECISION}"
echo "APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}"
echo "FINAL_DECISION=${FINAL_DECISION}"
echo "BACKUP_FRESHNESS_STATUS=${BACKUP_FRESHNESS_STATUS}"
echo "REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}"
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"

echo
echo "[11] Safety result"
echo "- latest backup file exists"
echo "- backup age is within acceptable window"
echo "- PostgreSQL Deployment is available"
echo "- PostgreSQL Pod is running"
echo "- postgres-data PVC is Bound"
echo "- PostgreSQL Secret exists"
echo "- GWAN API ConfigMap exists"
echo "- no active postgres StatefulSet exists yet"
echo "- secret values were not exported"
echo "- real migration remains blocked"
echo "- next step: 64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check"
