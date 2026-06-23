
## 27. Kubernetes production GHCR pull

The project now validates the production-style Kubernetes path.

Local/kind CI path:

```text
Build image in CI
→ kind load docker-image
→ k8s/overlays/local
```

Production-style path:

```text
Build and push image to GHCR
→ create Kubernetes ghcr-pull-secret
→ k8s/overlays/production
→ Kubernetes pulls the image from GHCR
```

New files:

```text
k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml
docs/27_GWAN_Kubernetes_Production_GHCR_Pull.md
tests/test_gwan_kubernetes_production_ghcr_pull.py
```

Manual production-like check:

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl -n hyean-gwan create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  --docker-email=YOUR_EMAIL
kubectl apply -k k8s/overlays/production
```
