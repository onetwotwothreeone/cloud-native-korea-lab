# Codex Prompt: 31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange

Implement namespace-level Kubernetes resource policies for the HYEAN/GWAN simulation integration project.

Tasks:

1. Add `k8s/base/resourcequota.yaml` for the `hyean-gwan` namespace.
2. Add `k8s/base/limitrange.yaml` for default container resource rules.
3. Update `k8s/base/kustomization.yaml` to include both files.
4. Add `scripts/k8s/namespace_policy_check.sh` to inspect ResourceQuota and LimitRange.
5. Update `.github/workflows/gwan-ci.yml` and nested workflow copy to check docs and run the namespace policy check after Kubernetes apply.
6. Add docs and tests.

Keep workflow variable naming consistent:

```text
KIND_CLUSTER_NAME
KIND_PRODUCTION_CLUSTER_NAME
GWAN_KIND_IMAGE
GHCR_IMAGE_NAME
```
