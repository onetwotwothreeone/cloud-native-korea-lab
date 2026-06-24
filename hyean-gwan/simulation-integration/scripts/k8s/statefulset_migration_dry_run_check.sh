#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"

echo "Checking GWAN PostgreSQL StatefulSet migration dry-run readiness"
echo

echo "[1] Current PostgreSQL Deployment"
kubectl -n "$NS" get deployment postgres

echo
echo "[2] Current PostgreSQL Pod"
kubectl -n "$NS" get pods -l app.kubernetes.io/name=gwan-postgres -o wide

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "$NS" get pvc postgres-data

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "$NS" get service postgres

echo
echo "[5] Current Secret"
kubectl -n "$NS" get secret gwan-postgres-secret

echo
echo "[6] Draft StatefulSet render"
kubectl kustomize k8s/drafts >/tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "kind: StatefulSet" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "serviceName: postgres-headless" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "volumeClaimTemplates:" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
echo "StatefulSet draft render OK"

echo
echo "[7] Backup/restore baseline script"
test -x scripts/k8s/postgres_backup_restore_check.sh
echo "Backup/restore baseline script exists"

echo
echo "[8] Active StatefulSet check"
if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: postgres StatefulSet already exists. Migration may have started."
else
  echo "No active postgres StatefulSet yet: OK"
fi

echo
echo "[9] Dry-run decision"
echo "- Current database is still Deployment"
echo "- PVC is available"
echo "- Backup/restore check script exists"
echo "- StatefulSet draft renders successfully"
echo "- Actual StatefulSet migration is NOT executed in this step"

echo
echo "[10] Next safe action"
echo "Run backup/restore baseline again before any real migration:"
echo "scripts/k8s/postgres_backup_restore_check.sh"
