from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_premigration_data_integrity_doc_exists():
    doc = ROOT / "docs" / "64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "PreMigration Data Integrity Check" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "DATA_INTEGRITY_STATUS=REVIEW_ONLY" in text
    assert "READ_ONLY_CHECK=true" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary" in text


def test_premigration_data_integrity_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_premigration_data_integrity_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "DATA_INTEGRITY_STATUS=REVIEW_ONLY" in text
    assert "READ_ONLY_CHECK=true" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "pg_isready" in text
    assert "SELECT current_database();" in text
    assert "information_schema.tables" in text
    assert "premigration-data-integrity" in text
    assert "kubectl -n" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get service postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "postgres_backup_restore_check.sh" in text
    assert "65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary" in text


def test_premigration_data_integrity_script_is_read_only():
    script = ROOT / "scripts" / "k8s" / "statefulset_premigration_data_integrity_check.sh"
    text = script.read_text(encoding="utf-8")

    assert "kubectl delete" not in text
    assert "kubectl patch" not in text
    assert "kubectl replace" not in text
    assert "kubectl scale" not in text
    assert "pg_restore" not in text
    assert "drop database" not in text.lower()
    assert "create database" not in text.lower()
    assert "alter table" not in text.lower()
    assert "truncate" not in text.lower()


def test_premigration_data_integrity_codex_prompt_exists():
    prompt = ROOT / "code" / "64_gwan_kubernetes_statefulset_premigration_data_integrity_check_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Codex Prompt" in text
    assert "Do not execute real migration." in text
    assert "READ_ONLY_CHECK=true" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
