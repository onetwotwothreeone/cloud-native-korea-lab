# Codex task: 23_GWAN_Kubernetes_Manifests

## Goal

Add first Kubernetes manifests for GWAN simulation integration.

## Required files

```text
k8s/base/namespace.yaml
k8s/base/postgres-secret.yaml
k8s/base/postgres-service.yaml
k8s/base/postgres-deployment.yaml
k8s/base/gwan-api-service.yaml
k8s/base/gwan-api-deployment.yaml
k8s/base/kustomization.yaml
tests/test_gwan_kubernetes_manifests.py
docs/23_GWAN_Kubernetes_Manifests.md
```

## Requirements

- Use namespace `hyean-gwan`.
- Run PostgreSQL with `postgres:16-alpine`.
- Run GWAN API image from `ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest`.
- Use Kubernetes Service DNS `postgres:5432` inside `DATABASE_URL`.
- Include readiness and liveness probes.
- Include kustomization entrypoint.
- Add tests that check the manifest files and critical strings.

## Success command

```bash
python -m pytest -q
```
