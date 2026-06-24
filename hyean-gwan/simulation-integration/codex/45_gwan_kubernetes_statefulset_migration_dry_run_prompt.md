# Codex Prompt: 45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run

Create a safe dry-run process before migrating GWAN PostgreSQL from Deployment to StatefulSet.

Requirements:

1. Do not perform actual migration.
2. Do not delete the PostgreSQL Deployment.
3. Do not apply the StatefulSet draft.
4. Verify current Deployment, Pod, PVC, Service, and Secret.
5. Verify StatefulSet draft render.
6. Verify backup/restore baseline script exists.
7. Confirm that no active postgres StatefulSet exists yet.
8. Create a dry-run check script.
9. Create documentation explaining the migration decision.
10. Add tests for the dry-run script, documentation, and prompt.

Next step:

46_GWAN_Kubernetes_StatefulSet_Migration_Runbook
