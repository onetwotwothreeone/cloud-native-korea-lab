from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backup_restore_doc_exists() -> None:
    doc = ROOT / "docs/43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "PostgreSQL Backup/Restore Baseline" in text
    assert "pg_dump" in text
    assert "temporary restore database" in text
    assert "Do not restore directly into the main database" in text
    assert "44_GWAN_Kubernetes_StatefulSet_Draft_Manifest" in text


def test_backup_restore_codex_prompt_exists() -> None:
    prompt = ROOT / "codex/43_gwan_kubernetes_postgresql_backup_restore_baseline_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "pg_dump" in text
    assert "temporary database" in text
    assert "Do not overwrite the main database" in text
    assert "44_GWAN_Kubernetes_StatefulSet_Draft_Manifest" in text


def test_backup_restore_script_exists() -> None:
    script = ROOT / "scripts/k8s/postgres_backup_restore_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "pg_dump" in text
    assert "createdb" in text
    assert "dropdb" in text
    assert "hyean_gwan_restore_check" in text
    assert ".local/postgres-backups" in text


def test_backup_directory_is_gitignored() -> None:
    gitignore = ROOT / ".gitignore"
    assert gitignore.exists()

    text = gitignore.read_text(encoding="utf-8")
    assert ".local/" in text


def test_current_postgres_still_uses_deployment_and_pvc() -> None:
    deployment = (ROOT / "k8s/base/postgres-deployment.yaml").read_text(encoding="utf-8")
    pvc = (ROOT / "k8s/base/postgres-pvc.yaml").read_text(encoding="utf-8")

    assert "kind: Deployment" in deployment
    assert "name: postgres" in deployment
    assert "persistentVolumeClaim" in deployment
    assert "claimName: postgres-data" in deployment

    assert "kind: PersistentVolumeClaim" in pvc
    assert "name: postgres-data" in pvc


def test_statefulset_is_still_not_applied_yet() -> None:
    statefulset_files = list((ROOT / "k8s/base").glob("*statefulset*.yaml"))
    assert statefulset_files == []
