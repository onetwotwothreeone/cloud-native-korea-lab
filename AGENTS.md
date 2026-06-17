# AGENTS.md

## Project

This repository is `Cloud Native Korea Lab`.

The project combines cloud-native learning, AI data evaluation infrastructure, xAI portfolio preparation, and future real service development.

## Core Direction

```text
Cloud Native learning
  -> xAI AI Tutor portfolio
  -> AI Evaluation Platform
  -> real Korean AI evaluation service
  -> xAI Model team readiness
```

## Project Identity

```text
mini-platform = practice sandbox
ai-evaluation-platform = flagship portfolio
```

Do not treat `mini-platform` as the final product.
Use it as a learning sandbox and apply the learned patterns to `ai-evaluation-platform`.

## Main Priority

When working in this repository, prioritize the following order:

1. Keep existing labs and learning history safe.
2. Build and document `ai-evaluation-platform` as the flagship portfolio.
3. Connect every change to xAI readiness or real service potential.
4. Keep explanations beginner-friendly but technically accurate.
5. Prefer small, testable, well-documented changes.

## Target Portfolio Message

The repository should communicate this message:

> I am building a cloud-native AI evaluation platform that connects human feedback, annotation workflows, data quality, FastAPI, PostgreSQL, Docker, Kubernetes, CI/CD, and future real service development.

## Coding Guidelines

- Use Python and FastAPI for backend work.
- Keep APIs simple and explicit.
- Prefer readable code over clever code.
- Add tests for new functionality when practical.
- Keep README files updated when adding features.
- Do not introduce unnecessary frontend complexity in the MVP.
- Do not add authentication, payment, or multi-tenant features until the MVP is complete.

## Documentation Guidelines

Every meaningful change should update at least one of these:

- README.md
- `ai-evaluation-platform/README.md`
- architecture document
- learning note
- error log
- portfolio write-up

## AI Evaluation Platform MVP Scope

Initial MVP features:

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

## Out of Scope for MVP

Do not implement these in the first MVP unless explicitly requested:

- complex frontend
- login / signup
- payment
- production user upload
- large-scale model training
- streaming audio processing
- multi-tenant architecture

## Safety and Confidentiality

If the owner later works with xAI or another AI company, do not use private, confidential, or internal company data in this public repository.

Use only:

- public data
- synthetic data
- self-created samples
- properly anonymized examples
- user-consented data

## Test and Validation

When changing code, run relevant tests when possible.

Recommended commands may include:

```bash
python -m pytest
```

For Docker work:

```bash
docker compose up --build
```

For Kubernetes work:

```bash
kubectl apply -f <manifest>
kubectl get pods
kubectl logs <pod-name>
```

## Response Style for Codex

When finishing a task, summarize:

1. What changed
2. Why it changed
3. Files touched
4. Tests or checks run
5. Next recommended step
