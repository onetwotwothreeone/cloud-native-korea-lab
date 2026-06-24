from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_cutover_checklist_doc_exists() -> None:
    text = read("docs/48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md")

    assert "Cutover Checklist" in text
    assert "This step does not execute the real cutover" in text
    assert "Required Pre-Cutover Conditions" in text
    assert "No-Go Conditions" in text
    assert "Cutover Safety Rule" in text
    assert "manual GO or NO-GO decision" in text
    assert "49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate" in text


def test_cutover_checklist_prompt_exists() -> None:
    text = read("codex/48_gwan_kubernetes_statefulset_migration_cutover_checklist_prompt.md")

    assert "Codex Prompt" in text
    assert "Do not execute real cutover" in text
    assert "Do not apply StatefulSet" in text
    assert "Do not delete Deployment" in text
    assert "Do not delete PVC" in text
    assert "manual operator GO or NO-GO decision" in text


def test_cutover_checklist_script_exists() -> None:
    text = read("scripts/k8s/statefulset_migration_cutover_checklist.sh")

    assert "kubectl -n \"$NS\" get deployment postgres" in text
    assert "kubectl -n \"$NS\" get pods -l app.kubernetes.io/name=gwan-postgres" in text
    assert "kubectl -n \"$NS\" get pvc postgres-data" in text
    assert "kubectl -n \"$NS\" get service postgres" in text
    assert "kubectl -n \"$NS\" get secret gwan-postgres-secret" in text
    assert "kubectl -n \"$NS\" get configmap gwan-api-config" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "CUTOVER_DECISION_REQUIRED=true" in text
    assert "CURRENT_DECISION=NO-GO" in text


def test_cutover_checklist_script_is_non_destructive() -> None:
    text = read("scripts/k8s/statefulset_migration_cutover_checklist.sh")

    forbidden = [
        "kubectl delete",
        "kubectl scale",
        "kubectl apply",
        "pg_restore",
        "DROP DATABASE",
        "rm -rf",
    ]

    for keyword in forbidden:
        assert keyword not in text


def test_cutover_checklist_requires_previous_safety_assets() -> None:
    text = read("scripts/k8s/statefulset_migration_cutover_checklist.sh")

    assert "postgres_backup_restore_check.sh" in text
    assert "statefulset_migration_dry_run_check.sh" in text
    assert "statefulset_migration_runbook_check.sh" in text
    assert "statefulset_migration_rollback_dry_run_check.sh" in text
    assert "43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md" in text
    assert "45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md" in text
    assert "46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md" in text
    assert "47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md" in text


def test_cutover_checklist_does_not_activate_statefulset() -> None:
    overlay = read("k8s/overlays/local/kustomization.yaml")

    assert "postgres-statefulset-draft.yaml" not in overlay
    assert "postgres-headless-service-draft.yaml" not in overlay
    assert "k8s/drafts" not in overlay
