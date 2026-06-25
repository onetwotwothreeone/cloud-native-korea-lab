# Codex Prompt: GWAN Kubernetes StatefulSet Operator Final Approval Record

Create a safety-first operator approval record step for PostgreSQL Deployment to StatefulSet migration.

Requirements:

- Do not execute real migration.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Keep OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED.
- Keep REAL_MIGRATION_EXECUTED=false.
- Keep SECRET_VALUES_EXPORTED=false.
- Verify previous safety documents exist.
- Verify Kubernetes PostgreSQL Deployment, Pod, PVC, Service, Secret metadata, and GWAN ConfigMap.
- Verify no active PostgreSQL StatefulSet exists yet.
- Run the previous pre-migration readiness summary safely.
- Create a local non-secret approval record artifact.
- Prepare the next approval gate step.
