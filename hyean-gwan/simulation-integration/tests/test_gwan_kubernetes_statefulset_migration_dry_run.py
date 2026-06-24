from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_statefulset_migration_dry_run_script_exists() -> None:
    path = ROOT / "scripts/k8s/statefulset_migration_dry_run_check.sh"
    assert path.exists()

    text = path.read_text(encoding="utf-8")
    assert "kubectl -n \"$NS\" get deployment postgres" in text
    assert "kubectl -n \"$NS\" get pvc postgres-data" in text
    assert "kubectl -n \"$NS\" get service postgres" in text
    assert "kubectl -n \"$NS\" get secret gwan-postgres-secret" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "statefulset postgres" in text


def test_statefulset_migration_dry_run_does_not_apply_statefulset() -> None:
    text = read("scripts/k8s/statefulset_migration_dry_run_check.sh")

    assert "kubectl apply -k k8s/drafts" not in text
    assert "kubectl delete deployment postgres" not in text
    assert "kubectl -n \"$NS\" delete deployment postgres" not in text
    assert "kubectl -n \"$NS\" scale deployment postgres --replicas=0" not in text


def test_statefulset_migration_dry_run_doc_exists() -> None:
    text = read("docs/45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md")

    assert "StatefulSet Migration Dry Run" in text
    assert "This step does not perform the actual migration" in text
    assert "backup/restore baseline" in text
    assert "StatefulSet draft" in text
    assert "46_GWAN_Kubernetes_StatefulSet_Migration_Runbook" in text


def test_statefulset_migration_dry_run_prompt_exists() -> None:
    text = read("codex/45_gwan_kubernetes_statefulset_migration_dry_run_prompt.md")

    assert "Codex Prompt" in text
    assert "Do not perform actual migration" in text
    assert "Verify current Deployment" in text
    assert "Verify StatefulSet draft render" in text
    assert "46_GWAN_Kubernetes_StatefulSet_Migration_Runbook" in text


def test_statefulset_draft_still_not_active_in_local_overlay() -> None:
    local = read("k8s/overlays/local/kustomization.yaml")

    assert "k8s/drafts" not in local
    assert "postgres-statefulset-draft.yaml" not in local
    assert "postgres-headless-service-draft.yaml" not in local


def test_previous_backup_restore_baseline_exists() -> None:
    assert (ROOT / "scripts/k8s/postgres_backup_restore_check.sh").exists()
