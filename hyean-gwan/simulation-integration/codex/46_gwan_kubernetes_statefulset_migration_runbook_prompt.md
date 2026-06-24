# Codex Prompt: 46_GWAN_Kubernetes_StatefulSet_Migration_Runbook

Create a safe migration runbook for moving GWAN PostgreSQL from Deployment + PVC to StatefulSet.

Requirements:

1. Do not execute the real migration.
2. Do not delete the PostgreSQL Deployment.
3. Do not apply the StatefulSet manifest.
4. Document current architecture.
5. Document target StatefulSet architecture.
6. Define migration gates.
7. Include backup/restore gate.
8. Include API scale-down and scale-up plan.
9. Include rollback plan.
10. Include stop conditions.
11. Add a read-only runbook check script.
12. Add tests for documentation, prompt, and script.

Next step:

47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run
