# Codex Prompt

Create GWAN Kubernetes StatefulSet Migration Risk Register.

Requirements:

- Add a risk register document.
- List major migration risks.
- Include impact, prevention, and recovery.
- Keep CURRENT_DECISION=NO_GO.
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Add RISK_REGISTER_STATUS=REVIEW_ONLY.
- Confirm PostgreSQL remains Deployment + PVC.
- Confirm no active PostgreSQL StatefulSet exists.
- Confirm real migration remains blocked.
- Set next step to 61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.

Do not create a live StatefulSet.
Do not delete the current PostgreSQL Deployment.
Do not modify the existing PostgreSQL PVC.
Do not switch database traffic.
Do not run real migration.
