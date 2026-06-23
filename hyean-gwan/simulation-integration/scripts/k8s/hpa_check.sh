#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${KUBERNETES_NAMESPACE:-hyean-gwan}"
HPA_NAME="${GWAN_HPA_NAME:-gwan-api-hpa}"

echo "Checking GWAN HorizontalPodAutoscaler in namespace: ${NAMESPACE}"
kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}"

echo "[${HPA_NAME} spec]"
echo "minReplicas=$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.minReplicas}')"
echo "maxReplicas=$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.maxReplicas}')"
echo "targetKind=$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.scaleTargetRef.kind}')"
echo "targetName=$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.scaleTargetRef.name}')"
echo "cpuTarget=$(kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o jsonpath='{.spec.metrics[0].resource.target.averageUtilization}')"

echo "[${HPA_NAME} describe]"
kubectl -n "${NAMESPACE}" describe hpa "${HPA_NAME}" || true

echo "Note: Docker Desktop and kind clusters may show CPU metrics as <unknown> unless metrics-server is installed. The HPA object can still be applied and inspected."
