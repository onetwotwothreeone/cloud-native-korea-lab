from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_migration_command_dry_run_doc_exists():
    doc = ROOT / "docs" / "58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Migration Command Dry Run" in text
    assert "This step does not execute real migration" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "PostgreSQL is still running as Deployment" in text
    assert "No active PostgreSQL StatefulSet exists yet" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "kubectl apply --dry-run=client" in text
    assert "Do not create a live PostgreSQL StatefulSet" in text
    assert "59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review" in text


def test_migration_command_dry_run_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_migration_command_dry_run_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "get deployment postgres" in text
    assert "get pvc postgres-data" in text
    assert "get svc postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "kubectl kustomize k8s/drafts" in text
    assert "kubectl apply --dry-run=client" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "does not execute real migration" in text


def test_migration_command_dry_run_prompt_exists():
    prompt = ROOT / "code" / "58_gwan_kubernetes_statefulset_migration_command_dry_run_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Migration Command Dry Run" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "Do not create a live StatefulSet" in text
    assert "Do not delete the current PostgreSQL Deployment" in text
