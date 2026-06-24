#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-hyean-gwan}"
PDB_NAME="${PDB_NAME:-gwan-api-pdb}"

echo "Checking PodDisruptionBudget in namespace: ${NAMESPACE}"

kubectl -n "${NAMESPACE}" get pdb "${PDB_NAME}"
kubectl -n "${NAMESPACE}" describe pdb "${PDB_NAME}"

echo
echo "[PDB YAML]"
kubectl -n "${NAMESPACE}" get pdb "${PDB_NAME}" -o yaml

echo
echo "Expected policy:"
echo "- GWAN API PDB exists"
echo "- minAvailable: 1"
echo "- selector matches app.kubernetes.io/name=gwan-api"
echo
echo "Note:"
echo "If GWAN API has only 1 replica, ALLOWED DISRUPTIONS can be 0."
echo "That is expected because the PDB is protecting the only available Pod."
