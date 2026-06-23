from pathlib import Path

WORKFLOW = Path(".github/workflows/gwan-ci.yml")
STEP_DOC = Path("docs/22_GWAN_GHCR_Image_Push.md")


def test_workflow_has_ghcr_publish_permissions() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "permissions:" in text
    assert "contents: read" in text
    assert "packages: write" in text


def test_workflow_logs_in_to_ghcr_with_github_token() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "docker/login-action@v3" in text
    assert "registry: ghcr.io" in text
    assert "username: ${{ github.actor }}" in text
    assert "password: ${{ secrets.GITHUB_TOKEN }}" in text


def test_workflow_builds_and_pushes_image_to_ghcr() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "docker/metadata-action@v5" in text
    assert "docker/build-push-action@v6" in text
    assert "GHCR_IMAGE_NAME: ghcr.io/${{ github.repository_owner }}/hyean-gwan-simulation" in text
    assert "context: hyean-gwan/simulation-integration" in text
    assert "file: hyean-gwan/simulation-integration/Dockerfile" in text
    assert "push: true" in text
    assert "type=sha,prefix=sha-" in text
    assert "type=raw,value=latest" in text


def test_workflow_pushes_only_on_main_push() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "if: github.event_name == 'push' && github.ref == 'refs/heads/main'" in text
    assert "pull_request:" in text


def test_step_22_documentation_exists() -> None:
    text = STEP_DOC.read_text(encoding="utf-8")

    assert "22_GWAN_GHCR_Image_Push" in text
    assert "GitHub Container Registry" in text
    assert "ghcr.io" in text
    assert "hyean-gwan-simulation" in text
    assert "packages: write" in text
