#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAMESPACE="hyean-gwan"

echo "Checking GWAN StatefulSet migration command dry run in namespace: ${NAMESPACE}"
echo

echo "[1] Current PostgreSQL Deployment"
kubectl -n "${NAMESPACE}" get deployment postgres
echo

echo "[2] Current PostgreSQL Pod"
kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres -o wide
echo

echo "[3] Current PostgreSQL PVC"
kubectl -n "${NAMESPACE}" get pvc postgres-data
echo

echo "[4] Current PostgreSQL Service"
kubectl -n "${NAMESPACE}" get svc postgres
echo

echo "[5] Current PostgreSQL Secret"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret
echo

echo "[6] Current GWAN API ConfigMap"
kubectl -n "${NAMESPACE}" get configmap gwan-api-config
echo

echo "[7] Active StatefulSet check"
if kubectl -n "${NAMESPACE}" get statefulset postgres >/dev/null 2>&1; then
  echo "WARNING: active postgres StatefulSet exists."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi
echo

echo "[8] Draft manifest files"
test -f k8s/drafts/postgres-headless-service-draft.yaml
test -f k8s/drafts/postgres-statefulset-draft.yaml
echo "OK: draft manifest files exist"
echo

echo "[9] Render StatefulSet draft"
kubectl kustomize k8s/drafts >/tmp/gwan-statefulset-draft-rendered.yaml
test -s /tmp/gwan-statefulset-draft-rendered.yaml
grep -q "kind: StatefulSet" /tmp/gwan-statefulset-draft-rendered.yaml
grep -q "kind: Service" /tmp/gwan-statefulset-draft-rendered.yaml
echo "OK: StatefulSet draft rendered"
echo

echo "[10] Client dry-run apply"
kubectl apply --dry-run=client -f k8s/drafts/postgres-headless-service-draft.yaml
kubectl apply --dry-run=client -f k8s/drafts/postgres-statefulset-draft.yaml
echo "OK: dry-run apply completed"
echo

echo "[11] Decision state"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo

echo "[12] Safety result"
echo "- this script does not execute real migration"
echo "- this script only validates migration command readiness"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active StatefulSet does not exist yet"
echo "- next step: 59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review"
