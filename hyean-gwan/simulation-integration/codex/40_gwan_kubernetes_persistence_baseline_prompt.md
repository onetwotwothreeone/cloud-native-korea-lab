# Codex Prompt: GWAN Kubernetes Persistence Baseline

Implement and verify Kubernetes persistence for the GWAN PostgreSQL database.

Requirements:

1. Add a PostgreSQL PersistentVolumeClaim.
2. Name the PVC postgres-data.
3. Keep the namespace as hyean-gwan.
4. Change PostgreSQL deployment storage from emptyDir to persistentVolumeClaim.
5. Keep the PostgreSQL mount path as /var/lib/postgresql/data.
6. Add a script that checks the PVC and PostgreSQL deployment volume configuration.
7. Add tests that verify:
   - postgres-pvc.yaml exists.
   - PVC kind is PersistentVolumeClaim.
   - PVC name is postgres-data.
   - PVC requests 1Gi.
   - postgres-deployment.yaml uses persistentVolumeClaim.
   - claimName is postgres-data.
8. Keep this aligned with the next step:
   41_GWAN_Kubernetes_StatefulSet_Design_Review
