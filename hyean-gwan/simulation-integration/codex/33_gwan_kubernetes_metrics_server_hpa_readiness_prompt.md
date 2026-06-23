# Codex prompt: 33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness

Update the HYEAN/GWAN simulation-integration project with a Metrics Server and HPA readiness baseline.

Requirements:

1. Add `scripts/k8s/metrics_server_check.sh`.
   - It must validate the `gwan-api-hpa` object.
   - It must check `v1beta1.metrics.k8s.io`.
   - It must run `kubectl top nodes` and `kubectl top pods -n hyean-gwan` only when available.
   - It must not fail CI when metrics-server is absent in kind.

2. Add `scripts/k8s/install_metrics_server_local.sh` for local learning environments.

3. Add documentation:
   - `docs/33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness.md`

4. Update both workflow copies:
   - `.github/workflows/gwan-ci.yml`
   - `hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml`

5. Workflow requirements:
   - fixed variable names: `KIND_CLUSTER_NAME`, `KIND_PRODUCTION_CLUSTER_NAME`, `GWAN_KIND_IMAGE`, `GHCR_IMAGE_NAME`
   - documentation check for step 33
   - `Kubernetes metrics server readiness check`
   - `Production metrics server readiness check`

6. Add tests:
   - `tests/test_gwan_kubernetes_metrics_server_hpa_readiness.py`

Run:

```bash
python -m pytest -q
```
