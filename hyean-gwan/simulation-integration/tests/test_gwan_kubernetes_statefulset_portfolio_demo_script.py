from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_portfolio_demo_script_doc_exists():
    doc = ROOT / "docs" / "70_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Script.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "Portfolio_Demo_Script" in text
    assert "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE" in text
    assert "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO" in text
    assert "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED" in text
    assert "FINAL_APPROVAL_GATE_STATUS=BLOCKED" in text
    assert "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED" in text
    assert "PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED" in text
    assert "MIGRATION_EXECUTION_ALLOWED=false" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "STATEFULSET_STATUS=NOT_CREATED" in text
    assert "POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC" in text
    assert "71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme" in text


def test_portfolio_demo_script_prompt_exists():
    prompt = ROOT / "code" / "70_gwan_kubernetes_statefulset_portfolio_demo_script_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "portfolio demo script" in text.lower()
    assert "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE" in text
    assert "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO" in text
    assert "PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED" in text
    assert "MIGRATION_EXECUTION_ALLOWED=false" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "STATEFULSET_STATUS=NOT_CREATED" in text
    assert "POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC" in text


def test_portfolio_demo_script_sh_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_portfolio_demo_script.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    required_markers = [
        "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE",
        "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO",
        "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW",
        "CURRENT_DECISION=NO_GO",
        "APPROVED_BY_OPERATOR=false",
        "FINAL_DECISION=NO_GO",
        "OPERATOR_FINAL_APPROVAL_STATUS=NOT_APPROVED",
        "FINAL_APPROVAL_GATE_STATUS=BLOCKED",
        "PREFLIGHT_STATUS=PASSED_BUT_BLOCKED",
        "PORTFOLIO_DEMO_SCRIPT_STATUS=CREATED",
        "MIGRATION_EXECUTION_ALLOWED=false",
        "REAL_MIGRATION_EXECUTED=false",
        "SECRET_VALUES_EXPORTED=false",
        "STATEFULSET_STATUS=NOT_CREATED",
        "POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC",
        "Do not execute real migration",
        "Do not export Secret values",
        "Do not create active PostgreSQL StatefulSet",
        "statefulset_portfolio_demo_readiness_report.sh",
        "71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme",
    ]

    for marker in required_markers:
        assert marker in text


def test_portfolio_demo_script_does_not_execute_real_migration():
    script = ROOT / "scripts" / "k8s" / "statefulset_portfolio_demo_script.sh"
    text = script.read_text(encoding="utf-8")

    forbidden_commands = [
        "kubectl delete deployment postgres",
        "kubectl scale deployment postgres",
        "kubectl rollout restart deployment/postgres",
        "kubectl create secret",
        "kubectl set image",
    ]

    for command in forbidden_commands:
        assert command not in text
