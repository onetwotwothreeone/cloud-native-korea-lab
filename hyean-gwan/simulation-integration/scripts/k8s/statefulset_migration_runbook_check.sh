#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"
DOC="docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md"

echo "Checking GWAN StatefulSet migration runbook readiness"
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
echo "[6] StatefulSet draft render"
kubectl kustomize k8s/drafts >/tmp/gwan-statefulset-runbook-draft.yaml
grep -q "kind: StatefulSet" /tmp/gwan-statefulset-runbook-draft.yaml
grep -q "postgres-headless" /tmp/gwan-statefulset-runbook-draft.yaml
echo "StatefulSet draft render OK"

echo
echo "[7] Runbook document check"
test -f "$DOC"
grep -q "Migration Gates" "$DOC"
grep -q "Backup/Restore Gate" "$DOC"
grep -q "Rollback Plan" "$DOC"
grep -q "Stop Conditions" "$DOC"
grep -q "Never do database migration without a verified backup" "$DOC"
echo "Runbook document OK"

echo
echo "[8] Active StatefulSet check"
if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: postgres StatefulSet already exists."
else
  echo "No active postgres StatefulSet yet: OK"
fi

echo
echo "[9] Result"
echo "- Runbook exists"
echo "- Backup/restore gate exists"
echo "- Rollback plan exists"
echo "- Stop conditions exist"
echo "- Real migration is still not executed"
