from pathlib import Path

README = Path("README.md")
API_REFERENCE = Path("docs/API_REFERENCE.md")
LOCAL_RUNBOOK = Path("docs/LOCAL_RUNBOOK.md")
STEP_DOC = Path("docs/16_GWAN_API_Documentation_and_README_Polish.md")
CHECKLIST = Path("docs/README_REVIEW_CHECKLIST.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_readme_contains_current_hyean_gwan_positioning() -> None:
    text = read(README)

    assert "HYEAN is a survival-oriented space intelligence service" in text
    assert "GWAN is the core observation, interpretation, scoring, decision, and memory engine" in text
    assert "synthetic and simulated data only" in text


def test_readme_contains_required_local_commands() -> None:
    text = read(README)

    assert "pytest -q" in text
    assert "docker compose up -d postgres" in text
    assert "127.0.0.1:55432" in text
    assert "uvicorn app.main:app --reload" in text


def test_api_reference_lists_critical_routes() -> None:
    text = read(API_REFERENCE)
    required_routes = [
        "/health",
        "/gwan/simulate-integrated",
        "/gwan/scoring-test-cases",
        "/gwan/memory/persist-simulated-snapshot",
        "/gwan/memory/query/high-risk",
        "/gwan/memory/postgres-design",
        "/gwan/memory/db-status",
        "/gwan/memory/db-create-tables",
        "/gwan/memory/db-persist-simulated-snapshot",
        "/gwan/memory/db-query/high-risk",
        "/gwan/memory/db-query/high-uncertainty",
        "/gwan/memory/db-query/action/{recommended_action}",
    ]

    for route in required_routes:
        assert route in text


def test_local_runbook_documents_postgres_port_and_troubleshooting() -> None:
    text = read(LOCAL_RUNBOOK)

    assert "55432->5432" in text
    assert "DATABASE_URL" in text
    assert "FATAL: role \"hyean\" does not exist" in text
    assert "docker compose down -v" in text


def test_step_16_docs_and_checklist_exist_with_purpose() -> None:
    step_text = read(STEP_DOC)
    checklist_text = read(CHECKLIST)

    assert "16_GWAN_API_Documentation_and_README_Polish" in step_text
    assert "README Review Checklist" in checklist_text
    assert "PostgreSQL uses host port `55432`" in checklist_text
