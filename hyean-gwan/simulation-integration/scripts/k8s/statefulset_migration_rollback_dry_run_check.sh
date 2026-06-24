#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"

echo "Checking GWAN StatefulSet migration rollback dry-run readiness"
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
echo "[5] Current PostgreSQL Secret"
kubectl -n "$NS" get secret gwan-postgres-secret

echo
echo "[6] StatefulSet draft render check"
kubectl kustomize k8s/drafts >/tmp/gwan-statefulset-rollback-dry-run.yaml
grep -q "kind: StatefulSet" /tmp/gwan-statefulset-rollback-dry-run.yaml
grep -q "postgres-headless" /tmp/gwan-statefulset-rollback-dry-run.yaml
echo "StatefulSet draft render OK"

echo
echo "[7] Active StatefulSet check"
if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: postgres StatefulSet already exists."
  echo "Rollback dry run should be reviewed manually."
else
  echo "No active postgres StatefulSet yet: OK"
fi

echo
echo "[8] Backup/restore baseline check"
test -x scripts/k8s/postgres_backup_restore_check.sh
echo "Backup/restore baseline script exists"

echo
echo "[9] Migration runbook check"
test -f docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
grep -q "Rollback Plan" docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
grep -q "Never do database migration without a verified backup" docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
echo "Migration runbook contains rollback and backup safety rule"

echo
echo "[10] Rollback dry-run result"
echo "- current Deployment baseline exists"
echo "- current PVC exists"
echo "- StatefulSet draft renders"
echo "- backup/restore baseline exists"
echo "- rollback plan exists"
echo "- real rollback was NOT executed"
echo "- real migration is still NOT executed"
