from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_operator_approval_template_doc_exists():
    doc = ROOT / "docs" / "51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "CURRENT_DECISION: NO_GO" in text
    assert "Operator Name" in text
    assert "Approval Date" in text
    assert "APPROVED_BY_OPERATOR=true" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record" in text

def test_operator_approval_template_script_exists_and_is_safe():
    script = ROOT / "scripts" / "k8s" / "statefulset_operator_approval_template_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record" in text

def test_operator_approval_codex_prompt_exists():
    prompt = ROOT / "codex" / "51_gwan_kubernetes_statefulset_operator_approval_template_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "manual operator approval template" in text
    assert "no real migration execution" in text
    assert "52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record" in text
