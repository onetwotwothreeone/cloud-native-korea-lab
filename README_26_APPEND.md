
## 26. Kubernetes CI with kind

GWAN now validates Kubernetes manifests inside GitHub Actions by creating a temporary kind cluster.

The workflow now checks:

```text
Python tests
Docker build
Docker Compose API + PostgreSQL integration
kind cluster creation
Docker image loaded into kind
kubectl apply -k k8s/overlays/local
PostgreSQL rollout
GWAN API rollout
/health check through port-forward
/gwan/memory/db-status check through port-forward
```

This means Kubernetes validation no longer depends only on the local Docker Desktop cluster.
GitHub Actions can now create a disposable Kubernetes cluster and verify that the GWAN manifests work.
