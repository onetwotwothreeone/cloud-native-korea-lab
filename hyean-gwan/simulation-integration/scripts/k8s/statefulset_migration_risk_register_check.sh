#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

NAMESPACE="hyean-gwan"
DOC="docs/60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register.md"

echo "Checking GWAN StatefulSet migration risk register in namespace: ${NAMESPACE}"
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

echo "[8] Risk register document check"
test -f "${DOC}"
grep -q "Migration Risk Register" "${DOC}"
grep -q "CURRENT_DECISION=NO_GO" "${DOC}"
grep -q "APPROVED_BY_OPERATOR=false" "${DOC}"
grep -q "FINAL_DECISION=NO_GO" "${DOC}"
grep -q "RISK_REGISTER_STATUS=REVIEW_ONLY" "${DOC}"
grep -q "Data loss during migration" "${DOC}"
grep -q "PostgreSQL downtime" "${DOC}"
grep -q "PVC mismatch" "${DOC}"
grep -q "Secret mismatch" "${DOC}"
grep -q "ConfigMap mismatch" "${DOC}"
grep -q "Service routing error" "${DOC}"
grep -q "StatefulSet manifest error" "${DOC}"
grep -q "Rollback plan missing" "${DOC}"
grep -q "Operator approval confusion" "${DOC}"
grep -q "Real migration remains blocked" "${DOC}"
grep -q "61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist" "${DOC}"
echo "OK: risk register document is valid"
echo

echo "[9] Decision state"
echo "CURRENT_DECISION=NO_GO"
echo "APPROVED_BY_OPERATOR=false"
echo "FINAL_DECISION=NO_GO"
echo "RISK_REGISTER_STATUS=REVIEW_ONLY"
echo

echo "[10] Risk register result"
echo "- migration risks are documented"
echo "- prevention actions are documented"
echo "- recovery actions are documented"
echo "- PostgreSQL remains Deployment + PVC"
echo "- active StatefulSet does not exist yet"
echo "- real migration remains blocked"
echo "- next step: 61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist"
