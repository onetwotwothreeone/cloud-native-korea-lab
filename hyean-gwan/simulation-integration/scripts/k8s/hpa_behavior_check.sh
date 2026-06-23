#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"
HPA_NAME="${HPA_NAME:-gwan-api-hpa}"

echo "Checking HPA behavior policy in namespace: ${NAMESPACE}"

kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}"
kubectl -n "${NAMESPACE}" describe hpa "${HPA_NAME}"

echo
echo "[HPA YAML behavior section]"
kubectl -n "${NAMESPACE}" get hpa "${HPA_NAME}" -o yaml | grep -A 30 "behavior:" || true

echo
echo "Expected policy:"
echo "- scaleUp: 1 pod per 60 seconds"
echo "- scaleDown: 1 pod per 120 seconds after 300 seconds stabilization"
