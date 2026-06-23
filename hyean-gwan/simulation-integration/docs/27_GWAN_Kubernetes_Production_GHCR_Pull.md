# 27_GWAN_Kubernetes_Production_GHCR_Pull

## Purpose

This step verifies the production-style Kubernetes path.

Previous Kubernetes CI used the local overlay:

```text
Build image in CI
→ kind load docker-image
→ imagePullPolicy: Never
→ Kubernetes local overlay
```

This step adds the production-style path:

```text
Build and push image to GHCR
→ create Kubernetes imagePullSecret
→ apply production overlay
→ Kubernetes pulls image from GHCR
→ /health and /db-status checks pass
```

## Why this matters

The local overlay proves that the manifests work when an image is already available inside the cluster.

The production overlay proves a more realistic deployment path: Kubernetes pulls the GWAN API image from a registry.

## New / updated files

```text
.github/workflows/gwan-ci.yml
k8s/overlays/production/kustomization.yaml
k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml
tests/test_gwan_kubernetes_production_ghcr_pull.py
docs/27_GWAN_Kubernetes_Production_GHCR_Pull.md
codex/27_gwan_kubernetes_production_ghcr_pull_prompt.md
```

## Production overlay behavior

The production overlay keeps:

```text
imagePullPolicy: IfNotPresent
```

and adds:

```text
imagePullSecrets:
  - name: ghcr-pull-secret
```

## GitHub Actions behavior

The workflow now performs these production-style checks on `main` push:

```text
Log in to GHCR
Build and push image to GHCR
Create a fresh kind cluster
Create ghcr-pull-secret in the hyean-gwan namespace
Apply k8s/overlays/production
Wait for postgres and gwan-api rollout
Check /health
Check /gwan/memory/db-status
Dump diagnostics on failure
Delete production kind cluster
```

## Manual local production-like check

If the GHCR package is private, create a pull secret first:

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl -n hyean-gwan create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_TOKEN \
  --docker-email=YOUR_EMAIL
```

Then apply the production overlay:

```bash
kubectl apply -k k8s/overlays/production
kubectl -n hyean-gwan rollout status deployment/postgres --timeout=180s
kubectl -n hyean-gwan rollout status deployment/gwan-api --timeout=180s
```

## Completion criteria

- Production overlay includes `imagePullSecrets`.
- GitHub Actions creates `ghcr-pull-secret` before applying production overlay.
- Production kind cluster pulls image from GHCR instead of using `kind load docker-image`.
- `/health` and `/gwan/memory/db-status` pass through port-forward.
