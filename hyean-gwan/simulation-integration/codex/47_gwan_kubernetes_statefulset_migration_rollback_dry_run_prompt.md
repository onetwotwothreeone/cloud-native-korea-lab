# Codex Prompt: 47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run

Create a safe rollback dry-run baseline for GWAN PostgreSQL StatefulSet migration.

Requirements:

1. Do not execute real rollback.
2. Do not delete StatefulSet.
3. Do not scale workloads.
4. Do not restore into the main database.
5. Check current PostgreSQL Deployment.
6. Check current PVC.
7. Check current Service.
8. Check current Secret.
9. Check StatefulSet draft rendering.
10. Check backup/restore baseline exists.
11. Document future rollback flow.
12. Add tests that prevent destructive commands.

Next step:

48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist
