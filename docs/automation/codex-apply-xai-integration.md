# Codex Prompt: Apply xAI Integration to Cloud Native Korea Lab

Use this prompt in Codex to update the repository structure and connect the new xAI strategy documents to the existing README.

---

## Prompt

You are working inside the `cloud-native-korea-lab` repository.

Goal:
Integrate the xAI career roadmap and AI Evaluation Platform direction into the existing Cloud Native Korea Lab project without deleting existing work.

Important context:
- `mini-platform` is a practice sandbox.
- `ai-evaluation-platform` is the new flagship portfolio project.
- Cloud Native Korea Lab should now be positioned as a cloud-native learning and portfolio project for AI data evaluation, annotation, human feedback, and evaluation infrastructure.
- The long-term goal is portfolio first, real service next.
- The target career path is xAI AI Tutor -> AI data quality experience -> Cloud Native AI Evaluation Platform -> xAI Model team roles.

Files already added:
- `docs/career/integrated-xai-strategy.md`
- `docs/career/xai-roadmap.md`
- `docs/career/portfolio-first-service-next.md`
- `ai-evaluation-platform/README.md`
- `portfolio/xai/korean-voice-data-evaluation/README.md`

Tasks:

1. Update root `README.md`.
   - Keep the existing Cloud Native Korea Lab history.
   - Add a new section near the top called `Updated Project Direction`.
   - Explain that the project now focuses on building a Cloud Native AI Evaluation Platform.
   - Explain that `mini-platform` is a practice sandbox and `ai-evaluation-platform` is the flagship portfolio.
   - Add links to the new documents.

2. Update `Repository Structure` in `README.md`.
   - Include `docs/career/`.
   - Include `docs/automation/`.
   - Include `ai-evaluation-platform/`.
   - Include `portfolio/xai/korean-voice-data-evaluation/`.

3. Update `Current Focus`.
   - New focus should be:
     1. Finish xAI AI Tutor portfolio package.
     2. Build AI Evaluation Platform MVP.
     3. Apply Docker, PostgreSQL, Kubernetes, and GitHub Actions to the platform.
     4. Later extend the portfolio into a real service.

4. Update `Next Steps`.
   - Add these next steps:
     - Create FastAPI skeleton for `ai-evaluation-platform`.
     - Add PostgreSQL schema for tasks, samples, annotations, and evaluations.
     - Add Docker Compose for API + DB.
     - Add tests.
     - Add Kubernetes manifests.
     - Add GitHub Actions workflow.
     - Prepare Korean Voice Data Evaluation Portfolio.

5. Do not remove existing completed labs.

6. Keep the README clear for beginners.
   - Korean explanations should remain easy to understand.
   - Avoid overcomplicated wording.

7. After editing, run a quick markdown review.
   - Make sure links are correct.
   - Make sure the project direction is clear.

Expected outcome:
The repository should clearly communicate that Cloud Native Korea Lab is now a focused project combining cloud-native learning, AI evaluation infrastructure, xAI portfolio preparation, and future real service development.
