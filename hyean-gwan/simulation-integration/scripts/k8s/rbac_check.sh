#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN ServiceAccounts and RBAC in namespace: ${NAMESPACE}"

kubectl -n "${NAMESPACE}" get serviceaccount gwan-api-sa
kubectl -n "${NAMESPACE}" get serviceaccount gwan-postgres-sa

echo
echo "[Roles]"
kubectl -n "${NAMESPACE}" get role gwan-api-minimal-role
kubectl -n "${NAMESPACE}" get role gwan-postgres-minimal-role

echo
echo "[RoleBindings]"
kubectl -n "${NAMESPACE}" get rolebinding gwan-api-minimal-rolebinding
kubectl -n "${NAMESPACE}" get rolebinding gwan-postgres-minimal-rolebinding

echo
echo "[Deployment ServiceAccount bindings]"
kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.serviceAccountName}{"\n"}'
kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.serviceAccountName}{"\n"}'

echo
echo "[ServiceAccount token automount]"
kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.automountServiceAccountToken}{"\n"}'
kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.automountServiceAccountToken}{"\n"}'

echo
echo "[Permission sample checks]"
kubectl auth can-i get pods --as="system:serviceaccount:${NAMESPACE}:gwan-api-sa" -n "${NAMESPACE}" || true
kubectl auth can-i get secrets --as="system:serviceaccount:${NAMESPACE}:gwan-postgres-sa" -n "${NAMESPACE}" || true

echo
echo "Expected policy:"
echo "- gwan-api uses gwan-api-sa"
echo "- postgres uses gwan-postgres-sa"
echo "- service account token automount is false"
echo "- minimal roles have no Kubernetes API permissions"
