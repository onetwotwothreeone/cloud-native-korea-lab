#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN Kubernetes SecurityContext baseline in namespace: ${NAMESPACE}"

echo
echo "[GWAN API Pod SecurityContext]"
kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.securityContext}{"\n"}'

echo
echo "[GWAN API Container SecurityContext]"
kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.containers[0].securityContext}{"\n"}'

echo
echo "[PostgreSQL Pod SecurityContext]"
kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.securityContext}{"\n"}'

echo
echo "[PostgreSQL Container SecurityContext]"
kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.containers[0].securityContext}{"\n"}'

echo
echo "[Expected checks]"

API_SECCOMP="$(kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.securityContext.seccompProfile.type}')"
API_NONROOT="$(kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.securityContext.runAsNonRoot}')"
API_NO_PRIV_ESC="$(kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.containers[0].securityContext.allowPrivilegeEscalation}')"
API_READONLY="$(kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.containers[0].securityContext.readOnlyRootFilesystem}')"
API_DROP="$(kubectl -n "${NAMESPACE}" get deployment gwan-api -o jsonpath='{.spec.template.spec.containers[0].securityContext.capabilities.drop[0]}')"

PG_SECCOMP="$(kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.securityContext.seccompProfile.type}')"
PG_NO_PRIV_ESC="$(kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.containers[0].securityContext.allowPrivilegeEscalation}')"
PG_DROP="$(kubectl -n "${NAMESPACE}" get deployment postgres -o jsonpath='{.spec.template.spec.containers[0].securityContext.capabilities.drop[0]}')"

test "${API_SECCOMP}" = "RuntimeDefault"
test "${API_NONROOT}" = "true"
test "${API_NO_PRIV_ESC}" = "false"
test "${API_READONLY}" = "true"
test "${API_DROP}" = "ALL"

test "${PG_SECCOMP}" = "RuntimeDefault"
test "${PG_NO_PRIV_ESC}" = "false"
test "${PG_DROP}" = "ALL"

echo "- gwan-api uses RuntimeDefault seccomp"
echo "- gwan-api runs as non-root"
echo "- gwan-api disables privilege escalation"
echo "- gwan-api uses read-only root filesystem"
echo "- gwan-api drops Linux capabilities"
echo "- postgres uses RuntimeDefault seccomp"
echo "- postgres disables privilege escalation"
echo "- postgres drops Linux capabilities"
