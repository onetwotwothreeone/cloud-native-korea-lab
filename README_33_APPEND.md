

---

## 33. GWAN Kubernetes Metrics Server and HPA Readiness

This step checks the metrics side of HPA.

Step 32 added the `gwan-api-hpa` object. Step 33 explains and checks whether the Kubernetes cluster can provide CPU and memory usage through the Metrics API.

### Why this matters

HPA needs metrics to make scaling decisions.

```text
Metrics Server
→ Metrics API
→ HPA
→ Deployment replica count
```

If Metrics Server is missing, HPA can still exist, but CPU values may show `<unknown>`.

### Check locally

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
scripts/k8s/metrics_server_check.sh
```

Optional local install:

```bash
scripts/k8s/install_metrics_server_local.sh
scripts/k8s/metrics_server_check.sh
```

### Test

```bash
python -m pytest -q
```
