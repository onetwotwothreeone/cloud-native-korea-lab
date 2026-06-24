from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_premigration_readiness_summary_doc_exists():
    doc = ROOT / "docs" / "65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "PreMigration Readiness Summary" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "READINESS_STATUS=SUMMARY_ONLY" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "BACKUP_FRESHNESS_STATUS=PASSED" in text
    assert "DATA_INTEGRITY_STATUS=PASSED" in text
    assert "66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record" in text


def test_premigration_readiness_summary_prompt_exists():
    prompt = ROOT / "code" / "65_gwan_kubernetes_statefulset_premigration_readiness_summary_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Do not execute real migration" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text


def test_premigration_readiness_summary_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_premigration_readiness_summary.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=\"NO_GO\"" in text
    assert "APPROVED_BY_OPERATOR=\"false\"" in text
    assert "FINAL_DECISION=\"NO_GO\"" in text
    assert "READINESS_STATUS=\"SUMMARY_ONLY\"" in text
    assert "REAL_MIGRATION_EXECUTED=\"false\"" in text
    assert "SECRET_VALUES_EXPORTED=\"false\"" in text
    assert "BACKUP_FRESHNESS_STATUS=\"PASSED\"" in text
    assert "DATA_INTEGRITY_STATUS=\"PASSED\"" in text
    assert "pg_isready" in text
    assert "SELECT 1;" in text
    assert "information_schema.tables" in text
    assert "kubectl -n" in text
    assert "get statefulset postgres" in text
    assert "66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record" in text
