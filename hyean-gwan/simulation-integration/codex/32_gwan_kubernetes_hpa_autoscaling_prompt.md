# Codex Prompt: 32_GWAN_Kubernetes_HPA_Autoscaling_Baseline

Apply the GWAN Kubernetes HPA autoscaling baseline.

Requirements:

1. Add `k8s/base/gwan-api-hpa.yaml` using `autoscaling/v2`.
2. Target `Deployment/gwan-api`.
3. Use `minReplicas: 1`, `maxReplicas: 3`, and CPU average utilization `70`.
4. Include the HPA manifest in `k8s/base/kustomization.yaml`.
5. Add `scripts/k8s/hpa_check.sh` to inspect the HPA.
6. Update GWAN CI workflow to check the new documentation and run the HPA check after Kubernetes overlay application.
7. Preserve fixed workflow variable names:
   - `KIND_CLUSTER_NAME`
   - `KIND_PRODUCTION_CLUSTER_NAME`
   - `GWAN_KIND_IMAGE`
   - `GHCR_IMAGE_NAME`
8. Add tests that validate HPA manifest structure, kustomization inclusion, workflow coverage, and documentation.
