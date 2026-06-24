# Codex Prompt

Create GWAN Kubernetes StatefulSet Cutover Decision Gate.

Requirements:

- Add a decision gate document.
- Confirm that the decision remains NO_GO.
- Confirm that operator approval is required.
- Confirm that this step does not execute real StatefulSet migration.
- Confirm that PostgreSQL remains Deployment + PVC.
- Preserve HYEAN/GWAN prevention-first safety.

Do not execute real migration.
Do not create a live StatefulSet.
Do not delete the current PostgreSQL Deployment.
