# Cloud Native AI Evaluation Platform

Cloud Native AI Evaluation Platform is the flagship portfolio project of Cloud Native Korea Lab.

The goal is to build a small cloud-native platform for AI data evaluation, annotation workflows, human feedback, quality scoring, and review management.

This project connects AI data quality, FastAPI API design, PostgreSQL, Docker, Kubernetes, GitHub Actions, and future real service development.

---

## Project Positioning

```text
mini-platform = practice sandbox
ai-evaluation-platform = flagship portfolio
```

The previous `mini-platform` was used to practice:

- FastAPI basics
- Docker
- Docker Compose
- Kubernetes
- readinessProbe / livenessProbe
- GitHub Actions
- GHCR
- Kustomize
- dev/prod namespace separation

This `ai-evaluation-platform` applies those learned patterns to a real portfolio project.

---

## Current Version

```text
v0.1.0
```

---

## Current Features

```text
GET  /
GET  /health
GET  /version
POST /tasks
GET  /tasks
POST /samples
GET  /samples
GET  /samples/{sample_id}
GET  /docs
```

---

## Why This Project Exists

AI models improve when training data, annotations, and human feedback are high quality.

However, AI evaluation workflows often have these problems:

- unclear quality criteria
- inconsistent human judgments
- ambiguous samples that need review
- unstructured feedback
- evaluation results that are difficult to reuse
- weak connection between human feedback and model improvement

This project starts by building a simple API system for managing evaluation tasks.

---

## MVP Direction

The final MVP will support the following workflow:

```text
Create evaluation task
→ Register sample
→ Submit annotation
→ Submit quality score
→ Mark review_required
→ Store results
→ Export or review data
```

---

## Current Scope

This version includes in-memory Task and Sample APIs.

PostgreSQL will be added in a later version.

---

## Data Model Draft

### Task

```text
id
title
task_type: text / audio
language
status
description
created_at
```

### Future Models

```text
Sample
Annotation
Evaluation
Review
```

---

## Tech Stack

```text
Language: Python
API Framework: FastAPI
Test Framework: pytest
HTTP Test Client: FastAPI TestClient / httpx
Future Database: PostgreSQL
Future Container Runtime: Docker
Future Orchestration: Kubernetes
Future CI/CD: GitHub Actions
```

---

## Project Structure

```text
ai-evaluation-platform
├── README.md
├── requirements.txt
├── pytest.ini
├── app
│   ├── __init__.py
│   └── main.py
└── tests
    └── test_main.py
```

---

## Run Locally

```bash
cd ~/cloud-native-korea-lab/ai-evaluation-platform

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8010
```

Open API docs:

```text
http://localhost:8010/docs
```

---

## Test

```bash
cd ~/cloud-native-korea-lab/ai-evaluation-platform

python -m pytest
```

Expected result:

```text
4 passed
```

---

## API Examples

### Health Check

```bash
curl http://localhost:8010/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Version Check

```bash
curl http://localhost:8010/version
```

Expected response:

```json
{
  "version": "0.1.0",
  "project": "ai-evaluation-platform",
  "framework": "FastAPI"
}
```

### Create Task

```bash
curl -X POST http://localhost:8010/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evaluate Korean AI Tutor response",
    "task_type": "text",
    "language": "ko",
    "description": "Check clarity, accuracy, and naturalness."
  }' | python3 -m json.tool
```

### List Tasks

```bash
curl http://localhost:8010/tasks | python3 -m json.tool
```

---

## Portfolio Message

This project demonstrates the ability to connect:

- AI data quality
- human feedback
- annotation workflows
- evaluation rubric design
- FastAPI backend development
- API testing
- PostgreSQL data modeling
- Docker containerization
- Kubernetes deployment
- CI/CD automation
- technical documentation

---

## Long-Term Direction

This project can later evolve into a real Korean AI evaluation service.

Possible future service directions:

- Korean LLM answer evaluation
- Korean speech data quality review
- AI tutor response evaluation
- human feedback dataset management
- CSV / JSON export for training data workflows

---

## Out of Scope for MVP

The first MVP will not include:

- login / signup
- payment
- complex frontend
- real user uploads
- private data handling
- large-scale model training
- streaming audio processing
- multi-tenant architecture

The goal is to build a small but complete portfolio first.

---

## Safety Rule

Do not use private, confidential, or internal company data.

Only use:

- public data
- synthetic data
- self-created samples
- properly anonymized examples
- user-consented data

---

## Next Steps

1. Add Annotation API
2. Add Evaluation API
3. Add `review_required` workflow
4. Add PostgreSQL
5. Add Dockerfile
6. Add Docker Compose
7. Add GitHub Actions CI
8. Add Kubernetes manifests
9. Write English portfolio README and architecture docs
