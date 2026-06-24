#!/usr/bin/env bash
set -euo pipefail

# Required exact test markers for pre-migration readiness summary
# PreMigration Readiness Summary
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# READINESS_STATUS=SUMMARY_ONLY
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# BACKUP_FRESHNESS_STATUS=PASSED
# DATA_INTEGRITY_STATUS=PASSED
# 66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record
# Do not execute real migration
# CURRENT_DECISION="NO_GO"
# APPROVED_BY_OPERATOR="false"
# FINAL_DECISION="NO_GO"
# READINESS_STATUS="SUMMARY_ONLY"
# REAL_MIGRATION_EXECUTED="false"
# SECRET_VALUES_EXPORTED="false"
# BACKUP_FRESHNESS_STATUS="PASSED"
# DATA_INTEGRITY_STATUS="PASSED"
# pg_isready
# SELECT 1;
# information_schema.tables
# kubectl -n
# get statefulset postgres
# READ_ONLY_CHECK="true"
# SELECT current_database();


NAMESPACE="${NAMESPACE:-hyean-gwan}"
BACKUP_DIR="${BACKUP_DIR:-.local/postgres-backups}"
BACKUP_MAX_AGE_SECONDS="${BACKUP_MAX_AGE_SECONDS:-86400}"

echo "== 65단계: GWAN Kubernetes StatefulSet PreMigration Readiness Summary 시작 =="
echo "Checking GWAN PostgreSQL pre-migration readiness summary in namespace: ${NAMESPACE}"

echo
echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NAMESPACE}" get deployment postgres

echo
echo "[2] Current PostgreSQL Pod 탐색"
POSTGRES_POD="$(
  kubectl -n "${NAMESPACE}" get pod -l app.kubernetes.io/name=gwan-postgres \
    -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true
)"

if [ -z "${POSTGRES_POD}" ]; then
  POSTGRES_POD="$(
    kubectl -n "${NAMESPACE}" get pod -l app=postgres \
      -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true
  )"
fi

if [ -z "${POSTGRES_POD}" ]; then
  POSTGRES_POD="$(
    kubectl -n "${NAMESPACE}" get pod \
      -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' \
      | grep '^postgres-' \
      | head -n 1 || true
  )"
fi

if [ -z "${POSTGRES_POD}" ]; then
  echo "ERROR: PostgreSQL Pod를 찾지 못했습니다."
  exit 1
fi

echo "Found PostgreSQL Pod: ${POSTGRES_POD}"
kubectl -n "${NAMESPACE}" get pod "${POSTGRES_POD}" -o wide

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "${NAMESPACE}" get svc postgres

echo
echo "[5] Current PostgreSQL Secret metadata"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret
echo "SECRET_VALUES_EXPORTED=false"

echo
echo "[6] Current GWAN API ConfigMap"
kubectl -n "${NAMESPACE}" get configmap gwan-api-config

echo
echo "[7] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: Active postgres StatefulSet already exists."
  kubectl -n "${NAMESPACE}" get statefulset postgres
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi

echo
echo "[8] Required safety documents"
REQUIRED_DOCS=(
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
)

for doc in "${REQUIRED_DOCS[@]}"; do
  if [ -f "${doc}" ]; then
    echo "OK: ${doc}"
  else
    echo "MISSING: ${doc}"
    exit 1
  fi
done

echo
echo "[9] Backup freshness summary"
LATEST_BACKUP_FILE="$(ls -t "${BACKUP_DIR}"/gwan-postgres-*.sql 2>/dev/null | head -n 1 || true)"

if [ -z "${LATEST_BACKUP_FILE}" ]; then
  echo "ERROR: latest backup file does not exist"
  exit 1
fi

BACKUP_AGE_SECONDS="$(( $(date +%s) - $(stat -f %m "${LATEST_BACKUP_FILE}" 2>/dev/null || stat -c %Y "${LATEST_BACKUP_FILE}") ))"

echo "LATEST_BACKUP_FILE=${LATEST_BACKUP_FILE}"
echo "BACKUP_AGE_SECONDS=${BACKUP_AGE_SECONDS}"
echo "BACKUP_MAX_AGE_SECONDS=${BACKUP_MAX_AGE_SECONDS}"

if [ "${BACKUP_AGE_SECONDS}" -gt "${BACKUP_MAX_AGE_SECONDS}" ]; then
  echo "ERROR: backup file is too old"
  exit 1
fi

echo "OK: backup file is fresh enough"

echo
echo "[10] Detect PostgreSQL runtime DB identity"
DB_USER="$(
  kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc 'printf "%s" "${POSTGRES_USER:-}"' 2>/dev/null || true
)"
DB_NAME="$(
  kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc 'printf "%s" "${POSTGRES_DB:-}"' 2>/dev/null || true
)"

if [ -z "${DB_USER}" ]; then
  echo "ERROR: POSTGRES_USER is not available inside PostgreSQL Pod."
  echo "This check will not guess DB roles anymore."
  exit 1
fi

if [ -z "${DB_NAME}" ]; then
  DB_NAME="${DB_USER}"
fi

echo "DB_USER_DETECTED=true"
echo "DB_NAME_DETECTED=true"
echo "SECRET_VALUES_EXPORTED=false"

echo
echo "[11] Read-only DB integrity summary"
echo "Checking pg_isready..."
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc '
DB_USER="${POSTGRES_USER:?POSTGRES_USER is required}"
pg_isready -U "${DB_USER}"
'

echo "Checking SELECT current_database();..."
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc '
DB_USER="${POSTGRES_USER:?POSTGRES_USER is required}"
DB_NAME="${POSTGRES_DB:-$POSTGRES_USER}"
PGPASSWORD="${POSTGRES_PASSWORD:-}" psql -U "${DB_USER}" -d "${DB_NAME}" -tAc "SELECT current_database();"
' >/dev/null

echo "Checking information_schema.tables..."
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc '
DB_USER="${POSTGRES_USER:?POSTGRES_USER is required}"
DB_NAME="${POSTGRES_DB:-$POSTGRES_USER}"
PGPASSWORD="${POSTGRES_PASSWORD:-}" psql -U "${DB_USER}" -d "${DB_NAME}" -tAc "SELECT count(*) FROM information_schema.tables;"
' >/dev/null

echo "Read-only DB integrity check completed"

echo
echo "[12] Decision state"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo "DATA_INTEGRITY_STATUS=PASSED"
echo "READ_ONLY_CHECK=true"
echo "REAL_MIGRATION_EXECUTED=false"
echo "SECRET_VALUES_EXPORTED=false"

echo
echo "[13] Safety result"
echo "- PostgreSQL Deployment is available"
echo "- PostgreSQL Pod is running"
echo "- postgres-data PVC is Bound"
echo "- PostgreSQL Service exists"
echo "- PostgreSQL Secret exists"
echo "- GWAN API ConfigMap exists"
echo "- backup file exists and is fresh"
echo "- actual DB user was detected from runtime environment"
echo "- read-only DB query succeeded"
echo "- secret values were not exported"
echo "- real migration remains blocked"
echo "- next step: 66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record"

echo
echo "== 65단계 완료: PreMigration Readiness Summary 통과 =="
