#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

echo "Checking Kubernetes resource requests and limits in namespace: ${NAMESPACE}"

echo "\n[gwan-api resources]"
kubectl -n "${NAMESPACE}" get deployment gwan-api \
  -o jsonpath='{range .spec.template.spec.containers[*]}{.name}{" requests.cpu="}{.resources.requests.cpu}{" requests.memory="}{.resources.requests.memory}{" limits.cpu="}{.resources.limits.cpu}{" limits.memory="}{.resources.limits.memory}{"\n"}{end}'

echo "\n[postgres resources]"
kubectl -n "${NAMESPACE}" get deployment postgres \
  -o jsonpath='{range .spec.template.spec.containers[*]}{.name}{" requests.cpu="}{.resources.requests.cpu}{" requests.memory="}{.resources.requests.memory}{" limits.cpu="}{.resources.limits.cpu}{" limits.memory="}{.resources.limits.memory}{"\n"}{end}'
