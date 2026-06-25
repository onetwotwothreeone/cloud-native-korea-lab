from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_operator_final_approval_record_doc_exists():
    doc = ROOT / "docs" / "66_GWAN_Kubernetes_StatefulSet_Operator_Final_Approval_Record.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Operator Final Approval Record" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate" in text


def test_operator_final_approval_record_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_operator_final_approval_record.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
    assert "READINESS_STATUS=SUMMARY_ONLY" in text
    assert "BACKUP_FRESHNESS_STATUS=PASSED" in text
    assert "DATA_INTEGRITY_STATUS=PASSED" in text
    assert "READ_ONLY_CHECK=true" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "statefulset_premigration_readiness_summary.sh" in text
    assert ".local/operator-approvals/statefulset-final-approval-record.env" in text
    assert "kubectl -n" in text
    assert "get statefulset postgres" in text
    assert "67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate" in text


def test_operator_final_approval_record_prompt_exists():
    prompt = ROOT / "code" / "66_gwan_kubernetes_statefulset_operator_final_approval_record_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Do not execute real migration" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
