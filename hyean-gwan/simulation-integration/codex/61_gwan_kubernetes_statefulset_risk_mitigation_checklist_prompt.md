# Codex Prompt: 61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist

Create a risk mitigation checklist for GWAN PostgreSQL StatefulSet migration.

Requirements:

- Do not execute real migration.
- Keep FINAL_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Verify that previous safety documents exist.
- Verify PVC, Deployment, Service, Secret, ConfigMap, and current non-StatefulSet status.
- Confirm that migration risks have prevention, verification, and recovery actions.
- Next recommended step must be 62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot.

This step is a checklist step, not a migration step.
