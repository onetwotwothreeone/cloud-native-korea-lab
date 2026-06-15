# Cloud Native Korea Lab

Cloud Native Korea Lab은 Python FastAPI 기반의 Cloud Native AI Docs Agent를 만들고, 이를 Docker, Docker Compose, Kubernetes, CI/CD, GitOps, Monitoring, Terraform, Cloud 배포까지 단계적으로 운영해보는 학습 Repository입니다.

목표는 클라우드 네이티브를 실습 중심으로 공부하면서, 초보자도 쉽게 따라올 수 있는 한국어 교육 콘텐츠와 커뮤니티 자료를 함께 만드는 것입니다.

---

## 현재 핵심 프로젝트

### FastAPI Mini Platform

현재 Mini Platform은 Python FastAPI 기반입니다.

구현된 API는 다음과 같습니다.

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

---

## Project Identity

```text
클라우드 네이티브를 설명하는 AI를
클라우드 네이티브 방식으로 운영한다.
```

---

## Operating Principle

> 이 기술이 Mini Platform 완성에 어떤 역할을 하지?

> 12살도 이해할 수 있을 만큼 쉽게 설명하되, 개념은 정확하게 설명한다.

모든 기술 학습은 단순 개념 암기가 아니라, FastAPI Mini Platform을 실제 운영 가능한 Cloud Native AI Docs Agent로 발전시키는 흐름에 연결합니다.

---

## Repository Structure

```text
cloud-native-korea-lab
├── README.md
├── .python-version
├── .github
│   └── workflows
│       └── fastapi-ci.yml
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
│   ├── README.md
│   ├── jobs
│   │   └── job-curation-template.md
│   ├── certifications
│   │   └── cloud-native-certification-roadmap.md
│   ├── roles
│   │   └── cloud-native-role-map.md
│   └── portfolio-checklist.md
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

---

## Learning Direction

1. Linux & Git
2. Network
3. Python & FastAPI
4. Docker
5. Docker Compose
6. Kubernetes
7. Kubernetes Health Check
8. CI/CD
9. Kubernetes ConfigMap / Secret
10. Helm
11. Argo CD
12. Monitoring
13. Terraform
14. Cloud Platform
15. Official Docs-based RAG
16. Cloud Native Career Guide

---

## Career Guide

Cloud Native Korea Lab은 학습과 실습을 실제 커리어 준비와 연결합니다.

커리어 가이드는 아래 흐름을 기준으로 운영합니다.

```text
채용공고 요구 기술
→ 배워야 할 개념
→ 해볼 실습
→ GitHub 포트폴리오 증거
→ 커뮤니티 설명 글
```

현재 추가된 문서는 다음과 같습니다.

- `career/README.md` : 커리어 가이드 전체 개요
- `career/jobs/job-curation-template.md` : 채용공고 큐레이션 템플릿
- `career/certifications/cloud-native-certification-roadmap.md` : 자격증 로드맵
- `career/roles/cloud-native-role-map.md` : 클라우드 네이티브 직무 지도
- `career/portfolio-checklist.md` : 포트폴리오 점검표

---

## Current Focus

현재 집중할 것은 GitHub Actions로 자동화된 테스트와 Docker 이미지 빌드 흐름을 안정적으로 기록하고, Kubernetes 운영 설정을 다음 단계로 확장하는 것입니다.

현재 CI 흐름은 다음과 같습니다.

```text
push / pull_request
→ Python 3.13 설정
→ requirements.txt 설치
→ python -m pytest
→ docker build
```

---

## Next Steps

1. GitHub Actions 실행 결과 확인 및 실습 기록 정리
2. Kubernetes ConfigMap / Secret 적용
3. Kubernetes manifest 개선
4. Helm Chart 작성
5. Argo CD GitOps 배포
6. Prometheus / Grafana 모니터링 연결
7. 공식 문서 기반 RAG 구조 설계
8. 실제 AI 응답 연결
9. Cloud 배포 구조 설계
10. Cloud Native Career Guide를 네이버 카페 콘텐츠와 연결

---

## Vision

Cloud Native Korea Lab은 한국에서 가장 초보자 친화적인 클라우드 네이티브 학습 커뮤니티를 만드는 것을 목표로 합니다.

최종 목표는 공식 문서 기반 Cloud Native AI Docs Agent를 만들고, 그 에이전트를 실제 클라우드 네이티브 방식으로 운영하면서 교육 콘텐츠와 커뮤니티를 함께 성장시키는 것입니다.
