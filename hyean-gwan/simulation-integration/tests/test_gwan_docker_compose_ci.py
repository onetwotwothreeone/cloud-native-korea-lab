from pathlib import Path


def test_compose_ci_file_exists_and_defines_api_and_postgres() -> None:
    compose_file = Path("docker-compose.ci.yml")
    assert compose_file.exists()
    content = compose_file.read_text(encoding="utf-8")

    assert "postgres:16-alpine" in content
    assert "hyean-gwan-postgres-ci" in content
    assert "hyean-gwan-api-ci" in content
    assert "DATABASE_URL: postgresql+psycopg://hyean:hyean_password@postgres:5432/hyean_gwan" in content
    assert "condition: service_healthy" in content
    assert '"8000:8000"' in content
    assert '"55432:5432"' in content


def test_github_actions_workflow_runs_docker_compose_integration() -> None:
    workflow = Path(".github/workflows/gwan-ci.yml")
    assert workflow.exists()
    content = workflow.read_text(encoding="utf-8")

    assert "name: GWAN CI" in content
    assert "pytest -q" in content
    assert "docker build -t hyean-gwan-simulation:ci ." in content
    assert "Docker Compose integration test" in content
    assert "docker compose -f docker-compose.ci.yml up -d --build" in content
    assert "curl -f http://127.0.0.1:8000/health" in content
    assert "curl -f http://127.0.0.1:8000/gwan/memory/db-status" in content
    assert "docker compose -f docker-compose.ci.yml down -v --remove-orphans" in content


def test_step_21_documentation_exists() -> None:
    text = Path("docs/21_GWAN_Docker_Compose_CI.md").read_text(encoding="utf-8")

    assert "21_GWAN_Docker_Compose_CI" in text
    assert "FastAPI container" in text
    assert "PostgreSQL container" in text
    assert "/gwan/memory/db-status" in text
    assert "docker-compose.ci.yml" in text
