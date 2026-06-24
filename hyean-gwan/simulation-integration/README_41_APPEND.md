## 41. GWAN Kubernetes StatefulSet Design Review

GWAN PostgreSQL persistence baseline was reviewed.

Current decision:

- Keep PostgreSQL as Deployment + PersistentVolumeClaim for the local baseline.
- Do not migrate to StatefulSet yet.
- Use this stage to confirm persistence, Secret, ConfigMap, RBAC, NetworkPolicy, SecurityContext, HPA, and PDB basics first.
- Plan StatefulSet migration later with backup and restore strategy.

Why this matters:

StatefulSet is better suited for stateful workloads, but it should not be added blindly.  
The project first records why the current architecture is acceptable and what must be prepared before migration.

Related files:

- `hyean-gwan/simulation-integration/docs/41_GWAN_Kubernetes_StatefulSet_Design_Review.md`
- `hyean-gwan/simulation-integration/codex/41_gwan_kubernetes_statefulset_design_review_prompt.md`
- `hyean-gwan/simulation-integration/scripts/k8s/statefulset_design_review_check.sh`
- `hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_statefulset_design_review.py`
