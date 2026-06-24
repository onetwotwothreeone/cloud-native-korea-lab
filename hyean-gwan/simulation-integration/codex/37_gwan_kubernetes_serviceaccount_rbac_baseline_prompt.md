# Codex Prompt: GWAN Kubernetes ServiceAccount RBAC Baseline

You are working in the HYEAN/GWAN project.

Add and maintain Kubernetes ServiceAccount and RBAC as preventive identity control.

Do not use the default ServiceAccount for GWAN workloads.

Baseline:

- gwan-api uses gwan-api-sa
- postgres uses gwan-postgres-sa
- service account token automount is false
- minimal roles have no Kubernetes API permissions

Explain this as least privilege and prevention-oriented infrastructure.
