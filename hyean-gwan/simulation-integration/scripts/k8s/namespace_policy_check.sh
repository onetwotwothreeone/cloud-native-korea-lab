#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"

printf 'Checking Kubernetes namespace policy in namespace: %s
' "$NAMESPACE"

printf '
[ResourceQuota]
'
kubectl -n "$NAMESPACE" get resourcequota hyean-gwan-resource-quota
kubectl -n "$NAMESPACE" describe resourcequota hyean-gwan-resource-quota

printf '
[LimitRange]
'
kubectl -n "$NAMESPACE" get limitrange hyean-gwan-default-container-limits
kubectl -n "$NAMESPACE" describe limitrange hyean-gwan-default-container-limits
