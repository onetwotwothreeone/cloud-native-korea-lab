# 32_GWAN_Kubernetes_HPA_Autoscaling_Baseline

## Purpose

This step adds a first HorizontalPodAutoscaler baseline for the GWAN API Deployment.

Until now, the HYEAN/GWAN Kubernetes work focused on deployment, health checks, configuration separation, and resource boundaries. This step adds an autoscaling policy so the API can increase or decrease replica count when CPU utilization changes.

## Simple mental model

- Deployment = the machine that runs GWAN API
- Resource requests/limits = how much CPU and memory each machine may use
- HorizontalPodAutoscaler = the automatic operator that can add or remove GWAN API machines

## Files added or changed

```text
k8s/base/gwan-api-hpa.yaml
k8s/base/kustomization.yaml
scripts/k8s/hpa_check.sh
docs/32_GWAN_Kubernetes_HPA_Autoscaling_Baseline.md
tests/test_gwan_kubernetes_hpa_autoscaling.py
.github/workflows/gwan-ci.yml
```

## HPA policy

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gwan-api-hpa
  namespace: hyean-gwan
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gwan-api
  minReplicas: 1
  maxReplicas: 3
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Why this baseline is conservative

This project is still in a learning and portfolio-building phase.

The API baseline uses:

```text
minReplicas: 1
maxReplicas: 3
averageUtilization: 70
```

This means:

- at least one GWAN API pod should exist
- no more than three GWAN API pods should be created
- scaling should target roughly 70 percent CPU utilization

The limit is intentionally small because Docker Desktop and kind are local learning environments.

## Important metrics-server note

The HPA object can be created without metrics-server, but CPU metrics may show as `<unknown>` until a metrics provider is installed.

This is expected in many local Docker Desktop or kind setups.

For this step, success means:

```text
HPA manifest exists
HPA is included in kustomization
HPA targets deployment/gwan-api
HPA can be applied and inspected
```

It does not require real load-based scaling yet.

## Local commands

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
```

Direct check:

```bash
kubectl -n hyean-gwan get hpa
kubectl -n hyean-gwan describe hpa gwan-api-hpa
```

## Next step

The next logical step is to improve autoscaling readiness by preparing metrics-server or documenting the difference between local learning autoscaling and production autoscaling.
