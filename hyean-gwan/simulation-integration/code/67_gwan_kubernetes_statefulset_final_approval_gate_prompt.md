# 67 GWAN Kubernetes StatefulSet Final Approval Gate Prompt

Create a final approval gate for the PostgreSQL Deployment to StatefulSet migration.

Requirements:

- Keep CURRENT_DECISION=NO_GO
- Keep APPROVED_BY_OPERATOR=false
- Keep FINAL_DECISION=NO_GO
- Keep OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
- Keep READINESS_STATUS=SUMMARY_ONLY
- Keep BACKUP_FRESHNESS_STATUS=PASSED
- Keep DATA_INTEGRITY_STATUS=PASSED
- Keep REAL_MIGRATION_EXECUTED=false
- Keep SECRET_VALUES_EXPORTED=false
- Keep FINAL_APPROVAL_GATE_STATUS=BLOCKED
- Do not execute real migration
- Do not export Secret values
- Do not create active PostgreSQL StatefulSet
- Check Kubernetes current state
- Check previous readiness summary
- Next step: 68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check
