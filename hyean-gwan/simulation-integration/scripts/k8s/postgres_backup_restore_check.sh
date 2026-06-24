#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"
BACKUP_DIR="${BACKUP_DIR:-.local/postgres-backups}"
RESTORE_DB="${RESTORE_DB:-hyean_gwan_restore_check}"

mkdir -p "${BACKUP_DIR}"

echo "Checking GWAN PostgreSQL backup/restore baseline in namespace: ${NAMESPACE}"

POSTGRES_POD="$(
  kubectl -n "${NAMESPACE}" get pods \
    -l app.kubernetes.io/name=gwan-postgres \
    --no-headers 2>/dev/null \
  | awk '$3 == "Running" {print $1; exit}'
)"

if [ -z "${POSTGRES_POD}" ]; then
  echo "ERROR: running PostgreSQL Pod was not found."
  kubectl -n "${NAMESPACE}" get pods || true
  exit 1
fi

echo
echo "[1] PostgreSQL Pod"
echo "${POSTGRES_POD}"

BACKUP_FILE="${BACKUP_DIR}/gwan-postgres-$(date +%Y%m%d%H%M%S).sql"

echo
echo "[2] Creating backup with pg_dump"
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc \
  'PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges' \
  > "${BACKUP_FILE}"

if [ ! -s "${BACKUP_FILE}" ]; then
  echo "ERROR: backup file is empty."
  exit 1
fi

echo "Backup file created: ${BACKUP_FILE}"
wc -c "${BACKUP_FILE}"

echo
echo "[3] Creating temporary restore database"
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc \
  "PGPASSWORD=\"\$POSTGRES_PASSWORD\" dropdb -U \"\$POSTGRES_USER\" --if-exists ${RESTORE_DB}"

kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc \
  "PGPASSWORD=\"\$POSTGRES_PASSWORD\" createdb -U \"\$POSTGRES_USER\" ${RESTORE_DB}"

echo
echo "[4] Restoring backup into temporary database"
kubectl -n "${NAMESPACE}" exec -i "${POSTGRES_POD}" -- sh -lc \
  "PGPASSWORD=\"\$POSTGRES_PASSWORD\" psql -v ON_ERROR_STOP=1 -U \"\$POSTGRES_USER\" -d ${RESTORE_DB}" \
  < "${BACKUP_FILE}" >/dev/null

echo
echo "[5] Restore verification"
TABLE_COUNT="$(
  kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc \
    "PGPASSWORD=\"\$POSTGRES_PASSWORD\" psql -U \"\$POSTGRES_USER\" -d ${RESTORE_DB} -tAc \"SELECT count(*) FROM information_schema.tables WHERE table_schema='public';\""
)"

echo "Restored public table count: ${TABLE_COUNT}"

echo
echo "[6] Cleaning up temporary restore database"
kubectl -n "${NAMESPACE}" exec "${POSTGRES_POD}" -- sh -lc \
  "PGPASSWORD=\"\$POSTGRES_PASSWORD\" dropdb -U \"\$POSTGRES_USER\" --if-exists ${RESTORE_DB}"

echo
echo "[7] Backup/restore baseline result"
echo "- pg_dump backup succeeded"
echo "- temporary restore database was created"
echo "- backup was restored safely"
echo "- temporary restore database was cleaned up"
echo "- main database was not overwritten"
