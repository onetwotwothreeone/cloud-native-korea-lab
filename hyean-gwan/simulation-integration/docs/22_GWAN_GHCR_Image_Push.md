# 22_GWAN_GHCR_Image_Push

## Purpose

This step publishes the tested GWAN Docker image to GitHub Container Registry, also called GHCR.

Previous step:

```text
Docker image build and Docker Compose integration test
```

This step:

```text
Docker image build
→ GHCR login
→ image metadata and tags
→ push image to ghcr.io
```

## Why this matters

A Docker image is useful only when another environment can pull and run it.

For HYEAN/GWAN, GHCR becomes the first image registry stage:

```text
GitHub repository
→ GitHub Actions
→ Docker image
→ GitHub Container Registry
→ future Kubernetes deployment
```

This supports the future path toward Kubernetes, GitOps, and repeatable deployments.

## New workflow behavior

The workflow still checks:

```text
pytest
Docker build
single-container /health smoke test
Docker Compose API + PostgreSQL integration
```

After those pass, the workflow also pushes the image to GHCR on `push` to `main`.

## Image name

```text
ghcr.io/${{ github.repository_owner }}/hyean-gwan-simulation
```

Example after push:

```text
ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest
ghcr.io/onetwotwothreeone/hyean-gwan-simulation:sha-<commit-sha>
```

## Important security decision

The workflow uses:

```yaml
permissions:
  contents: read
  packages: write
```

It only pushes to GHCR on:

```text
push to main
```

Pull requests still run tests and builds, but they do not push images.

## New workflow steps

```text
Log in to GitHub Container Registry
Extract Docker metadata
Build and push image to GHCR
```

## Manual verification

After the GitHub Actions run passes, check:

```text
GitHub repository
→ Packages
→ hyean-gwan-simulation
```

Later, the image can be pulled with:

```bash
docker pull ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest
```

If the package is private, authentication may be required.

## Completion criteria

- Tests pass.
- Docker image builds.
- Docker Compose integration test passes.
- GHCR login step succeeds on push to main.
- Image is pushed to `ghcr.io`.
- GitHub Packages shows `hyean-gwan-simulation`.
