
## 20. Docker image build CI

GWAN CI now verifies not only Python tests but also Docker image packaging.

```text
pytest -q
→ docker build
→ docker run
→ curl /health
```

Important: GitHub Actions workflows must live at the repository root.

```text
.github/workflows/gwan-ci.yml
```

The Docker build context is:

```text
hyean-gwan/simulation-integration
```

Manual local check:

```bash
cd hyean-gwan/simulation-integration
docker build -t hyean-gwan-simulation:local .
docker run --rm -p 8000:8000 hyean-gwan-simulation:local
```

Then check:

```text
http://127.0.0.1:8000/health
```
