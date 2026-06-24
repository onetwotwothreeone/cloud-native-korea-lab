from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_migration_risk_register_doc_exists():
    doc = ROOT / "docs" / "60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Migration Risk Register" in text
    assert "This step does not execute real migration" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "RISK_REGISTER_STATUS=REVIEW_ONLY" in text
    assert "PostgreSQL is still running as Deployment" in text
    assert "No active PostgreSQL StatefulSet exists yet" in text
    assert "Data loss during migration" in text
    assert "PostgreSQL downtime" in text
    assert "PVC mismatch" in text
    assert "Secret mismatch" in text
    assert "ConfigMap mismatch" in text
    assert "Service routing error" in text
    assert "StatefulSet manifest error" in text
    assert "Rollback plan missing" in text
    assert "Operator approval confusion" in text
    assert "Real migration remains blocked" in text
    assert "61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist" in text


def test_migration_risk_register_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_migration_risk_register_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "get deployment postgres" in text
    assert "get pods -l app.kubernetes.io/name=gwan-postgres" in text
    assert "get pvc postgres-data" in text
    assert "get svc postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "Migration Risk Register" in text
    assert "RISK_REGISTER_STATUS=REVIEW_ONLY" in text
    assert "real migration remains blocked" in text


def test_migration_risk_register_prompt_exists():
    prompt = ROOT / "code" / "60_gwan_kubernetes_statefulset_migration_risk_register_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Migration Risk Register" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "RISK_REGISTER_STATUS=REVIEW_ONLY" in text
    assert "Do not run real migration" in text
