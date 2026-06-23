# 29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline

## Purpose

This step adds a small Kubernetes operations baseline for HYEAN/GWAN.

Previous step:

```text
Kubernetes can run GWAN API and PostgreSQL.
```

This step:

```text
Kubernetes can check when GWAN starts, when it is ready, whether it is alive, and how to inspect basic events and logs.
```

## Why this matters

A cloud-native service should not only start. It should be observable enough for an operator to answer simple questions:

```text
Is it starting?
Is it ready for traffic?
Is it still alive?
Why did it fail?
What do recent events and logs say?
```

## Probe model

| Probe | Meaning | GWAN usage |
|---|---|---|
| startupProbe | Gives the app time to start before liveness checks can kill it. | Protects slow startup. |
| readinessProbe | Decides whether the pod should receive traffic. | Uses `/health`. |
| livenessProbe | Decides whether Kubernetes should restart the container. | Uses `/health`. |

## Added scripts

```text
scripts/k8s/rollout_check.sh
scripts/k8s/health_readiness_check.sh
scripts/k8s/diagnostics.sh
```

## Typical local flow

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
```

In another terminal:

```bash
scripts/k8s/health_readiness_check.sh
```

If something fails:

```bash
scripts/k8s/diagnostics.sh
```

## Operator checklist

```text
kubectl -n hyean-gwan get pods
kubectl -n hyean-gwan get svc
kubectl -n hyean-gwan get events --sort-by=.lastTimestamp
kubectl -n hyean-gwan describe pods
kubectl -n hyean-gwan logs deployment/gwan-api
kubectl -n hyean-gwan logs deployment/postgres
```

## Completion criteria

- `gwan-api` has startupProbe, readinessProbe, and livenessProbe.
- `/health` is used as the first baseline health endpoint.
- rollout, health, and diagnostics scripts exist.
- diagnostics includes events, describe output, and logs.
