#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"

echo "Checking GWAN PostgreSQL StatefulSet migration cutover checklist"
echo

echo "[1] Current PostgreSQL Deployment"
kubectl -n "$NS" get deployment postgres

AVAILABLE_REPLICAS="$(kubectl -n "$NS" get deployment postgres -o jsonpath='{.status.availableReplicas}' || true)"
if [ "${AVAILABLE_REPLICAS:-0}" = "0" ] || [ -z "${AVAILABLE_REPLICAS:-}" ]; then
  echo "NO-GO: PostgreSQL Deployment has no available replicas"
  exit 1
fi
echo "PostgreSQL Deployment available replicas: $AVAILABLE_REPLICAS"

echo
echo "[2] Current PostgreSQL Pod"
kubectl -n "$NS" get pods -l app.kubernetes.io/name=gwan-postgres -o wide

RUNNING_PODS="$(kubectl -n "$NS" get pods -l app.kubernetes.io/name=gwan-postgres --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l | tr -d ' ')"
if [ "${RUNNING_PODS:-0}" = "0" ]; then
  echo "NO-GO: No Running PostgreSQL Pod"
  exit 1
fi
echo "Running PostgreSQL Pods: $RUNNING_PODS"

echo
echo "[3] Current PostgreSQL PVC"
kubectl -n "$NS" get pvc postgres-data

PVC_PHASE="$(kubectl -n "$NS" get pvc postgres-data -o jsonpath='{.status.phase}' || true)"
if [ "$PVC_PHASE" != "Bound" ]; then
  echo "NO-GO: postgres-data PVC is not Bound"
  exit 1
fi
echo "PVC phase: $PVC_PHASE"

echo
echo "[4] Current PostgreSQL Service"
kubectl -n "$NS" get service postgres

echo
echo "[5] Current PostgreSQL Secret"
kubectl -n "$NS" get secret gwan-postgres-secret

echo
echo "[6] Current GWAN API ConfigMap"
kubectl -n "$NS" get configmap gwan-api-config

echo
echo "[7] StatefulSet draft render check"
kubectl kustomize k8s/drafts >/tmp/gwan-statefulset-cutover-checklist.yaml

if ! grep -q "kind: StatefulSet" /tmp/gwan-statefulset-cutover-checklist.yaml; then
  echo "NO-GO: StatefulSet draft does not contain kind: StatefulSet"
  exit 1
fi

if ! grep -q "postgres-headless" /tmp/gwan-statefulset-cutover-checklist.yaml; then
  echo "NO-GO: StatefulSet draft does not contain postgres-headless service"
  exit 1
fi

if ! grep -q "volumeClaimTemplates:" /tmp/gwan-statefulset-cutover-checklist.yaml; then
  echo "NO-GO: StatefulSet draft does not contain volumeClaimTemplates"
  exit 1
fi

if ! grep -q "name: postgres-data" /tmp/gwan-statefulset-cutover-checklist.yaml; then
  echo "NO-GO: StatefulSet draft does not contain postgres-data volume claim template"
  exit 1
fi

echo "StatefulSet draft render OK"

echo
echo "[8] Active StatefulSet check"
if kubectl -n "$NS" get statefulset postgres >/dev/null 2>&1; then
  echo "NO-GO: postgres StatefulSet already exists"
  exit 1
else
  echo "No active postgres StatefulSet yet: OK"
fi

echo
echo "[9] Required safety assets"
test -x scripts/k8s/postgres_backup_restore_check.sh
test -x scripts/k8s/statefulset_migration_dry_run_check.sh
test -x scripts/k8s/statefulset_migration_runbook_check.sh
test -x scripts/k8s/statefulset_migration_rollback_dry_run_check.sh
test -f docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md
test -f docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md
test -f docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
test -f docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md
echo "Required safety assets exist"

echo
echo "[10] Manual decision gate"
echo "CUTOVER_DECISION_REQUIRED=true"
echo "CURRENT_DECISION=NO-GO"
echo "Reason: real migration must be approved manually by the operator"

echo
echo "[11] Cutover checklist result"
echo "- pytest should pass before cutover"
echo "- GitHub Actions should pass before cutover"
echo "- PostgreSQL Deployment is available"
echo "- PostgreSQL Pod is running"
echo "- PostgreSQL PVC is Bound"
echo "- PostgreSQL Service exists"
echo "- PostgreSQL Secret exists"
echo "- GWAN API ConfigMap exists"
echo "- StatefulSet draft renders"
echo "- backup/restore baseline exists"
echo "- rollback dry run exists"
echo "- active StatefulSet does not exist yet"
echo "- real migration was NOT executed"
echo "- final decision remains NO-GO until operator approval"
