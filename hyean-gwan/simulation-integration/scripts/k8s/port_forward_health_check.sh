#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="hyean-gwan"
LOCAL_PORT="8000"
SERVICE="svc/gwan-api"

echo "[HYEAN/GWAN] Starting port-forward ${SERVICE} ${LOCAL_PORT}:8000..."
kubectl -n "$NAMESPACE" port-forward "$SERVICE" "${LOCAL_PORT}:8000" >/tmp/hyean-gwan-port-forward.log 2>&1 &
PF_PID=$!

cleanup() {
  echo "[HYEAN/GWAN] Stopping port-forward..."
  kill "$PF_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

sleep 5

echo "[HYEAN/GWAN] Checking /health..."
curl -f "http://127.0.0.1:${LOCAL_PORT}/health"
echo

echo "[HYEAN/GWAN] Checking /gwan/memory/db-status..."
curl -f "http://127.0.0.1:${LOCAL_PORT}/gwan/memory/db-status"
echo

echo "[HYEAN/GWAN] Port-forward health check completed."
