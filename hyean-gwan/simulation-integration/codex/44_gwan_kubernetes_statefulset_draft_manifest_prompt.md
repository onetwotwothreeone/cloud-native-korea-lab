# Codex Prompt: 44_GWAN_Kubernetes_StatefulSet_Draft_Manifest

Create a draft StatefulSet manifest for GWAN PostgreSQL.

Requirements:

1. Do not apply the StatefulSet yet.
2. Keep current PostgreSQL Deployment active.
3. Create a draft Headless Service.
4. Create a draft StatefulSet.
5. Use serviceName: postgres-headless.
6. Use volumeClaimTemplates.
7. Keep SecurityContext, probes, resources, and Secret usage aligned with the current Deployment.
8. Do not include the draft in the base or local overlay kustomization yet.
9. Add static tests to verify the draft.
10. Add a script to render and inspect the draft.

Next step:

45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run
