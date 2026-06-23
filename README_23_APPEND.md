
## 23. GWAN Kubernetes manifests

This step adds the first Kubernetes manifests for the GWAN simulation integration prototype.

The manifests are under:

```text
k8s/base/
```

They define:

```text
Namespace
PostgreSQL Secret
PostgreSQL Service
PostgreSQL Deployment
GWAN API Service
GWAN API Deployment
Kustomization entrypoint
```

Local check with kubectl and kustomize-compatible rendering:

```bash
kubectl kustomize k8s/base
```

Apply to a local Kubernetes cluster, such as Docker Desktop Kubernetes, only after confirming the GHCR image is available:

```bash
kubectl apply -k k8s/base
kubectl -n hyean-gwan get pods
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
curl http://127.0.0.1:8000/health
```

This step begins the Kubernetes path after Docker image build, Docker Compose CI, and GHCR image push.
