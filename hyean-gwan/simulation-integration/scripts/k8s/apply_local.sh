#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="hyean-gwan"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KUSTOMIZE_PATH="k8s/overlays/local"
IMAGE_NAME="ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest"

cd "$BASE_DIR"

echo "[HYEAN/GWAN] Building local Docker image for Docker Desktop Kubernetes..."
docker build -t "$IMAGE_NAME" .

echo "[HYEAN/GWAN] Rendering local Kubernetes overlay..."
kubectl kustomize "$KUSTOMIZE_PATH" >/tmp/hyean-gwan-kustomize-local-rendered.yaml

echo "[HYEAN/GWAN] Applying local Kubernetes overlay..."
kubectl apply -k "$KUSTOMIZE_PATH"

echo "[HYEAN/GWAN] Waiting for PostgreSQL deployment..."
kubectl -n "$NAMESPACE" rollout status deployment/postgres --timeout=180s

echo "[HYEAN/GWAN] Waiting for GWAN API deployment..."
kubectl -n "$NAMESPACE" rollout status deployment/gwan-api --timeout=180s

echo "[HYEAN/GWAN] Current pods and services:"
kubectl -n "$NAMESPACE" get pods
kubectl -n "$NAMESPACE" get svc

echo "[HYEAN/GWAN] Local Kubernetes apply completed with k8s/overlays/local."
echo "Next: run scripts/k8s/port_forward_health_check.sh or use kubectl port-forward manually."
