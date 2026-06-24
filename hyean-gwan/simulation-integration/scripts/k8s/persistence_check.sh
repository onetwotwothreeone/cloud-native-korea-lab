#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN PostgreSQL persistence baseline in namespace: ${NAMESPACE}"

echo ""
echo "[PVC]"
kubectl -n "${NAMESPACE}" get pvc postgres-data
kubectl -n "${NAMESPACE}" describe pvc postgres-data | sed -n '1,80p'

echo ""
echo "[PostgreSQL Deployment Volume]"
kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.volumes}'
echo ""

echo ""
echo "[PostgreSQL Pods]"
kubectl -n "${NAMESPACE}" get pods -l app.kubernetes.io/name=gwan-postgres -o wide

echo ""
echo "Expected policy:"
echo "- postgres-data PersistentVolumeClaim exists"
echo "- postgres deployment uses persistentVolumeClaim"
echo "- claimName is postgres-data"
echo "- postgres pod mounts postgres-data at /var/lib/postgresql/data"
