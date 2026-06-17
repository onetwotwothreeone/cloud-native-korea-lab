# AI Evaluation Platform

## Project Role

This is the flagship portfolio project of Cloud Native Korea Lab.

The existing `mini-platform` is a practice sandbox.
This `ai-evaluation-platform` is the main portfolio project.

```text
mini-platform = practice sandbox
ai-evaluation-platform = flagship portfolio
```

## Problem Definition

AI models improve when training data, annotations, and human feedback are high quality.

However, evaluation workflows often have these problems:

- unclear quality criteria
- inconsistent human judgments
- ambiguous samples that need review
- unstructured feedback
- evaluation results that are difficult to reuse
- weak connection between human feedback and model improvement

This project builds a small cloud-native platform to manage AI data evaluation workflows.

## MVP Goal

Build a minimal but complete API system for evaluating AI training data and model outputs.

## MVP Features

1. Create evaluation tasks
2. Register text or audio sample metadata
3. Submit annotations
4. Submit quality scores
5. Mark samples as `review_required`
6. Store evaluation results in PostgreSQL
7. Expose FastAPI endpoints
8. Run locally with Docker Compose
9. Deploy to Kubernetes
10. Test with GitHub Actions

## Initial Scope

The first version focuses on text and metadata-based evaluation.
Audio file handling can be added later.

## Out of Scope for MVP

- user authentication
- payment
- complex frontend
- large-scale model training
- real user uploads
- streaming audio processing
- multi-tenant architecture

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Kubernetes
- GitHub Actions
- Kustomize later

## Suggested Data Model

### Task

- id
- title
- task_type: text / audio
- language
- status
- created_at

### Sample

- id
- task_id
- content
- transcript
- metadata
- created_at

### Annotation

- id
- sample_id
- annotator
- label
- comment
- ambiguity_flag
- created_at

### Evaluation

- id
- sample_id
- clarity_score
- naturalness_score
- accuracy_score
- context_score
- quality_score
- review_required
- reason
- created_at

## API Draft

```text
GET  /health
GET  /version
POST /tasks
GET  /tasks
POST /samples
GET  /samples/{sample_id}
POST /annotations
POST /evaluations
GET  /reviews
```

## Portfolio Message

This project demonstrates the ability to connect AI data quality, human feedback, API design, database modeling, containerization, Kubernetes deployment, CI/CD, and technical documentation.

## Long-term Service Direction

After the portfolio version is complete, this project can evolve into a real Korean AI data and model output evaluation service.

Potential service direction:

- Korean LLM answer evaluation
- Korean speech data quality review
- AI tutor answer evaluation
- human feedback dataset management
- CSV / JSON export for training data workflows

## Current Priority

1. Build a simple FastAPI MVP
2. Add PostgreSQL
3. Add Docker Compose
4. Add tests
5. Add Kubernetes manifests
6. Add GitHub Actions
7. Write English README and architecture docs
