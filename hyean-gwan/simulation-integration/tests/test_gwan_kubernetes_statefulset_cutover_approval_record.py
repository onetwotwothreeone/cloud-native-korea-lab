from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_approval_record_doc_exists_and_blocks_real_migration():
    doc = ROOT / "docs" / "50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "CURRENT_DECISION: NO_GO" in text
    assert "FINAL_DECISION: NO_GO" in text
    assert "APPROVED_BY_OPERATOR: true" in text
    assert "51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template" in text

def test_approval_record_script_exists_and_is_safe():
    script = ROOT / "scripts" / "k8s" / "statefulset_cutover_approval_record_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "kubectl -n" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text

def test_codex_prompt_exists():
    prompt = ROOT / "codex" / "50_gwan_kubernetes_statefulset_cutover_approval_record_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Do not execute the migration" in text
    assert "operator approval is required" in text
