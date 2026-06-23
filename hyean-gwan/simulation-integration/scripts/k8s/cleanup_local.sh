#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="hyean-gwan"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KUSTOMIZE_PATH="k8s/overlays/local"

cd "$BASE_DIR"

echo "[HYEAN/GWAN] Deleting local Kubernetes overlay resources..."
kubectl delete -k "$KUSTOMIZE_PATH" --ignore-not-found=true

echo "[HYEAN/GWAN] Cleanup requested."
echo "If the namespace remains terminating, check finalizers or wait a few seconds."
kubectl get namespace "$NAMESPACE" || true
