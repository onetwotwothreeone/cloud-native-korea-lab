from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_premigration_final_check_doc_exists():
    doc = ROOT / "docs" / "54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "PreMigration Final Check" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "This step does not execute a real migration." in text
    assert "55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review" in text


def test_premigration_final_check_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_premigration_final_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "kubectl -n \"$NS\" get deployment postgres" in text
    assert "kubectl -n \"$NS\" get pods -l app.kubernetes.io/name=gwan-postgres" in text
    assert "kubectl -n \"$NS\" get pvc postgres-data" in text
    assert "kubectl -n \"$NS\" get service postgres" in text
    assert "kubectl -n \"$NS\" get secret gwan-postgres-secret" in text
    assert "kubectl -n \"$NS\" get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "FINAL_DECISION=NO_GO" in text


def test_codex_prompt_exists_for_premigration_final_check():
    prompt = ROOT / "code" / "54_gwan_kubernetes_statefulset_premigration_final_check_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Codex Prompt" in text
    assert "Do not execute real migration." in text
    assert "FINAL_DECISION=NO_GO" in text
