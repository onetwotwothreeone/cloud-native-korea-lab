# Codex task: 29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline

## Goal

Add a first Kubernetes operations baseline for GWAN.

## Add or update

```text
k8s/base/gwan-api-deployment.yaml
scripts/k8s/rollout_check.sh
scripts/k8s/health_readiness_check.sh
scripts/k8s/diagnostics.sh
docs/29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline.md
tests/test_gwan_kubernetes_observability_baseline.py
```

## Required checks

- gwan-api Deployment has startupProbe, readinessProbe, and livenessProbe.
- health endpoint remains `/health`.
- diagnostics script includes events, describe, and logs.
- tests pass with `python -m pytest -q`.
