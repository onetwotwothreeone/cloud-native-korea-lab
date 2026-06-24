from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cutover_decision_gate_doc_exists():
    doc = ROOT / "docs" / "49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Cutover Decision Gate" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "PostgreSQL is still Deployment" in text
    assert "Do not execute real migration" in text
    assert "HYEAN" in text
    assert "GWAN" in text


def test_cutover_decision_gate_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_cutover_decision_gate_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "kubectl -n" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get statefulset postgres" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "does not execute real migration" in text


def test_cutover_decision_gate_prompt_exists():
    prompt = ROOT / "code" / "49_gwan_kubernetes_statefulset_cutover_decision_gate_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Cutover Decision Gate" in text
    assert "Do not execute real migration" in text
    assert "NO_GO" in text
