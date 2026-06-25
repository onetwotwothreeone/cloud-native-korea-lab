from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_approval_gate_doc_exists():
    doc = ROOT / "docs" / "67_GWAN_Kubernetes_StatefulSet_Final_Approval_Gate.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "StatefulSet_Final_Approval_Gate" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
    assert "READINESS_STATUS=SUMMARY_ONLY" in text
    assert "BACKUP_FRESHNESS_STATUS=PASSED" in text
    assert "DATA_INTEGRITY_STATUS=PASSED" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "FINAL_APPROVAL_GATE_STATUS=BLOCKED" in text
    assert "68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check" in text


def test_final_approval_gate_prompt_exists():
    prompt = ROOT / "code" / "67_gwan_kubernetes_statefulset_final_approval_gate_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "final approval gate" in text.lower()
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_APPROVAL_GATE_STATUS=BLOCKED" in text
    assert "Do not execute real migration" in text


def test_final_approval_gate_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_approval_gate.sh"
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
        "REAL_MIGRATION_EXECUTED=false",
        "SECRET_VALUES_EXPORTED=false",
        "FINAL_APPROVAL_GATE_STATUS=BLOCKED",
        "Do not execute real migration",
        "kubectl -n",
        "get statefulset postgres",
        "68_GWAN_Kubernetes_StatefulSet_Final_Preflight_Check",
    ]

    for marker in required_markers:
        assert marker in text


def test_final_approval_gate_script_keeps_migration_blocked():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_approval_gate.sh"
    text = script.read_text(encoding="utf-8")

    assert "kubectl apply -f" not in text
    assert "kubectl delete deployment postgres" not in text
    assert "kubectl scale deployment postgres --replicas=0" not in text
    assert "FINAL_APPROVAL_GATE_STATUS=\"BLOCKED\"" in text
