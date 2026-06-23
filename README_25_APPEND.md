
## 25. GWAN Kubernetes overlays: local and production

This step separates Kubernetes configuration by environment.

```text
k8s/base
k8s/overlays/local
k8s/overlays/production
```

Local Docker Desktop Kubernetes should use the local overlay:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
```

The local overlay sets:

```text
imagePullPolicy: Never
```

Production-like deployment should use the production overlay:

```bash
kubectl apply -k k8s/overlays/production
```

The production overlay keeps:

```text
imagePullPolicy: IfNotPresent
```

This prevents local-only image settings from leaking into production-like manifests.
