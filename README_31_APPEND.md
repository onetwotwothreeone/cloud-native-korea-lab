

## 31. GWAN Kubernetes Namespace ResourceQuota and LimitRange

This step adds namespace-level resource boundaries for the HYEAN/GWAN Kubernetes environment.

Added files:

```text
k8s/base/resourcequota.yaml
k8s/base/limitrange.yaml
scripts/k8s/namespace_policy_check.sh
docs/31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange.md
```

Local check:

```bash
cd hyean-gwan/simulation-integration

docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/namespace_policy_check.sh
```

Simple meaning:

```text
ResourceQuota = total resource fence for the namespace
LimitRange = default resource rule for containers
```
