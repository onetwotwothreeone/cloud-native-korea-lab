# Codex task: 28_GWAN_Kubernetes_Production_Secrets_And_Config

## Goal

Separate non-sensitive Kubernetes runtime configuration into a ConfigMap and keep sensitive values in Secret.

## Add

```text
k8s/base/gwan-api-configmap.yaml
```

## Update

```text
k8s/base/kustomization.yaml
k8s/base/gwan-api-deployment.yaml
```

## Rules

- ConfigMap should include `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, and `HYEAN_MEMORY_JSONL_PATH`.
- Secret should keep `POSTGRES_PASSWORD`.
- Deployment should use `configMapKeyRef` and `secretKeyRef`.
- `DATABASE_URL` should be composed from environment variables.

## Success command

```bash
python -m pytest -q
kubectl kustomize k8s/overlays/local
kubectl kustomize k8s/overlays/production
```
