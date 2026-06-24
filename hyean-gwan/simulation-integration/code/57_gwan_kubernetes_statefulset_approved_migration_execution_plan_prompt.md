# Codex Prompt

Create GWAN Kubernetes StatefulSet Approved Migration Execution Plan.

Requirements:

- Add an execution plan document.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Confirm this step does not execute real migration.
- Confirm PostgreSQL remains Deployment + PVC.
- Define safe execution phases.
- Preserve HYEAN/GWAN prevention-first safety principle.

Do not create a live StatefulSet.
Do not delete the current PostgreSQL Deployment.
Do not modify the existing PostgreSQL PVC.
Do not switch database traffic.
