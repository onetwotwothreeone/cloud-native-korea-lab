from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_manual_approval_record_doc_exists():
    doc = ROOT / "docs" / "52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "NOT_APPROVED_YET" in text
    assert "PostgreSQL is still Deployment" in text
    assert "Real PostgreSQL StatefulSet migration remains blocked" in text
    assert "53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template" in text

def test_manual_approval_record_script_exists_and_blocks_real_migration():
    script = ROOT / "scripts" / "k8s" / "statefulset_manual_approval_record_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "get deployment postgres" in text
    assert "get statefulset postgres" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "real migration is still blocked" in text

def test_manual_approval_record_codex_prompt_exists():
    prompt = ROOT / "codex" / "52_gwan_kubernetes_statefulset_manual_approval_record_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "no real StatefulSet migration is executed" in text
    assert "53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template" in text
