#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"

echo "Checking GWAN API health at ${BASE_URL}"
curl -fsS "${BASE_URL}/health"
echo
echo "Checking GWAN database status through API"
curl -fsS "${BASE_URL}/gwan/memory/db-status"
echo
