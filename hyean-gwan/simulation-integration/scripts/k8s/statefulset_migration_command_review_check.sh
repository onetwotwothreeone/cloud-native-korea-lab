#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAMESPACE="hyean-gwan"

echo "Checking GWAN StatefulSet migration command review in namespace: ${NAMESPACE}"
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
  echo "ERROR: active postgres StatefulSet already exists."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet."
fi
echo

echo "[8] Required command review documents"
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
)

for doc in "${required_docs[@]}"; do
  test -f "${doc}"
  echo "OK: ${doc}"
done
echo

echo "[9] Render StatefulSet draft"
kubectl kustomize k8s/drafts >/tmp/gwan-statefulset-command-review-rendered.yaml
test -s /tmp/gwan-statefulset-command-review-rendered.yaml
grep -q "kind: StatefulSet" /tmp/gwan-statefulset-command-review-rendered.yaml
grep -q "kind: Service" /tmp/gwan-statefulset-command-review-rendered.yaml
echo "OK: StatefulSet draft rendered"
echo

echo "[10] Client dry-run apply only"
kubectl apply --dry-run=client -f k8s/drafts/postgres-headless-service-draft.yaml
kubectl apply --dry-run=client -f k8s/drafts/postgres-statefulset-draft.yaml
echo "OK: dry-run apply completed"
echo

echo "[11] Decision state"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo "COMMAND_REVIEW_STATUS=REVIEW_ONLY"
echo

echo "[12] Command review result"
echo "- command order is reviewable"
echo "- this script does not execute real migration"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active StatefulSet does not exist yet"
echo "- real migration remains blocked"
echo "- next step: 60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register"
