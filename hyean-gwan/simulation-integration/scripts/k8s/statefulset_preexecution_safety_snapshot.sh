#!/usr/bin/env bash
set -euo pipefail

NS="hyean-gwan"
TS="$(date +%Y%m%d%H%M%S)"
OUT_DIR=".local/k8s-safety-snapshots/preexecution-${TS}"

mkdir -p "${OUT_DIR}"

echo "Checking GWAN StatefulSet pre-execution safety snapshot in namespace: ${NS}"
echo "Snapshot directory: ${OUT_DIR}"

echo ""
echo "[1] PostgreSQL Deployment snapshot"
kubectl -n "${NS}" get deployment postgres -o wide | tee "${OUT_DIR}/postgres-deployment.txt"
kubectl -n "${NS}" get deployment postgres -o yaml > "${OUT_DIR}/postgres-deployment.yaml"

READY_REPLICAS="$(kubectl -n "${NS}" get deployment postgres -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo 0)"
if [ "${READY_REPLICAS:-0}" = "0" ]; then
  echo "ERROR: PostgreSQL Deployment has no ready replicas."
  exit 1
fi

echo ""
echo "[2] PostgreSQL Pod snapshot"
kubectl -n "${NS}" get pods -o wide | tee "${OUT_DIR}/all-pods.txt"

POSTGRES_POD_COUNT="$(kubectl -n "${NS}" get pods --no-headers 2>/dev/null | awk '/^postgres-/ && $3=="Running"{count++} END{print count+0}')"
if [ "${POSTGRES_POD_COUNT}" = "0" ]; then
  echo "ERROR: No running postgres pod found by postgres-* pod name."
  exit 1
fi
echo "Running postgres pod count: ${POSTGRES_POD_COUNT}" | tee "${OUT_DIR}/postgres-pod-count.txt"

echo ""
echo "[3] PostgreSQL PVC snapshot"
kubectl -n "${NS}" get pvc postgres-data -o wide | tee "${OUT_DIR}/postgres-pvc.txt"
kubectl -n "${NS}" get pvc postgres-data -o yaml > "${OUT_DIR}/postgres-pvc.yaml"

PVC_PHASE="$(kubectl -n "${NS}" get pvc postgres-data -o jsonpath='{.status.phase}' 2>/dev/null || echo "")"
if [ "${PVC_PHASE}" != "Bound" ]; then
  echo "ERROR: postgres-data PVC is not Bound."
  exit 1
fi

echo ""
echo "[4] PostgreSQL Service snapshot"
kubectl -n "${NS}" get service postgres -o wide | tee "${OUT_DIR}/postgres-service.txt"
kubectl -n "${NS}" get service postgres -o yaml > "${OUT_DIR}/postgres-service.yaml"

echo ""
echo "[5] PostgreSQL Secret metadata snapshot"
kubectl -n "${NS}" get secret gwan-postgres-secret | tee "${OUT_DIR}/postgres-secret-metadata.txt"
echo "SECRET_VALUES_EXPORTED=false" | tee "${OUT_DIR}/secret-handling.txt"
echo "SECRET_METADATA_ONLY=true" | tee -a "${OUT_DIR}/secret-handling.txt"

echo ""
echo "[6] GWAN API ConfigMap snapshot"
kubectl -n "${NS}" get configmap gwan-api-config -o yaml | tee "${OUT_DIR}/gwan-api-configmap.yaml" >/dev/null
kubectl -n "${NS}" get configmap gwan-api-config | tee "${OUT_DIR}/gwan-api-configmap.txt"

echo ""
echo "[7] Active StatefulSet check"
if kubectl -n "${NS}" get statefulset postgres >/dev/null 2>&1; then
  echo "ERROR: Active postgres StatefulSet already exists. Stop before real migration."
  exit 1
else
  echo "OK: No active postgres StatefulSet exists yet." | tee "${OUT_DIR}/statefulset-status.txt"
fi

echo ""
echo "[8] Rollout status snapshot"
kubectl -n "${NS}" rollout status deployment/postgres --timeout=180s | tee "${OUT_DIR}/postgres-rollout.txt"
kubectl -n "${NS}" rollout status deployment/gwan-api --timeout=180s | tee "${OUT_DIR}/gwan-api-rollout.txt"

echo ""
echo "[9] Required safety documents"
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
)

missing=0
for doc in "${required_docs[@]}"; do
  if [ -f "${doc}" ]; then
    echo "OK: ${doc}" | tee -a "${OUT_DIR}/required-documents.txt"
  else
    echo "MISSING: ${doc}" | tee -a "${OUT_DIR}/required-documents.txt"
    missing=1
  fi
done

if [ "${missing}" = "1" ]; then
  echo "ERROR: Some required safety documents are missing."
  exit 1
fi

echo ""
echo "[10] Event summary snapshot"
kubectl -n "${NS}" get events --sort-by=.lastTimestamp | tail -40 > "${OUT_DIR}/events-tail.txt" || true

echo ""
echo "[11] Decision state"
cat > "${OUT_DIR}/decision-state.txt" <<DECISION
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
REAL_MIGRATION_EXECUTED=false
PREEXECUTION_SNAPSHOT_CREATED=true
SECRET_VALUES_EXPORTED=false
SECRET_METADATA_ONLY=true
NEXT_STEP=63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check
DECISION

cat "${OUT_DIR}/decision-state.txt"

echo ""
echo "[12] Safety result"
echo "- pre-execution safety snapshot created"
echo "- PostgreSQL Deployment is available"
echo "- postgres pod is running"
echo "- postgres-data PVC is Bound"
echo "- PostgreSQL Service exists"
echo "- PostgreSQL Secret metadata exists"
echo "- GWAN API ConfigMap exists"
echo "- no active postgres StatefulSet exists yet"
echo "- secret values were not exported"
echo "- real migration remains blocked"
echo "- next step: 63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check"
