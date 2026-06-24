from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_approved_migration_execution_plan_doc_exists():
    doc = ROOT / "docs" / "57_GWAN_Kubernetes_StatefulSet_Approved_Migration_Execution_Plan.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Approved Migration Execution Plan" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "This step does not execute real migration" in text
    assert "PostgreSQL is still running as Deployment" in text
    assert "No active PostgreSQL StatefulSet exists yet" in text
    assert "Execution Plan Phases" in text
    assert "Pre-check" in text
    assert "Backup" in text
    assert "Approval" in text
    assert "Controlled StatefulSet Apply" in text
    assert "Rollback Readiness" in text
    assert "58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run" in text


def test_approved_migration_execution_plan_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_approved_migration_execution_plan_check.sh"
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
    assert "real migration is not executed" in text


def test_approved_migration_execution_plan_prompt_exists():
    prompt = ROOT / "code" / "57_gwan_kubernetes_statefulset_approved_migration_execution_plan_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Approved Migration Execution Plan" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "Do not create a live StatefulSet" in text
