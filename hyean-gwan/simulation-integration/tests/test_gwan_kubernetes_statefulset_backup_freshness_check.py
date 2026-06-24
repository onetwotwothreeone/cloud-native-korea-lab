from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_backup_freshness_check_doc_exists():
    doc = ROOT / "docs" / "63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "Backup Freshness Check" in text
    assert "latest backup file exists" in text
    assert "backup age is within acceptable window" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check" in text


def test_backup_freshness_check_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_backup_freshness_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "BACKUP_DIR" in text
    assert "BACKUP_MAX_AGE_SECONDS" in text
    assert "LATEST_BACKUP_FILE" in text
    assert "BACKUP_AGE_SECONDS" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "FINAL_DECISION" in text
    assert "64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check" in text


def test_backup_freshness_code_prompt_exists():
    prompt = ROOT / "code" / "63_gwan_kubernetes_statefulset_backup_freshness_check_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Code Prompt" in text
    assert "Do not execute real migration." in text
    assert "Do not export secret values." in text
    assert "FINAL_DECISION=NO_GO" in text
