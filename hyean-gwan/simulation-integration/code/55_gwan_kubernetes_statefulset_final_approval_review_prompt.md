# Codex Prompt

Create GWAN Kubernetes StatefulSet Final Approval Review.

Requirements:

- Add a final approval review document.
- Add a Kubernetes check script.
- Add pytest coverage.
- Confirm that this step does not execute real migration.
- Confirm that FINAL_DECISION remains NO_GO.
- Confirm that operator approval is still required.
- Confirm that HYEAN/GWAN prevention-first safety is preserved.

Do not execute real migration.
Do not create a live PostgreSQL StatefulSet.
Do not delete the current PostgreSQL Deployment.
