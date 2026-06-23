# 24_GWAN_Kubernetes_Local_Run

## Purpose

This step turns the Kubernetes manifest files from step 23 into an actual local Kubernetes run procedure.

Step 23 created the deployment description. Step 24 verifies that a beginner can run it on local Docker Desktop Kubernetes.

After step 25, local execution should use the local overlay:

```text
k8s/overlays/local
```

The local overlay uses the Docker image built on the Mac and sets:

```text
imagePullPolicy: Never
```

This avoids GHCR private-image pull errors during local practice.

## Manual local run

From the simulation integration directory:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
```

Build the local Docker image with the same name used in the Kubernetes manifest:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
```

Render the local overlay first:

```bash
kubectl kustomize k8s/overlays/local
```

Apply the local overlay:

```bash
kubectl apply -k k8s/overlays/local
```

Wait for deployments:

```bash
kubectl -n hyean-gwan rollout status deployment/postgres --timeout=180s
kubectl -n hyean-gwan rollout status deployment/gwan-api --timeout=180s
```

Check status:

```bash
kubectl -n hyean-gwan get pods
kubectl -n hyean-gwan get svc
```

Port-forward the API service:

```bash
kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
```

In another terminal:

```bash
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
```

Expected health response:

```json
{"status":"ok"}
```

## Scripted local run

Apply and wait:

```bash
scripts/k8s/apply_local.sh
```

Check status:

```bash
scripts/k8s/status.sh
```

Run port-forward and API checks:

```bash
scripts/k8s/port_forward_health_check.sh
```

Clean up:

```bash
scripts/k8s/cleanup_local.sh
```

## Common troubleshooting

### Kubernetes is not enabled

If `kubectl apply` shows connection refused to `127.0.0.1:6443`, enable Kubernetes in Docker Desktop first.

### gwan-api shows ErrImagePull

For local Docker Desktop Kubernetes, use the local overlay:

```bash
kubectl apply -k k8s/overlays/local
```

The local overlay sets `imagePullPolicy: Never`, so Kubernetes uses the local Docker image instead of pulling from GHCR.

### Production should not use imagePullPolicy: Never

Production-like deployment should use:

```bash
kubectl apply -k k8s/overlays/production
```

That overlay keeps GHCR image pull behavior with `imagePullPolicy: IfNotPresent`.

## Completion criteria

- `kubectl kustomize k8s/overlays/local` renders YAML.
- `kubectl apply -k k8s/overlays/local` succeeds.
- `postgres` deployment becomes available.
- `gwan-api` deployment becomes available.
- `kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000` works.
- `/health` returns `{"status":"ok"}`.
