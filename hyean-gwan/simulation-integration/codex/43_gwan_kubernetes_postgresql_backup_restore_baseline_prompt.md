# Codex Prompt: 43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline

Create a safe PostgreSQL backup and restore baseline for GWAN Kubernetes.

Current state:

- PostgreSQL runs as a Deployment.
- PostgreSQL uses a PVC named postgres-data.
- GWAN API connects through the postgres Service.
- StatefulSet migration is planned but not applied yet.

Requirements:

1. Use pg_dump for backup.
2. Store backup files in a local ignored directory.
3. Do not commit backup files to Git.
4. Restore into a temporary database.
5. Do not overwrite the main database.
6. Clean up the temporary restore database after verification.
7. Document why backup and restore must come before StatefulSet migration.

Next recommended step:

44_GWAN_Kubernetes_StatefulSet_Draft_Manifest
