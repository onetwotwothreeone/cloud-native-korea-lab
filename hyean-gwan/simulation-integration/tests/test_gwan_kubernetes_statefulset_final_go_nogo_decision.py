from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_go_nogo_decision_doc_exists():
    doc = ROOT / "docs" / "56_GWAN_Kubernetes_StatefulSet_Final_Go_NoGo_Decision.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Final Go/No-Go Decision" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "Final decision remains NO_GO" in text
    assert "PostgreSQL is still running as Deployment" in text
    assert "Do not execute real migration" in text
    assert "57_GWAN_Kubernetes_StatefulSet_Approved_Migration_Execution_Plan" in text
    assert "HYEAN" in text
    assert "GWAN" in text


def test_final_go_nogo_decision_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_go_nogo_decision_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get svc postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "does not execute real migration" in text


def test_final_go_nogo_decision_prompt_exists():
    prompt = ROOT / "code" / "56_gwan_kubernetes_statefulset_final_go_nogo_decision_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Final GO/NO-GO Decision" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "Do not execute real migration" in text
