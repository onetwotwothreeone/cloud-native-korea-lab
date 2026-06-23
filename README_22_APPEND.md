
## 22. GHCR image push

GWAN CI now publishes the tested Docker image to GitHub Container Registry.

```text
pytest
→ Docker build
→ container smoke test
→ Docker Compose API + PostgreSQL test
→ GHCR image push
```

Image name:

```text
ghcr.io/<github-owner>/hyean-gwan-simulation
```

The workflow pushes images only on `push` to `main`. Pull requests still run tests and builds, but do not push images.

After the workflow passes, check:

```text
GitHub repository → Packages → hyean-gwan-simulation
```
