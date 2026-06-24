# Code Prompt: 65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary

Create a Kubernetes safety summary script for PostgreSQL Deployment to StatefulSet migration.

Required behavior:

- Do not execute real migration.
- Keep CURRENT_DECISION=NO_GO.
- Keep FINAL_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep REAL_MIGRATION_EXECUTED=false.
- Keep SECRET_VALUES_EXPORTED=false.
- Summarize backup freshness.
- Summarize read-only DB integrity.
- Confirm active PostgreSQL StatefulSet does not exist yet.
- Recommend the next step: 66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record.
