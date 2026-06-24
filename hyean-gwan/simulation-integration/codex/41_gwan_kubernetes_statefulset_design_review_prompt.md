# Codex Prompt: 41_GWAN_Kubernetes_StatefulSet_Design_Review

Review the current GWAN Kubernetes PostgreSQL persistence design.

Current state:

- PostgreSQL is deployed as a Deployment.
- PostgreSQL uses a PersistentVolumeClaim named postgres-data.
- GWAN API connects to PostgreSQL through the postgres ClusterIP Service.
- The system already includes Secret, ConfigMap, ResourceQuota, LimitRange, HPA, PDB, NetworkPolicy, RBAC, and SecurityContext baselines.

Do not convert PostgreSQL to StatefulSet yet.

Create a design review explaining:

1. Why Deployment + PVC is acceptable for the current local baseline.
2. Why StatefulSet is usually more appropriate for stateful workloads.
3. What risks must be handled before migration.
4. What the next migration plan should include.
5. Why this decision matters for production architecture.

Next recommended step:

42_GWAN_Kubernetes_StatefulSet_Migration_Plan
