
## 28. Kubernetes production secrets and config

GWAN Kubernetes configuration now separates runtime settings into ConfigMap and Secret.

```text
ConfigMap = non-sensitive settings
Secret = sensitive settings
Deployment = references both
```

New file:

```text
k8s/base/gwan-api-configmap.yaml
```

ConfigMap values:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
HYEAN_MEMORY_JSONL_PATH
```

Secret value:

```text
POSTGRES_PASSWORD
```

The API Deployment now composes `DATABASE_URL` from environment variables instead of hardcoding the full connection string in one line.

Check:

```bash
kubectl kustomize k8s/overlays/local
kubectl kustomize k8s/overlays/production
python -m pytest -q
```
