
## 29. Kubernetes health, readiness, and observability baseline

This step adds the first Kubernetes operations baseline for GWAN.

It adds:

```text
startupProbe
readinessProbe
livenessProbe
rollout check script
health/readiness check script
diagnostics script
```

Local check:

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
