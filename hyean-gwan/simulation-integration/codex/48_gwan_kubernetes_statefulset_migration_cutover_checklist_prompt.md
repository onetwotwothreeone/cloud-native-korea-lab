# Codex Prompt: 48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist

Create a final pre-cutover checklist for GWAN PostgreSQL StatefulSet migration.

Requirements:

1. Do not execute real cutover.
2. Do not apply StatefulSet to the local overlay.
3. Do not delete Deployment.
4. Do not delete PVC.
5. Do not restore into the main database.
6. Verify current PostgreSQL Deployment.
7. Verify current PostgreSQL Pod.
8. Verify current PVC.
9. Verify current Service.
10. Verify current Secret.
11. Verify ConfigMap.
12. Verify backup/restore baseline exists.
13. Verify rollback dry run exists.
14. Verify StatefulSet draft renders.
15. Require manual operator GO or NO-GO decision.

Next step:

49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate
