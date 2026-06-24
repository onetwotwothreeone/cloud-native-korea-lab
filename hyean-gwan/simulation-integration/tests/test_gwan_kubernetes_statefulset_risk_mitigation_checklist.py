from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_risk_mitigation_checklist_doc_exists():
    doc = ROOT / "docs" / "61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Risk Mitigation Checklist" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "DATA_LOSS_RISK=MITIGATED" in text
    assert "DOWNTIME_RISK=MITIGATED" in text
    assert "WORKLOAD_CONFLICT_RISK=MITIGATED" in text
    assert "ROLLBACK_RISK=MITIGATED" in text
    assert "APPROVAL_BYPASS_RISK=MITIGATED" in text
    assert "62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot" in text


def test_risk_mitigation_script_exists_and_is_safe():
    script = ROOT / "scripts" / "k8s" / "statefulset_risk_mitigation_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "kubectl -n" in text
    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get service postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "kubectl apply -f k8s/drafts" not in text
    assert "kubectl delete deployment postgres" not in text


def test_codex_prompt_exists():
    prompt = ROOT / "codex" / "61_gwan_kubernetes_statefulset_risk_mitigation_checklist_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Do not execute real migration" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot" in text
