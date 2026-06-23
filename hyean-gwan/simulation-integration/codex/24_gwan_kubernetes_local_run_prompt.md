# Codex task: 24_GWAN_Kubernetes_Local_Run

## Goal

Add local Kubernetes run scripts and documentation for the GWAN API + PostgreSQL manifests created in step 23.

## Required files

```text
scripts/k8s/apply_local.sh
scripts/k8s/port_forward_health_check.sh
scripts/k8s/status.sh
scripts/k8s/cleanup_local.sh
docs/24_GWAN_Kubernetes_Local_Run.md
tests/test_gwan_kubernetes_local_run.py
```

## Required behavior

- `apply_local.sh` must run `kubectl apply -k k8s/base` and wait for `postgres` and `gwan-api` deployments.
- `port_forward_health_check.sh` must port-forward `svc/gwan-api` and check `/health` and `/gwan/memory/db-status`.
- `status.sh` must show namespace, pods, services, deployments, and recent events.
- `cleanup_local.sh` must run `kubectl delete -k k8s/base --ignore-not-found=true`.
- Documentation must explain manual and scripted run flows.

## Success command

```bash
python -m pytest -q
```
