# Codex task: 22_GWAN_GHCR_Image_Push

## Goal

Extend GWAN CI so the Docker image is pushed to GitHub Container Registry after tests, Docker build, and Docker Compose integration pass.

## Required files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/docs/22_GWAN_GHCR_Image_Push.md
hyean-gwan/simulation-integration/tests/test_gwan_ghcr_image_push_ci.py
```

## Required workflow behavior

- Keep pytest.
- Keep Docker build.
- Keep single-container smoke test.
- Keep Docker Compose integration test.
- Add permissions:

```yaml
permissions:
  contents: read
  packages: write
```

- Login to GHCR using:

```yaml
registry: ghcr.io
username: ${{ github.actor }}
password: ${{ secrets.GITHUB_TOKEN }}
```

- Push only on `push` to `main`, not pull requests.
- Push image:

```text
ghcr.io/${{ github.repository_owner }}/hyean-gwan-simulation
```

## Success command

```bash
python -m pytest -q
```
