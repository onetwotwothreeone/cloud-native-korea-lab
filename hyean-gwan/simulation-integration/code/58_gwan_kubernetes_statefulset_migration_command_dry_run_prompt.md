# Codex Prompt

Create GWAN Kubernetes StatefulSet Migration Command Dry Run.

Requirements:

- Add a dry-run command plan document.
- Add a shell script that checks current PostgreSQL state.
- The script may run kubectl dry-run commands.
- The script must not execute real migration.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Confirm PostgreSQL remains Deployment + PVC.
- Confirm no active PostgreSQL StatefulSet exists yet.
- Confirm next step is command review.

Do not create a live StatefulSet.
Do not delete the current PostgreSQL Deployment.
Do not modify the existing PostgreSQL PVC.
Do not switch database traffic.
