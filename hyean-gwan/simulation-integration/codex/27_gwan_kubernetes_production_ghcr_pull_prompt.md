# Codex task: 27_GWAN_Kubernetes_Production_GHCR_Pull

## Goal

Add production-style Kubernetes validation where Kubernetes pulls the GWAN API image from GHCR.

## Required changes

- Add `imagePullSecrets` to production overlay.
- Update root `.github/workflows/gwan-ci.yml`.
- Create a kind cluster after GHCR push.
- Create `ghcr-pull-secret` in namespace `hyean-gwan`.
- Apply `k8s/overlays/production`.
- Verify `/health` and `/gwan/memory/db-status`.
- Add tests and docs.

## Required files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/k8s/overlays/production/kustomization.yaml
hyean-gwan/simulation-integration/k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml
hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_production_ghcr_pull.py
hyean-gwan/simulation-integration/docs/27_GWAN_Kubernetes_Production_GHCR_Pull.md
```

## Success command

```bash
python -m pytest -q
```
