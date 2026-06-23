# Codex task: 30_GWAN_Kubernetes_Resource_Requests_And_Limits

## Goal

Add baseline Kubernetes CPU and memory requests/limits to GWAN Kubernetes manifests.

## Required changes

- Add `resources.requests` and `resources.limits` to `gwan-api` deployment.
- Add `resources.requests` and `resources.limits` to `postgres` deployment.
- Add a resource inspection script.
- Add documentation and tests.
- Keep workflow variable naming consistent:
  - `KIND_CLUSTER_NAME`
  - `KIND_PRODUCTION_CLUSTER_NAME`
  - `GWAN_KIND_IMAGE`
  - `GHCR_IMAGE_NAME`

## Target resource baseline

### gwan-api

```yaml
requests:
  cpu: 100m
  memory: 128Mi
limits:
  cpu: 500m
  memory: 512Mi
```

### postgres

```yaml
requests:
  cpu: 100m
  memory: 256Mi
limits:
  cpu: 500m
  memory: 512Mi
```

## Success command

```bash
python -m pytest -q
```
