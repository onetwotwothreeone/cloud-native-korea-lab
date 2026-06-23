# Codex task: 20_GWAN_Docker_Image_Build_CI

## Goal

Extend GWAN CI so GitHub Actions verifies both Python tests and Docker image build.

## Required files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/Dockerfile
hyean-gwan/simulation-integration/.dockerignore
hyean-gwan/simulation-integration/tests/test_gwan_docker_image_build_ci.py
hyean-gwan/simulation-integration/docs/20_GWAN_Docker_Image_Build_CI.md
```

## Requirements

- Workflow must live at repository root: `.github/workflows/gwan-ci.yml`.
- Workflow must use Python 3.13.
- Workflow must run `pytest -q` inside `hyean-gwan/simulation-integration`.
- Workflow must build Docker image with `docker build`.
- Workflow must run the container and smoke test `/health`.
- Dockerfile must run FastAPI with Uvicorn.
- Add tests checking Dockerfile, `.dockerignore`, and workflow content.

## Success criteria

```bash
pytest -q
```

GitHub Actions should show a green check after push.
