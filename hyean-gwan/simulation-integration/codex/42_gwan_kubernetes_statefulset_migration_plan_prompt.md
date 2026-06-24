# Codex Prompt: 42_GWAN_Kubernetes_StatefulSet_Migration_Plan

Create a safe migration plan for GWAN PostgreSQL.

Current state:

- PostgreSQL runs as a Deployment.
- PostgreSQL uses a PVC named postgres-data.
- GWAN API connects through the postgres ClusterIP Service.
- Existing baselines include ConfigMap, Secret, RBAC, SecurityContext, NetworkPolicy, ResourceQuota, LimitRange, PDB, and HPA.

Do not convert PostgreSQL to StatefulSet yet.

The plan must explain:

1. Why StatefulSet may be needed later.
2. Why migration should not be rushed.
3. What must be checked before migration.
4. Why backup and restore must come before StatefulSet conversion.
5. What rollback strategy should exist.
6. Why local Kubernetes and production database strategy may differ.

Next recommended step:

43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline
