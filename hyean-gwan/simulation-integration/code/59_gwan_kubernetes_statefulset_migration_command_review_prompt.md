# Codex Prompt

Create GWAN Kubernetes StatefulSet Migration Command Review.

Requirements:

- Add a command review document.
- Add a shell script that reviews command order.
- The script must not execute real migration.
- The script may run kubectl get, kubectl kustomize, and kubectl apply --dry-run=client.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Add COMMAND_REVIEW_STATUS=REVIEW_ONLY.
- Confirm PostgreSQL remains Deployment + PVC.
- Confirm no active PostgreSQL StatefulSet exists.
- Confirm real migration remains blocked.
- Set next step to 60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register.

Do not create a live StatefulSet.
Do not delete the current PostgreSQL Deployment.
Do not modify the existing PostgreSQL PVC.
Do not switch database traffic.
Do not run real migration.
