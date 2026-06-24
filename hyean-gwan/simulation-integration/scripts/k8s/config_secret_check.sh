#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN Kubernetes ConfigMap and Secret baseline in namespace: ${NAMESPACE}"

echo
echo "[ConfigMap]"
kubectl -n "${NAMESPACE}" get configmap gwan-api-config -o yaml

echo
echo "[Secret name]"
kubectl -n "${NAMESPACE}" get secret gwan-postgres-secret -o jsonpath='{.metadata.name}{"\n"}'

echo
echo "[Deployment env check]"
kubectl -n "${NAMESPACE}" get deployment gwan-api -o yaml | grep -E "DATABASE_HOST|DATABASE_PORT|DATABASE_NAME|DATABASE_DIALECT|HYEAN_MEMORY_JSONL_PATH|POSTGRES_PASSWORD|secretKeyRef|configMapKeyRef" || true

echo
echo "[Expected checks]"
echo "- ConfigMap contains non-sensitive runtime settings"
echo "- Secret contains PostgreSQL credentials"
echo "- gwan-api reads database settings from ConfigMap"
echo "- gwan-api reads PostgreSQL password from Secret"
echo "- postgres reads PostgreSQL credentials from Secret"
echo "- raw database password is not hardcoded in ConfigMap or Deployment"
