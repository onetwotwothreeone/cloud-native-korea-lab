# Codex Prompt: 62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot

Create a pre-execution safety snapshot step for GWAN PostgreSQL StatefulSet migration.

Requirements:

- Do not execute real migration.
- Do not export secret values.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Keep REAL_MIGRATION_EXECUTED=false.
- Capture current safe baseline before migration.
- Snapshot should include Deployment, Pod, PVC, Service, Secret metadata, ConfigMap, rollout state, and safety documents.
- Next recommended step must be 63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check.
