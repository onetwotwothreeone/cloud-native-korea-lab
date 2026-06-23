from pathlib import Path


def test_dockerfile_exists_and_runs_fastapi() -> None:
    dockerfile = Path("Dockerfile")
    assert dockerfile.exists()
    content = dockerfile.read_text(encoding="utf-8")

    assert "FROM python:3.13-slim" in content
    assert "pip install -r requirements.txt" in content
    assert "uvicorn" in content
    assert "app.main:app" in content
    assert "EXPOSE 8000" in content


def test_dockerignore_excludes_local_noise() -> None:
    content = Path(".dockerignore").read_text(encoding="utf-8")

    assert ".venv" in content
    assert "__pycache__" in content
    assert ".pytest_cache" in content
    assert ".env" in content
    assert "data" in content


def test_github_actions_workflow_builds_docker_image() -> None:
    # Local project copy for documentation/test compatibility.
    nested_workflow = Path(".github/workflows/gwan-ci.yml")
    assert nested_workflow.exists()
    content = nested_workflow.read_text(encoding="utf-8")

    assert "name: GWAN CI" in content
    assert "pytest -q" in content
    assert "docker build -t hyean-gwan-simulation:ci ." in content
    assert "docker run -d --name hyean-gwan-ci" in content
    assert "curl -f http://127.0.0.1:8000/health" in content
    assert "working-directory: hyean-gwan/simulation-integration" in content


def test_step_20_documentation_exists() -> None:
    text = Path("docs/20_GWAN_Docker_Image_Build_CI.md").read_text(encoding="utf-8")

    assert "20_GWAN_Docker_Image_Build_CI" in text
    assert "Docker image builds automatically" in text
    assert "GitHub Actions only detects workflow files under the repository root" in text
    assert "/health" in text
