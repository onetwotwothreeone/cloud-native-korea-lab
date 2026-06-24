# Codex Prompt: 54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check

Create a final pre-migration validation step for GWAN PostgreSQL StatefulSet migration.

Requirements:

- Do not execute real migration.
- Check current Deployment, Pod, PVC, Service, Secret, and ConfigMap.
- Check required migration safety documents.
- Confirm backup/restore, rollback, cutover checklist, approval template, manual approval record, and operator approval gate exist.
- Confirm active PostgreSQL StatefulSet does not exist yet.
- Keep FINAL_DECISION=NO_GO unless a human operator explicitly approves later.
- Next step should be 55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review.
