from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_final_approval_review_doc_exists():
    doc = ROOT / "docs" / "55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Final Approval Review" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "Do not execute real migration" in text
    assert "HYEAN" in text
    assert "GWAN" in text
    assert "prevention-first" in text


def test_final_approval_review_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_final_approval_review_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "kubectl -n" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get statefulset postgres" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "does not execute real migration" in text


def test_codex_prompt_exists_for_final_approval_review():
    prompt = ROOT / "code" / "55_gwan_kubernetes_statefulset_final_approval_review_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Final Approval Review" in text
    assert "Do not execute real migration" in text
    assert "FINAL_DECISION remains NO_GO" in text
