# Cloud Native Korea Lab

Cloud Native Korea Lab은 클라우드 네이티브 학습, FastAPI 실습, AI 데이터 평가 플랫폼 구축, 그리고 xAI 커리어 준비를 하나의 흐름으로 연결하는 학습형 포트폴리오 저장소입니다.

처음에는 Python FastAPI 기반의 Cloud Native AI Docs Agent를 만들고 Docker, Docker Compose, Kubernetes, CI/CD를 실습하는 저장소로 시작했습니다. 이제는 그 실습 경험을 바탕으로 `ai-evaluation-platform`이라는 대표 포트폴리오를 만들어 가는 방향으로 확장합니다.

쉽게 말하면, 이 저장소의 방향은 다음과 같습니다.

```text
클라우드 네이티브 기초 실습
→ FastAPI mini-platform으로 연습
→ AI 데이터 평가 플랫폼 구축
→ 한국어 AI 평가 서비스 가능성 검증
→ xAI AI Tutor 및 Model team 준비
```

---

## Project Identity

```text
mini-platform = practice sandbox
ai-evaluation-platform = flagship portfolio
```

`mini-platform`은 최종 제품이 아니라 연습장입니다. FastAPI, Docker, Kubernetes, CI/CD 같은 기본기를 작게 실험하고 익히는 공간입니다.

`ai-evaluation-platform`은 이 저장소의 대표 포트폴리오입니다. AI 학습 데이터, 어노테이션, 사람의 피드백, 품질 점수, 리뷰 워크플로우를 FastAPI, PostgreSQL, Docker, Kubernetes, GitHub Actions로 연결하는 것을 목표로 합니다.

---

## Main Direction

Cloud Native Korea Lab의 새 통합 방향은 다음 질문에 답하는 것입니다.

> 이 실습이 AI 데이터 평가, 클라우드 네이티브 인프라, xAI 준비에 어떤 증거가 되는가?

기존 실습은 삭제하지 않습니다. 이미 완료한 실습들은 학습 기록이자 포트폴리오의 기반입니다. 앞으로는 그 기반 위에 `ai-evaluation-platform`을 중심 프로젝트로 쌓아 갑니다.

---

## Top-down Completion Principle

Cloud Native Korea Lab은 프로젝트 완성을 목표로 출발하는 Top-down 방식으로 진행합니다.

먼저 완성해야 할 결과물을 정의하고, 그 결과물을 만들기 위해 필요한 기능, 기술, 실습, 문서를 역순으로 정리합니다.

```text
완성된 AI Evaluation Platform
→ 필요한 MVP 기능
→ 필요한 API와 데이터 모델
→ 필요한 인프라와 자동화
→ 필요한 클라우드 네이티브 실습
→ 오늘 해야 할 작은 작업
```

따라서 Docker, Kubernetes, PostgreSQL, CI/CD, Helm, Argo CD, Monitoring, Terraform, Cloud는 따로따로 외우는 대상이 아니라, `ai-evaluation-platform` 완성에 필요한 도구로 학습합니다.

모든 프로젝트 판단 기준은 다음 문장입니다.

> 이 작업이 xAI 지원용 포트폴리오 완성 또는 실제 한국어 AI 평가 서비스화에 도움이 되는가?

도움이 되면 진행하고, 도움이 약하면 보류합니다.

---

## Current Core Projects

### 1. mini-platform

`mini-platform`은 FastAPI와 클라우드 네이티브 배포 흐름을 연습하는 샌드박스입니다.

현재 구현된 API는 다음과 같습니다.

```text
GET  /
GET  /health
GET  /version
POST /ask
GET  /docs
```

- `/` : 기본 홈 응답
- `/health` : Docker, Kubernetes, readinessProbe, livenessProbe 상태 확인용 API
- `/version` : 앱 버전, 언어, 프레임워크 확인
- `/ask` : Cloud Native AI Docs Agent의 질문 접수 API
- `/docs` : FastAPI 자동 API 문서

현재 `/ask`는 실제 AI/RAG를 연결하기 전 단계이며, 고정된 예시 응답을 반환합니다.

### 2. ai-evaluation-platform

`ai-evaluation-platform`은 이 저장소의 대표 포트폴리오입니다.

목표는 AI 모델 학습과 개선에 필요한 평가 흐름을 작고 명확한 API 시스템으로 만드는 것입니다.

초기 MVP는 다음 기능을 목표로 합니다.

1. 평가 작업 생성
2. 텍스트 또는 오디오 샘플 메타데이터 등록
3. 어노테이션 제출
4. 품질 점수 제출
5. `review_required` 샘플 표시
6. PostgreSQL에 평가 결과 저장
7. FastAPI 엔드포인트 제공
8. Docker Compose로 로컬 실행
9. Kubernetes로 배포
10. GitHub Actions로 테스트

이 프로젝트는 단순한 CRUD 연습이 아니라, AI 데이터 품질과 사람의 피드백을 어떻게 구조화할 수 있는지 보여주는 포트폴리오입니다.

---

## Strategy Documents

새 방향은 아래 문서들에 정리되어 있습니다.

- [Integrated xAI Strategy](docs/career/integrated-xai-strategy.md)
- [xAI Roadmap](docs/career/xai-roadmap.md)
- [Portfolio First, Service Next](docs/career/portfolio-first-service-next.md)
- [AI Evaluation Platform README](ai-evaluation-platform/README.md)

---

## Repository Structure

```text
cloud-native-korea-lab
├── README.md
├── .python-version
├── .github
│   └── workflows
│       └── fastapi-ci.yml
├── docs
│   └── career
│       ├── integrated-xai-strategy.md
│       ├── xai-roadmap.md
│       └── portfolio-first-service-next.md
├── ai-evaluation-platform
│   └── README.md
├── roadmap
├── labs
│   ├── week-01-linux-git
│   ├── week-02-network
│   ├── week-03-docker
│   ├── week-04-python-fastapi
│   ├── week-05-kubernetes
│   ├── week-06-ai-docs-agent
│   └── legacy
│       └── node-mini-platform-v0
├── error-logs
├── notes
├── content
├── career
├── portfolio
└── mini-platform
    ├── README.md
    ├── app
    │   ├── __init__.py
    │   └── main.py
    ├── tests
    │   └── test_main.py
    ├── requirements.txt
    ├── pytest.ini
    ├── Dockerfile
    ├── .dockerignore
    ├── compose
    │   └── docker-compose.yml
    └── k8s
        ├── deployment.yaml
        └── service.yaml
```

---

## Current Stack

```text
Language: Python 3.13.13
API Framework: FastAPI
ASGI Server: Uvicorn
Database: PostgreSQL for ai-evaluation-platform
Test: pytest, httpx, FastAPI TestClient
Container: Docker
Local Container Orchestration: Docker Compose
Kubernetes: Docker Desktop Kubernetes
CI: GitHub Actions
```

---

## Completed Labs

- Node.js Mini Platform v0 실습
- Node.js 기반 `/ask` API 실습
- Node.js 버전 legacy 이동
- Python FastAPI 전환
- FastAPI `/`, `/health`, `/version`, `/ask` API 구현
- FastAPI `/docs` 자동 문서 확인
- pytest 기반 로컬 테스트 준비
- FastAPI Docker 이미지 빌드
- FastAPI Docker Compose 실행
- FastAPI Kubernetes Deployment/Service 실행
- readinessProbe/livenessProbe 추가
- GitHub Actions로 FastAPI 테스트 자동화
- GitHub Actions로 Docker 이미지 빌드 자동화
- 루트 README와 mini-platform README 최신화
- Cloud Native Career Guide 문서 추가
- Company Tech Notes 기반 커리어 리서치 템플릿 추가

---

## Learning Direction

학습 방향은 기존 클라우드 네이티브 기초를 유지하면서, AI 평가 플랫폼에 필요한 기술로 연결합니다.

1. Linux & Git
2. Network
3. Python & FastAPI
4. Docker
5. Docker Compose
6. Kubernetes
7. Kubernetes Health Check
8. CI/CD
9. PostgreSQL
10. API design for evaluation workflows
11. Kubernetes ConfigMap / Secret
12. Helm
13. Argo CD
14. Monitoring
15. Terraform
16. Cloud Platform
17. Official Docs-based RAG
18. AI data evaluation and annotation workflow
19. Korean voice/text evaluation portfolio
20. Cloud Native Career Guide
21. Company Tech Notes Research

---

## Career and Portfolio Direction

Cloud Native Korea Lab은 학습과 실습을 실제 커리어 준비와 연결합니다.

목표 포지셔닝은 다음과 같습니다.

```text
Korean AI Data & Evaluation Builder
with Cloud Native Infrastructure Skills
```

이 저장소는 다음 경험을 하나로 연결합니다.

- 한국어 튜터링 경험
- 한국어 음성/텍스트 평가 역량
- FastAPI 기반 API 설계
- PostgreSQL 데이터 모델링
- Docker와 Kubernetes 운영 실습
- GitHub Actions 기반 CI/CD
- AI 데이터 품질, 어노테이션, 사람의 피드백 이해
- xAI AI Tutor 및 Model team 준비

---

## Current Focus

현재 집중할 것은 `ai-evaluation-platform`을 작지만 완성도 있는 포트폴리오 MVP로 만드는 것입니다.

우선순위는 다음과 같습니다.

1. `ai-evaluation-platform`의 FastAPI MVP 만들기
2. PostgreSQL 데이터 모델 추가하기
3. Docker Compose로 로컬 실행 가능하게 만들기
4. 테스트 추가하기
5. Kubernetes manifest 작성하기
6. GitHub Actions로 테스트 자동화하기
7. README, 아키텍처 문서, 문제 정의 문서 정리하기

`mini-platform`에서 배운 것은 버리지 않습니다. 대신 그 경험을 `ai-evaluation-platform`에 적용합니다.

---

## Next Steps

1. `ai-evaluation-platform` FastAPI 프로젝트 구조 만들기
2. Task, Sample, Annotation, Evaluation 데이터 모델 설계
3. `/health`, `/version`, `/tasks`, `/samples`, `/annotations`, `/evaluations`, `/reviews` API 초안 구현
4. PostgreSQL 연결
5. Docker Compose 실행 환경 추가
6. pytest 기반 테스트 추가
7. Kubernetes 배포 manifest 작성
8. GitHub Actions CI 추가
9. 영어 README와 아키텍처 문서 작성
10. 한국어 음성/텍스트 평가 예시 데이터 준비
11. 포트폴리오 먼저 완성한 뒤, 실제 한국어 AI 평가 서비스 가능성 검토

---

## Vision

Cloud Native Korea Lab은 초보자 친화적인 클라우드 네이티브 학습 기록에서 출발해, AI 데이터 평가와 사람의 피드백을 다루는 실전형 포트폴리오로 성장하는 프로젝트입니다.

최종 목표는 단순히 실습을 많이 하는 것이 아닙니다. 클라우드 네이티브 방식으로 AI 평가 플랫폼을 만들고, 그 과정을 통해 기술력, 제품 사고, 운영 습관을 함께 증명하는 것입니다.

## 35.2. HYEAN/GWAN Prevention Layer Alignment

This step aligns the current GWAN Kubernetes implementation with the updated Prevention Layer project source.

HYEAN/GWAN is not only a response system.

It is a prevention-oriented survival intelligence architecture.

GWAN should later expand beyond current risk scoring and include:

- trend_score
- imbalance_score
- early_warning_score
- recovery_capacity
- preventive_action_priority

This means Kubernetes work should be explained as preventive operational infrastructure.

Examples:

- HPA supports changing demand.
- HPA behavior policy prevents unstable scaling.
- PDB protects availability during voluntary disruption.
- NetworkPolicy will prevent unnecessary Pod communication risk.

Next step:

36_GWAN_Kubernetes_NetworkPolicy_Baseline

## 36. GWAN Kubernetes NetworkPolicy Baseline

This step adds baseline Kubernetes NetworkPolicy rules for GWAN.

NetworkPolicy is preventive communication control.

For HYEAN/GWAN, this means unnecessary Pod communication paths are reduced before they become operational risk paths.

Baseline:

- GWAN API allows ingress on TCP 8000.
- GWAN API allows egress to PostgreSQL on TCP 5432.
- GWAN API allows DNS egress on TCP/UDP 53.
- GWAN PostgreSQL allows ingress only from GWAN API on TCP 5432.

Important:

NetworkPolicy enforcement depends on the Kubernetes CNI plugin.
Local Docker Desktop or kind may create NetworkPolicy objects even if actual packet blocking is not enforced.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/network_policy_check.sh

## 37. GWAN Kubernetes ServiceAccount RBAC Baseline

This step adds dedicated Kubernetes ServiceAccounts and minimal RBAC baseline for GWAN.

ServiceAccount is the workload identity.
RBAC is the permission rule.

For HYEAN/GWAN, RBAC is preventive identity control.

Baseline:

- GWAN API uses gwan-api-sa.
- PostgreSQL uses gwan-postgres-sa.
- ServiceAccount token automount is false.
- Minimal Roles have no Kubernetes API permissions.

Check commands:

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/rbac_check.sh

