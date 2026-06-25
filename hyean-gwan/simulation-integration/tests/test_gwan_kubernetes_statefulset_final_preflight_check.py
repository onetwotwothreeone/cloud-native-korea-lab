from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_preflight_doc_exists():
    doc = ROOT / "docs" / "68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "Final_Preflight_Check" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
    assert "READINESS_STATUS=SUMMARY_ONLY" in text
    assert "BACKUP_FRESHNESS_STATUS=PASSED" in text
    assert "DATA_INTEGRITY_STATUS=PASSED" in text
    assert "FINAL_APPROVAL_GATE_STATUS=BLOCKED" in text
    assert "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED" in text
    assert "MIGRATION_EXECUTION_ALLOWED=false" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report" in text


def test_final_preflight_prompt_exists():
    prompt = ROOT / "code" / "68_gwan_kubernetes_statefulset_final_preflight_check_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "final preflight check" in text.lower()
    assert "CURRENT_DECISION=NO_GO" in text
    assert "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED" in text
    assert "MIGRATION_EXECUTION_ALLOWED=false" in text
    assert "Do not execute real migration" in text


def test_final_preflight_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_preflight_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    required_markers = [
        "CURRENT_DECISION=NO_GO",
        "APPROVED_BY_OPERATOR=false",
        "FINAL_DECISION=NO_GO",
        "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED",
        "READINESS_STATUS=SUMMARY_ONLY",
        "BACKUP_FRESHNESS_STATUS=PASSED",
        "DATA_INTEGRITY_STATUS=PASSED",
        "FINAL_APPROVAL_GATE_STATUS=BLOCKED",
        "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED",
        "MIGRATION_EXECUTION_ALLOWED=false",
        "REAL_MIGRATION_EXECUTED=false",
        "SECRET_VALUES_EXPORTED=false",
        "Do not execute real migration",
        "Do not export Secret values",
        "Do not create active PostgreSQL StatefulSet",
        "statefulset_premigration_readiness_summary.sh",
        "statefulset_final_approval_gate.sh",
        "69_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readiness_Report",
    ]

    for marker in required_markers:
        assert marker in text


def test_final_preflight_script_does_not_mutate_postgres():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_preflight_check.sh"
    text = script.read_text(encoding="utf-8")

    forbidden_commands = [
        "kubectl apply -f",
        "kubectl delete deployment postgres",
        "kubectl scale deployment postgres",
        "kubectl rollout restart deployment/postgres",
    ]

    for command in forbidden_commands:
        assert command not in text
