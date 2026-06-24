from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operator_approval_gate_doc_exists():
    doc = ROOT / "docs" / "53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "Operator Approval Gate" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "real migration remains blocked" in text
    assert "54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check" in text


def test_operator_approval_gate_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_operator_approval_gate_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "APPROVAL_GATE=OPEN" in text
    assert "APPROVAL_GATE=CLOSED" in text
    assert "CURRENT_DECISION" in text
    assert "APPROVED_BY_OPERATOR" in text
    assert "FINAL_DECISION" in text
    assert "does not execute real migration" in text


def test_codex_prompt_exists_for_operator_approval_gate():
    prompt = ROOT / "codex" / "53_gwan_kubernetes_statefulset_operator_approval_gate_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Codex Prompt" in text
    assert "Operator Approval Gate" in text
    assert "Do not execute real migration" in text
