# 68 GWAN Kubernetes StatefulSet Final Preflight Check Prompt

Create a final preflight check before PostgreSQL Deployment to StatefulSet migration.

Requirements:

- Keep CURRENT_DECISION=NO_GO
- Keep APPROVED_BY_OPERATOR=false
- Keep FINAL_DECISION=NO_GO
- Keep OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED
- Keep READINESS_STATUS=SUMMARY_ONLY
- Keep BACKUP_FRESHNESS_STATUS=PASSED
- Keep DATA_INTEGRITY_STATUS=PASSED
- Keep FINAL_APPROVAL_GATE_STATUS=BLOCKED
- Set PREFLIGHT_STATUS=PASSED_BUT_BLOCKED
- Set MIGRATION_EXECUTION_ALLOWED=false
- Keep REAL_MIGRATION_EXECUTED=false
- Keep SECRET_VALUES_EXPORTED=false
- Do not execute real migration
- Do not export Secret values
- Do not create active PostgreSQL StatefulSet
- Check previous readiness summary
- Check final approval gate
- Next step: 69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report
