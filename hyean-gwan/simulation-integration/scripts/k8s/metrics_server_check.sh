#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"
HPA_NAME="${HPA_NAME:-gwan-api-hpa}"
METRICS_APISERVICE="v1beta1.metrics.k8s.io"

echo "Checking Metrics Server and HPA readiness for namespace: ${NAMESPACE}"

echo "[1/5] HPA object"
kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}"

echo "[2/5] HPA target reference"
TARGET_NAME="$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.scaleTargetRef.name}')"
if [ "${TARGET_NAME}" != "gwan-api" ]; then
  echo "Unexpected HPA target: ${TARGET_NAME}"
  exit 1
fi

echo "[3/5] Metrics APIService"
if ! kubectl get apiservice "${METRICS_APISERVICE}" >/dev/null 2>&1; then
  echo "Metrics APIService ${METRICS_APISERVICE} is not installed."
  echo "HPA object is valid, but CPU metrics may show <unknown> until metrics-server is installed."
  echo "This is acceptable for this baseline check in Docker Desktop or kind."
  exit 0
fi

kubectl get apiservice "${METRICS_APISERVICE}"
AVAILABLE="$(kubectl get apiservice "${METRICS_APISERVICE}" -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' 2>/dev/null || true)"
if [ "${AVAILABLE}" != "True" ]; then
  echo "Metrics APIService exists but is not Available yet: ${AVAILABLE:-unknown}"
  echo "HPA object is present, but usage values may still be <unknown>."
  exit 0
fi

echo "[4/5] kubectl top smoke check"
kubectl top nodes || true
kubectl top pods -n "${NAMESPACE}" || true

echo "[5/5] HPA description"
kubectl -n "${NAMESPACE}" describe hpa "${HPA_NAME}" || true

echo "Metrics Server and HPA readiness baseline check completed."
