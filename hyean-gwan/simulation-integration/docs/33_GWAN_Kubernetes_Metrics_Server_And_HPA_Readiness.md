# 33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness

## Purpose

This step connects the previous HPA baseline to the Kubernetes resource metrics pipeline.

Step 32 created the `gwan-api-hpa` object. Step 33 checks whether the cluster has the Metrics API available through Metrics Server, and documents why HPA CPU values can show `<unknown>` in local or kind clusters.

## Beginner explanation

HPA is like an automatic staff manager.

- If many people arrive, it can open more counters.
- If fewer people arrive, it can close extra counters.

But the manager needs a thermometer. In Kubernetes, that thermometer is the resource metrics pipeline.

- Metrics Server collects CPU and memory usage.
- The Metrics API exposes that data to Kubernetes.
- HPA uses that data to decide whether to scale Pods.

## What was added

```text
scripts/k8s/metrics_server_check.sh
scripts/k8s/install_metrics_server_local.sh
docs/33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness.md
tests/test_gwan_kubernetes_metrics_server_hpa_readiness.py
```

The GitHub Actions workflow also checks that the metrics readiness script exists and runs safely.

## Important local note

Docker Desktop Kubernetes and kind do not always have Metrics Server ready by default.

That means this command may show `<unknown>` for CPU:

```bash
kubectl -n hyean-gwan get hpa
```

This is not a GWAN API failure.
It usually means the cluster does not yet provide `metrics.k8s.io` resource metrics.

## Check commands

```bash
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl top nodes
kubectl top pods -n hyean-gwan
kubectl -n hyean-gwan get hpa
kubectl -n hyean-gwan describe hpa gwan-api-hpa
```

## Script usage

```bash
scripts/k8s/metrics_server_check.sh
```

This script is intentionally safe for CI. If Metrics Server is not installed, it explains the situation and exits successfully, because the current milestone is readiness documentation and HPA object validation rather than live load-based scaling.

## Optional local install

For local learning only:

```bash
scripts/k8s/install_metrics_server_local.sh
```

After installation, wait a little and then run:

```bash
kubectl top nodes
kubectl top pods -n hyean-gwan
scripts/k8s/metrics_server_check.sh
```

## Learning point

HPA has two layers:

1. The HPA object exists and points to the target Deployment.
2. The metrics pipeline provides actual CPU and memory values.

Step 32 completed the first layer.
Step 33 checks and documents the second layer.
