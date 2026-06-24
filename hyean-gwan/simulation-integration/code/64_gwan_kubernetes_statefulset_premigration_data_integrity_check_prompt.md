# Codex Prompt

Create a safe pre-migration data integrity check for GWAN PostgreSQL.

Requirements:

- Do not execute real migration.
- Do not apply StatefulSet manifest.
- Do not delete PostgreSQL Deployment.
- Do not overwrite the database.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Keep DATA_INTEGRITY_STATUS=REVIEW_ONLY.
- Keep READ_ONLY_CHECK=true.
- Keep REAL_MIGRATION_EXECUTED=false.
- Keep SECRET_VALUES_EXPORTED=false.
- Check PostgreSQL Deployment, Pod, PVC, Service, Secret metadata, and GWAN API ConfigMap.
- Check latest backup file exists.
- Use pg_isready.
- Use SELECT current_database().
- Use information_schema.tables.
- Generate a local read-only integrity report.
- Make the script safe for repeated execution.
