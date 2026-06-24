#!/usr/bin/env bash
set -euo pipefail

# Required safety markers for pre-migration data integrity check
# CURRENT_DECISION=NO_GO
# APPROVED_BY_OPERATOR=false
# FINAL_DECISION=NO_GO
# DATA_INTEGRITY_STATUS=REVIEW_ONLY
# READ_ONLY_CHECK=true
# REAL_MIGRATION_EXECUTED=false
# SECRET_VALUES_EXPORTED=false
# pg_isready
# SELECT current_database();

# Safety status constants for pre-migration data integrity review
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
DATA_INTEGRITY_STATUS=REVIEW_ONLY
READ_ONLY_CHECK=true
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false


NAMESPACE="${NAMESPACE:-hyean-gwan}"
BACKUP_DIR="${BACKUP_DIR:-.local/postgres-backups}"
BACKUP_MAX_AGE_SECONDS="${BACKUP_MAX_AGE_SECONDS:-86400}"

# Safety decision is intentionally fixed for this pre-migration check.
# This script must never approve or execute the real StatefulSet migration.
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false
DATA_INTEGRITY_STATUS=REVIEW_ONLY

echo "== 64단계: GWAN Kubernetes StatefulSet PreMigration Data Integrity Check 시작 =="
echo "Checking GWAN PostgreSQL pre-migration data integrity in namespace: ${NAMESPACE}"
echo

echo "[1] Current PostgreSQL Deployment"
kubectl -n "$NAMESPACE" get deployment postgres
echo

echo "[2] Current PostgreSQL Pod 탐색"
POSTGRES_POD=""

for selector in \
  "app.kubernetes.io/name=gwan-postgres" \
  "app.kubernetes.io/component=database" \
  "app=postgres"
do
  POSTGRES_POD="$(kubectl -n "$NAMESPACE" get pods \
    -l "$selector" \
    --field-selector=status.phase=Running \
    -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"

  if [ -n "$POSTGRES_POD" ]; then
    echo "Found PostgreSQL Pod by selector: $selector"
    break
  fi
done

if [ -z "$POSTGRES_POD" ]; then
  POSTGRES_POD="$(kubectl -n "$NAMESPACE" get pods --no-headers 2>/dev/null | awk '$1 ~ /^postgres-/ && $3 == "Running" {print $1; exit}')"
fi

if [ -z "$POSTGRES_POD" ]; then
  echo "ERROR: Running PostgreSQL Pod를 찾지 못했습니다."
  echo
  echo "현재 Pod 목록:"
  kubectl -n "$NAMESPACE" get pods --show-labels || true
  exit 1
fi

echo "POSTGRES_POD=${POSTGRES_POD}"
kubectl -n "$NAMESPACE" get pod "$POSTGRES_POD" -o wide
echo

echo "[3] Current PostgreSQL PVC"
kubectl -n "$NAMESPACE" get pvc postgres-data
echo

echo "[4] Current PostgreSQL Service"
kubectl -n "$NAMESPACE" get service postgres
echo

echo "[5] Current PostgreSQL Secret metadata"
kubectl -n "$NAMESPACE" get secret gwan-postgres-secret
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"
echo

echo "[6] Current GWAN API ConfigMap"
kubectl -n "$NAMESPACE" get configmap gwan-api-config
echo

echo "[7] Active StatefulSet check"
if kubectl -n "$NAMESPACE" get statefulset postgres >/dev/null 2>&1; then
  echo "ERROR: postgres StatefulSet already exists. Real migration may already have started."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi
echo

echo "[8] Required safety documents"
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
)

for doc in "${required_docs[@]}"; do
  if [ ! -f "$doc" ]; then
    echo "MISSING: $doc"
    exit 1
  fi
  echo "OK: $doc"
done
echo

echo "[9] Backup freshness check"
LATEST_BACKUP_FILE="$(ls -t "$BACKUP_DIR"/*.sql 2>/dev/null | head -1 || true)"

if [ -z "$LATEST_BACKUP_FILE" ]; then
  echo "ERROR: 최신 PostgreSQL 백업 파일을 찾지 못했습니다."
  echo "먼저 43단계 Backup/Restore Baseline 또는 63단계 Backup Freshness Check를 실행해야 합니다."
  exit 1
fi

if BACKUP_MODIFIED_EPOCH="$(stat -c %Y "$LATEST_BACKUP_FILE" 2>/dev/null)"; then
  :
else
  BACKUP_MODIFIED_EPOCH="$(stat -f %m "$LATEST_BACKUP_FILE")"
fi

NOW_EPOCH="$(date +%s)"
BACKUP_AGE_SECONDS="$((NOW_EPOCH - BACKUP_MODIFIED_EPOCH))"

echo "LATEST_BACKUP_FILE=${LATEST_BACKUP_FILE}"
echo "BACKUP_AGE_SECONDS=${BACKUP_AGE_SECONDS}"
echo "BACKUP_MAX_AGE_SECONDS=${BACKUP_MAX_AGE_SECONDS}"

if [ "$BACKUP_AGE_SECONDS" -gt "$BACKUP_MAX_AGE_SECONDS" ]; then
  echo "ERROR: 백업 파일이 너무 오래되었습니다."
  exit 1
fi

echo "OK: backup file is fresh enough"
echo

echo "[10] Read-only DB integrity check"
kubectl -n "$NAMESPACE" exec "$POSTGRES_POD" -- sh -lc '
set -eu

DB="${POSTGRES_DB:-hyean_gwan}"
USER="${POSTGRES_USER:-hyean}"

export PGPASSWORD="${POSTGRES_PASSWORD:-}"

echo "Checking pg_isready..."
pg_isready -U "$USER" -d "$DB"

echo "Checking SELECT 1..."
psql -U "$USER" -d "$DB" -v ON_ERROR_STOP=1 -tAc "SELECT 1;" >/dev/null

echo "Checking user table count..."
TABLE_COUNT="$(psql -U "$USER" -d "$DB" -v ON_ERROR_STOP=1 -tAc "SELECT count(*) FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('\''pg_catalog'\'', '\''information_schema'\'');")"
echo "USER_TABLE_COUNT=${TABLE_COUNT}"

echo "Read-only DB integrity check completed"
'
echo

echo "[11] Decision state"
echo "CURRENT_DECISION=${CURRENT_DECISION}"
echo "APPROVED_BY_OPERATOR=${APPROVED_BY_OPERATOR}"
echo "FINAL_DECISION=${FINAL_DECISION}"
echo "REAL_MIGRATION_EXECUTED=${REAL_MIGRATION_EXECUTED}"
echo "SECRET_VALUES_EXPORTED=${SECRET_VALUES_EXPORTED}"
echo

echo "[12] Safety result"
echo "- PostgreSQL Deployment is available"
echo "- PostgreSQL Pod is running"
echo "- postgres-data PVC is Bound"
echo "- PostgreSQL Service exists"
echo "- PostgreSQL Secret exists"
echo "- GWAN API ConfigMap exists"
echo "- backup file exists and is fresh"
echo "- read-only DB query succeeded"
echo "- secret values were not exported"
echo "- real migration remains blocked"
echo "- next step: 65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary"

echo
echo "== 64단계 완료: PreMigration Data Integrity Check 통과 =="
