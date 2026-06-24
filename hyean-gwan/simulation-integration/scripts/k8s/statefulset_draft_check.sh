#!/usr/bin/env bash
set -euo pipefail

echo "Checking GWAN PostgreSQL StatefulSet draft manifest"

echo
echo "[1] Draft files"
test -f k8s/drafts/postgres-headless-service-draft.yaml
test -f k8s/drafts/postgres-statefulset-draft.yaml
test -f k8s/drafts/kustomization.yaml
echo "draft files exist"

echo
echo "[2] Kustomize render"
kubectl kustomize k8s/drafts >/tmp/gwan-postgres-statefulset-draft-rendered.yaml
echo "Kustomize render OK"

echo
echo "[3] Expected draft fields"
grep -q "kind: StatefulSet" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "name: postgres" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "serviceName: postgres-headless" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "volumeClaimTemplates:" /tmp/gwan-postgres-statefulset-draft-rendered.yaml
grep -q "claimName" /tmp/gwan-postgres-statefulset-draft-rendered.yaml && {
  echo "ERROR: StatefulSet draft should use volumeClaimTemplates, not direct claimName."
  exit 1
} || true

echo
echo "[4] Current active workload check"
if kubectl -n hyean-gwan get deployment postgres >/dev/null 2>&1; then
  echo "Current active PostgreSQL workload is still Deployment: OK"
else
  echo "Current PostgreSQL Deployment not found. Check manually."
fi

if kubectl -n hyean-gwan get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: postgres StatefulSet already exists in cluster."
else
  echo "No active postgres StatefulSet yet: OK"
fi

echo
echo "[5] Result"
echo "- StatefulSet draft exists"
echo "- Headless Service draft exists"
echo "- Draft renders successfully"
echo "- Draft is not applied to local overlay yet"
echo "- Safe next step is migration dry-run/runbook"
