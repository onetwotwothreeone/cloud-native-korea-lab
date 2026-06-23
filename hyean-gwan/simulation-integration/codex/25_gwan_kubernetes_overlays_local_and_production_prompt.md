# Codex task: 25_GWAN_Kubernetes_Overlays_Local_And_Production

## Goal

Separate Kubernetes manifests into base, local overlay, and production overlay.

## Why

Local Docker Desktop Kubernetes can use a locally built image with `imagePullPolicy: Never`. Production-like deployment should keep GHCR image pull behavior with `imagePullPolicy: IfNotPresent`.

## Required files

```text
k8s/overlays/local/kustomization.yaml
k8s/overlays/local/gwan-api-image-pull-policy-patch.yaml
k8s/overlays/production/kustomization.yaml
k8s/overlays/production/gwan-api-image-pull-policy-patch.yaml
docs/25_GWAN_Kubernetes_Overlays_Local_And_Production.md
tests/test_gwan_kubernetes_overlays.py
```

## Required behavior

- Restore `k8s/base/gwan-api-deployment.yaml` to `imagePullPolicy: IfNotPresent`.
- Local overlay must patch `gwan-api` to `imagePullPolicy: Never`.
- Production overlay must patch `gwan-api` to `imagePullPolicy: IfNotPresent`.
- Local scripts should use `k8s/overlays/local`.

## Success command

```bash
python -m pytest -q
```
