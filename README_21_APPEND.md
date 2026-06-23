
## 21. Docker Compose CI

GWAN CI now verifies the API and PostgreSQL together with Docker Compose.

```text
pytest -q
→ docker build
→ docker run /health
→ docker compose up API + PostgreSQL
→ /health
→ /gwan/memory/db-status
```

Manual local check:

```bash
cd hyean-gwan/simulation-integration
docker compose -f docker-compose.ci.yml up -d --build
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
docker compose -f docker-compose.ci.yml down -v --remove-orphans
```

This step proves that the FastAPI container and PostgreSQL container can run together through Docker Compose.
