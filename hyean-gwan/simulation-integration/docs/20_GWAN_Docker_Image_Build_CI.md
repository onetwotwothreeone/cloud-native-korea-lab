# 20_GWAN_Docker_Image_Build_CI

## Purpose

This step extends GitHub Actions from Python test validation to Docker image validation.

Previous step:

```text
pytest runs automatically in GitHub Actions
```

This step:

```text
pytest runs automatically
→ Docker image builds automatically
→ container starts successfully
→ /health smoke test passes
```

## Why this matters

HYEAN/GWAN is moving toward a cloud-native implementation path. A backend prototype should not only pass Python tests. It should also be packageable as a reproducible container image.

Docker image build CI checks that:

- dependencies install correctly in a clean Linux container
- the FastAPI app can be copied into an image
- Uvicorn can start inside the container
- `/health` responds successfully

## Added files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/Dockerfile
hyean-gwan/simulation-integration/.dockerignore
hyean-gwan/simulation-integration/tests/test_gwan_docker_image_build_ci.py
hyean-gwan/simulation-integration/docs/20_GWAN_Docker_Image_Build_CI.md
hyean-gwan/simulation-integration/codex/20_gwan_docker_image_build_ci_prompt.md
```

## Important workflow placement

GitHub Actions only detects workflow files under the repository root:

```text
.github/workflows/*.yml
```

A workflow inside a nested project folder, such as this path, is useful as a copied reference but will not run by itself:

```text
hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml
```

The real workflow must be committed at:

```text
.cloud-native-korea-lab/.github/workflows/gwan-ci.yml
```

## CI behavior

The workflow runs on:

```text
push
pull_request
workflow_dispatch
```

It checks:

```text
1. Python 3.13 setup
2. pip install -r requirements.txt
3. pytest -q
4. required documentation files exist
5. docker build -t hyean-gwan-simulation:ci .
6. docker run container
7. curl /health
```

## Manual local check

From the project folder:

```bash
docker build -t hyean-gwan-simulation:local .
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="sqlite+pysqlite:////tmp/hyean-gwan-local.db" \
  hyean-gwan-simulation:local
```

Then open:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"ok"}
```

## Completion criteria

- Local `pytest -q` passes.
- Docker image builds locally.
- GitHub Actions runs from repository root.
- GitHub Actions shows green check.
- Docker smoke test calls `/health` successfully.
