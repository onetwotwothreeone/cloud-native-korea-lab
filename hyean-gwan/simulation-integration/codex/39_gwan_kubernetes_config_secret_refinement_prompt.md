# Codex Prompt: 39_GWAN_Kubernetes_Config_And_Secret_Refinement

Refine GWAN Kubernetes configuration and secrets.

Requirements:

1. Keep non-sensitive runtime configuration in ConfigMap.
2. Keep database credentials in Secret.
3. Ensure gwan-api Deployment consumes ConfigMap and Secret values.
4. Ensure postgres Deployment consumes Secret values.
5. Do not hardcode raw passwords in Deployment or ConfigMap.
6. Add a script that checks the expected ConfigMap and Secret separation.
7. Add pytest coverage for the Kubernetes YAML files.
8. Keep compatibility with the next step: 40_GWAN_Kubernetes_PersistentVolume_Baseline.
