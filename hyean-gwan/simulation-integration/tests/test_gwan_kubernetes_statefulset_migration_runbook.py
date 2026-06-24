from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_statefulset_migration_runbook_doc_exists() -> None:
    text = read("docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md")

    assert "StatefulSet Migration Runbook" in text
    assert "Migration Gates" in text
    assert "Backup/Restore Gate" in text
    assert "Rollback Plan" in text
    assert "Stop Conditions" in text
    assert "Never do database migration without a verified backup" in text
    assert "47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run" in text


def test_statefulset_migration_runbook_prompt_exists() -> None:
    text = read("codex/46_gwan_kubernetes_statefulset_migration_runbook_prompt.md")

    assert "Codex Prompt" in text
    assert "Do not execute the real migration" in text
    assert "Document current architecture" in text
    assert "Include rollback plan" in text
    assert "47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run" in text


def test_statefulset_migration_runbook_check_script_exists() -> None:
    text = read("scripts/k8s/statefulset_migration_runbook_check.sh")

    assert "kubectl -n \"$NS\" get deployment postgres" in text
    assert "kubectl -n \"$NS\" get pvc postgres-data" in text
    assert "kubectl -n \"$NS\" get service postgres" in text
    assert "kubectl -n \"$NS\" get secret gwan-postgres-secret" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "Rollback Plan" in text
    assert "Stop Conditions" in text


def test_statefulset_migration_runbook_check_script_is_read_only() -> None:
    text = read("scripts/k8s/statefulset_migration_runbook_check.sh")

    assert "kubectl apply" not in text
    assert "kubectl delete" not in text
    assert "kubectl scale" not in text
    assert "pg_restore" not in text
    assert "psql" not in text


def test_statefulset_still_not_added_to_local_overlay() -> None:
    text = read("k8s/overlays/local/kustomization.yaml")

    assert "postgres-statefulset-draft.yaml" not in text
    assert "postgres-headless-service-draft.yaml" not in text
    assert "k8s/drafts" not in text


def test_previous_safety_assets_exist() -> None:
    assert (ROOT / "scripts/k8s/postgres_backup_restore_check.sh").exists()
    assert (ROOT / "scripts/k8s/statefulset_migration_dry_run_check.sh").exists()
    assert (ROOT / "docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md").exists()
