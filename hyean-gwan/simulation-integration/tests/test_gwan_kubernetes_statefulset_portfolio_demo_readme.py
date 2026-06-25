from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_portfolio_demo_readme_doc_exists():
    doc = ROOT / "docs" / "71_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Readme.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    required = [
        "PORTFOLIO_DEMO_README_STATUS=CREATED",
        "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE",
        "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO",
        "DEMO_STATUS=READY_FOR_PORTFOLIO_REVIEW",
        "POSTGRES_CURRENT_MODE=DEPLOYMENT_WITH_PVC",
        "STATEFULSET_STATUS=NOT_CREATED",
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
        "72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook",
    ]

    for marker in required:
        assert marker in text


def test_portfolio_demo_readme_prompt_exists():
    prompt = ROOT / "code" / "71_gwan_kubernetes_statefulset_portfolio_demo_readme_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "beginner-friendly README" in text
    assert "PORTFOLIO_DEMO_README_STATUS=CREATED" in text
    assert "MIGRATION_EXECUTION_ALLOWED=false" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SECRET_VALUES_EXPORTED=false" in text


def test_portfolio_demo_readme_script_exists():
    script = ROOT / "scripts" / "k8s" / "statefulset_portfolio_demo_readme.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    required = [
        "HYEAN_SERVICE_GOAL=PREVENTIVE_SURVIVAL_INTELLIGENCE",
        "DEMO_TITLE=HYEAN_GWAN_POSTGRESQL_STATEFULSET_SAFETY_DEMO",
        "PORTFOLIO_DEMO_README_STATUS=CREATED",
        "statefulset-portfolio-demo-readme.md",
        "statefulset-portfolio-demo-script.md",
        "MIGRATION_EXECUTION_ALLOWED=false",
        "REAL_MIGRATION_EXECUTED=false",
        "SECRET_VALUES_EXPORTED=false",
        "Do not execute real migration",
        "Do not export Secret values",
        "Do not create active PostgreSQL StatefulSet",
        "72_GWAN_Kubernetes_StatefulSet_Portfolio_Demo_Runbook",
    ]

    for marker in required:
        assert marker in text


def test_portfolio_demo_readme_script_does_not_execute_real_migration():
    script = ROOT / "scripts" / "k8s" / "statefulset_portfolio_demo_readme.sh"
    text = script.read_text(encoding="utf-8")

    forbidden = [
        "kubectl delete deployment postgres",
        "kubectl scale deployment postgres",
        "kubectl rollout restart deployment/postgres",
        "kubectl create secret",
        "kubectl set image",
    ]

    for command in forbidden:
        assert command not in text
