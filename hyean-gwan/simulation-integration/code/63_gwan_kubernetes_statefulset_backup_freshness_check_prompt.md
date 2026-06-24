# Code Prompt: 63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check

Create a Kubernetes safety validation step that checks PostgreSQL backup freshness before StatefulSet migration.

Requirements:

- Do not execute real migration.
- Do not export secret values.
- Confirm PostgreSQL Deployment exists.
- Confirm PostgreSQL Pod is running.
- Confirm PostgreSQL PVC is Bound.
- Confirm PostgreSQL Secret exists.
- Confirm GWAN API ConfigMap exists.
- Confirm active PostgreSQL StatefulSet does not exist yet.
- Confirm latest backup file exists.
- Confirm backup age is within acceptable window.
- Keep FINAL_DECISION=NO_GO.
- Recommend next step: 64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check.
