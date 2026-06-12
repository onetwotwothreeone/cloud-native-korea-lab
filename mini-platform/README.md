# FastAPI Mini Platform

FastAPI Mini Platform은 Cloud Native Korea Lab의 핵심 실습 프로젝트입니다.

이 프로젝트의 목표는 Python FastAPI 기반의 Cloud Native AI Docs Agent를 만들고, 이를 Docker, Docker Compose, Kubernetes, GitHub Actions, GitOps, Monitoring, Terraform, Cloud 배포까지 단계적으로 운영해보는 것입니다.

최종 목표는 클라우드 네이티브 질문에 대해 공식 문서를 참고하여 초보자도 이해할 수 있게 쉽고 정확하게 답변하는 AI Docs Agent를 만드는 것입니다.

---

## Project Identity

```text
클라우드 네이티브를 설명하는 AI를
클라우드 네이티브 방식으로 운영한다.
```

현재 단계에서는 실제 AI/RAG를 연결하기 전, FastAPI 기반 API 구조와 운영 기반을 먼저 만듭니다.

---

## Operating Principle

> 이 기술이 Mini Platform 완성에 어떤 역할을 하지?

> 12살도 이해할 수 있을 만큼 쉽게 설명하되, 개념은 정확하게 설명한다.

모든 실습은 단순히 명령어를 실행하는 것이 아니라, FastAPI Mini Platform을 실제 운영 가능한 Cloud Native AI Docs Agent로 발전시키는 흐름에 연결합니다.

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

## Implemented API

```text
GET  /
GET  /health
GET  /version
POST /ask
GET  /docs
```

### `/`
기본 홈 응답을 반환합니다.

### `/health`
Docker, Kubernetes, readinessProbe, livenessProbe에서 앱 상태를 확인하기 위한 API입니다.

### `/version`
앱 버전, 언어, 프레임워크 정보를 반환합니다.

### `/ask`
Cloud Native AI Docs Agent의 질문 접수 API입니다.

현재는 실제 AI/RAG를 연결하기 전 단계이며, 고정된 예시 응답을 반환합니다.

### `/docs`
FastAPI가 자동으로 제공하는 API 문서입니다.

---

## Directory Structure

```text
mini-platform
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

## Completed Labs

- Python FastAPI 기반 Mini Platform 전환
- FastAPI `/`, `/health`, `/version`, `/ask` API 구현
- FastAPI `/docs` 자동 문서 확인
- pytest 기반 로컬 테스트 준비
- Docker 이미지 빌드
- Docker Compose 실행
- Kubernetes Deployment/Service 배포
- readinessProbe/livenessProbe 추가
- GitHub Actions로 FastAPI 테스트 자동화
- GitHub Actions로 Docker 이미지 빌드 자동화

---

## Local Run

```bash
cd mini-platform
uvicorn app.main:app --reload
```

확인:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/version
```

---

## Test

```bash
cd mini-platform
python -m pytest
```

현재 테스트 대상:

```text
/health
/version
/ask
```

---

## Docker Run

```bash
cd mini-platform
docker build -t cnkl-fastapi-mini-platform:0.1.0 .
docker run --rm -p 8001:8000 cnkl-fastapi-mini-platform:0.1.0
```

확인:

```bash
curl http://localhost:8001/health
```

---

## Docker Compose Run

```bash
cd mini-platform/compose
docker compose up -d --build
```

확인:

```bash
curl http://localhost:8001/health
```

정리:

```bash
docker compose down
```

---

## Kubernetes Run

```bash
kubectl apply -f mini-platform/k8s/deployment.yaml
kubectl apply -f mini-platform/k8s/service.yaml
kubectl get pods
kubectl get svc
```

port-forward:

```bash
kubectl port-forward svc/fastapi-mini-platform-service 8001:80
```

확인:

```bash
curl http://localhost:8001/health
```

---

## GitHub Actions

`.github/workflows/fastapi-ci.yml`에서 다음 작업을 자동화합니다.

```text
1. FastAPI 테스트 실행
2. Docker 이미지 빌드 확인
```

현재 CI 흐름:

```text
push / pull_request
→ Python 3.13 설정
→ requirements.txt 설치
→ python -m pytest
→ docker build
```

---

## Next Steps

1. README와 실습 기록 정리
2. Docker 이미지 빌드 자동화 결과 확인
3. Kubernetes manifest 개선
4. ConfigMap / Secret 적용
5. Helm Chart 작성
6. Argo CD GitOps 배포
7. Prometheus / Grafana 모니터링 연결
8. 공식 문서 기반 RAG 구조 설계
9. 실제 AI 응답 연결

---

## Learning Connection

- FastAPI: AI Docs Agent의 API 서버
- `/ask`: 사용자의 클라우드 네이티브 질문을 받는 입구
- `/health`: Kubernetes가 앱 상태를 확인하는 기준
- Docker: FastAPI 앱을 어디서든 실행 가능한 이미지로 포장
- Docker Compose: 로컬 실행 구조 관리
- Kubernetes: 앱을 운영 환경처럼 배포하고 관리
- readinessProbe/livenessProbe: 앱이 요청을 받을 준비가 되었는지, 살아 있는지 자동 확인
- GitHub Actions: 테스트와 빌드를 자동화
- Helm: Kubernetes 설정을 패키지화
- Argo CD: Git 기준으로 배포 상태 유지
- Prometheus / Grafana: 앱 상태 관찰
- Terraform: 클라우드 인프라를 코드로 관리

---

## Vision

FastAPI Mini Platform은 단순한 예제 앱이 아니라, 공식 문서 기반 Cloud Native AI Docs Agent로 발전하기 위한 시작점입니다.

이 프로젝트를 통해 클라우드 네이티브를 직접 실습하고, 그 과정을 한국어 교육 콘텐츠와 커뮤니티 자료로 전환합니다.
