# Codex Prompt: GWAN Kubernetes StatefulSet Operator Approval Gate

Create a Kubernetes safety gate for PostgreSQL StatefulSet migration.

Requirements:

1. Do not execute real migration.
2. Read the manual approval record.
3. Keep migration blocked by default.
4. Allow migration only if:
   - CURRENT_DECISION=GO
   - APPROVED_BY_OPERATOR=true
   - FINAL_DECISION=GO
5. Confirm backup/restore and rollback dry-run documents exist.
6. Confirm StatefulSet draft exists.
7. Print a clear GO or NO_GO result.

Related documents:

- 51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template
- 52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record
- 53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate
