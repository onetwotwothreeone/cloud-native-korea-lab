#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="hyean-gwan"

echo "[HYEAN/GWAN] Namespace: ${NAMESPACE}"
kubectl get namespace "$NAMESPACE"

echo "[HYEAN/GWAN] Pods:"
kubectl -n "$NAMESPACE" get pods -o wide

echo "[HYEAN/GWAN] Services:"
kubectl -n "$NAMESPACE" get svc

echo "[HYEAN/GWAN] Deployments:"
kubectl -n "$NAMESPACE" get deploy

echo "[HYEAN/GWAN] Recent events:"
kubectl -n "$NAMESPACE" get events --sort-by=.lastTimestamp | tail -20
