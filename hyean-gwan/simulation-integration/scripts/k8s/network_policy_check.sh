#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking GWAN NetworkPolicies in namespace: ${NAMESPACE}"

kubectl -n "${NAMESPACE}" get networkpolicy

echo
echo "[GWAN API NetworkPolicy]"
kubectl -n "${NAMESPACE}" describe networkpolicy gwan-api-network-policy

echo
echo "[GWAN PostgreSQL NetworkPolicy]"
kubectl -n "${NAMESPACE}" describe networkpolicy gwan-postgres-network-policy

echo
echo "Expected policy:"
echo "- gwan-api allows ingress on TCP 8000 from namespace Pods"
echo "- gwan-api allows egress to gwan-postgres on TCP 5432"
echo "- gwan-api allows DNS egress to kube-dns on TCP/UDP 53"
echo "- gwan-postgres allows ingress only from gwan-api on TCP 5432"
echo
echo "Note:"
echo "NetworkPolicy enforcement depends on the Kubernetes CNI plugin."
echo "Docker Desktop or kind may create NetworkPolicy objects even if actual traffic blocking is not enforced."
