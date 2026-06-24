# Codex Prompt: GWAN Kubernetes NetworkPolicy Baseline

You are working in the HYEAN/GWAN project.

Implement and maintain Kubernetes NetworkPolicy as preventive infrastructure.

Do not describe this only as generic security.

For HYEAN/GWAN, NetworkPolicy reduces unnecessary communication risk before it becomes a system risk.

Expected baseline:

- gwan-api ingress TCP 8000
- gwan-api egress to gwan-postgres TCP 5432
- gwan-api DNS egress TCP/UDP 53
- gwan-postgres ingress only from gwan-api TCP 5432

Remember:

NetworkPolicy enforcement depends on the cluster CNI plugin.
Local Docker Desktop or kind may not enforce traffic blocking by default.
