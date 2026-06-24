from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_statefulset_migration_plan_doc_exists() -> None:
    doc = ROOT / "docs/42_GWAN_Kubernetes_StatefulSet_Migration_Plan.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "StatefulSet Migration Plan" in text
    assert "Do not migrate yet" in text
    assert "backup" in text.lower()
    assert "restore" in text.lower()
    assert "rollback" in text.lower()
    assert "43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline" in text


def test_statefulset_migration_codex_prompt_exists() -> None:
    prompt = ROOT / "codex/42_gwan_kubernetes_statefulset_migration_plan_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Do not convert PostgreSQL to StatefulSet yet" in text
    assert "Backup and restore" in text or "backup and restore" in text
    assert "43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline" in text


def test_current_postgres_baseline_still_uses_deployment_and_pvc() -> None:
    deployment = (ROOT / "k8s/base/postgres-deployment.yaml").read_text(encoding="utf-8")
    pvc = (ROOT / "k8s/base/postgres-pvc.yaml").read_text(encoding="utf-8")

    assert "kind: Deployment" in deployment
    assert "name: postgres" in deployment
    assert "persistentVolumeClaim" in deployment
    assert "claimName: postgres-data" in deployment

    assert "kind: PersistentVolumeClaim" in pvc
    assert "name: postgres-data" in pvc


def test_migration_plan_check_script_exists() -> None:
    script = ROOT / "scripts/k8s/statefulset_migration_plan_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get statefulset" in text
    assert "Backup and restore baseline" in text or "backup and restore baseline" in text


def test_no_statefulset_manifest_is_applied_yet() -> None:
    k8s_base = ROOT / "k8s/base"
    statefulset_files = list(k8s_base.glob("*statefulset*.yaml"))
    assert statefulset_files == []
