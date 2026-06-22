from pathlib import Path

WORKFLOW = Path(".github/workflows/gwan-ci.yml")
STEP_DOC = Path("docs/19_GWAN_GitHub_Actions_CI.md")
README = Path("README.md")


def test_github_actions_workflow_exists() -> None:
    assert WORKFLOW.exists()


def test_workflow_runs_pytest_with_python_313() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'python-version:' in text
    assert '"3.13"' in text
    assert 'pip install -r requirements.txt' in text
    assert 'pytest -q' in text


def test_workflow_uses_ci_safe_database_settings() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'DATABASE_URL: sqlite+pysqlite:////tmp/hyean-gwan-ci.db' in text
    assert 'HYEAN_MEMORY_JSONL_PATH: /tmp/hyean-gwan-memory.jsonl' in text


def test_workflow_checks_required_docs() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'test -f README.md' in text
    assert 'test -f docs/API_REFERENCE.md' in text
    assert 'test -f docs/LOCAL_RUNBOOK.md' in text
    assert 'test -f docs/19_GWAN_GitHub_Actions_CI.md' in text


def test_step_19_documentation_exists_and_explains_ci() -> None:
    text = STEP_DOC.read_text(encoding="utf-8")

    assert '19_GWAN_GitHub_Actions_CI' in text
    assert 'GitHub runs pytest automatically' in text
    assert 'Python 3.13' in text
    assert 'SQLite' in text
