from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rollback_dry_run_doc_exists() -> None:
    text = read("docs/47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md")

    assert "Rollback Dry Run" in text
    assert "This step does not execute the real rollback" in text
    assert "Current Safe Baseline" in text
    assert "Future Real Rollback Flow" in text
    assert "Stop Conditions" in text
    assert "A rollback plan is not optional" in text
    assert "48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist" in text


def test_rollback_dry_run_prompt_exists() -> None:
    text = read("codex/47_gwan_kubernetes_statefulset_migration_rollback_dry_run_prompt.md")

    assert "Codex Prompt" in text
    assert "Do not execute real rollback" in text
    assert "Do not delete StatefulSet" in text
    assert "Do not scale workloads" in text
    assert "Do not restore into the main database" in text
    assert "48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist" in text


def test_rollback_dry_run_script_exists() -> None:
    text = read("scripts/k8s/statefulset_migration_rollback_dry_run_check.sh")

    assert "kubectl -n \"$NS\" get deployment postgres" in text
    assert "kubectl -n \"$NS\" get pvc postgres-data" in text
    assert "kubectl -n \"$NS\" get service postgres" in text
    assert "kubectl -n \"$NS\" get secret gwan-postgres-secret" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "real rollback was NOT executed" in text
    assert "real migration is still NOT executed" in text


def test_rollback_dry_run_script_is_non_destructive() -> None:
    text = read("scripts/k8s/statefulset_migration_rollback_dry_run_check.sh")

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


def test_previous_migration_safety_assets_exist() -> None:
    assert (ROOT / "docs/46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md").exists()
    assert (ROOT / "scripts/k8s/postgres_backup_restore_check.sh").exists()
    assert (ROOT / "scripts/k8s/statefulset_migration_runbook_check.sh").exists()
    assert (ROOT / "scripts/k8s/statefulset_migration_dry_run_check.sh").exists()


def test_statefulset_still_not_added_to_local_overlay() -> None:
    text = read("k8s/overlays/local/kustomization.yaml")

    assert "postgres-statefulset-draft.yaml" not in text
    assert "postgres-headless-service-draft.yaml" not in text
    assert "k8s/drafts" not in text
