
## 24. GWAN Kubernetes local run

This step adds a local Kubernetes runbook and helper scripts for the GWAN API and PostgreSQL manifests.

Manual check:

```bash
cd hyean-gwan/simulation-integration
kubectl kustomize k8s/base
kubectl apply -k k8s/base
kubectl -n hyean-gwan rollout status deployment/postgres --timeout=180s
kubectl -n hyean-gwan rollout status deployment/gwan-api --timeout=180s
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
```

In another terminal:

```bash
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
```

Scripted check:

```bash
scripts/k8s/apply_local.sh
scripts/k8s/status.sh
scripts/k8s/port_forward_health_check.sh
scripts/k8s/cleanup_local.sh
```
