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
- `/health` : Docker, Kubernetes 상태 확인용 API
- `/version` : 앱 버전, 언어, 프레임워크 확인
- `/ask` : Cloud Native AI Docs Agent의 질문 접수 API
- `/docs` : FastAPI 자동 API 문서

현재 `/ask`는 실제 AI/RAG를 연결하기 전 단계이며, 고정된 예시 응답을 반환합니다.

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
├── portfolio
└── mini-platform
    ├── app
    │   └── main.py
    ├── requirements.txt
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
Container: Docker
Local Container Orchestration: Docker Compose
Kubernetes: Docker Desktop Kubernetes
```

---

## Completed Labs

- Node.js Mini Platform v0 실습
- Node.js 기반 `/ask` API 실습
- Node.js 버전 legacy 이동
- Python FastAPI 전환
- FastAPI `/`, `/health`, `/version`, `/ask` API 구현
- FastAPI `/docs` 자동 문서 확인
- FastAPI Docker 이미지 빌드
- FastAPI Docker Compose 실행
- FastAPI Kubernetes Deployment/Service 실행
- readinessProbe/livenessProbe 추가

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
9. Helm
10. Argo CD
11. Monitoring
12. Terraform
13. Cloud Platform

---

## Next Steps

1. README 최신화 완료
2. Kubernetes 리소스 정리 완료
3. GitHub Actions로 FastAPI 앱 테스트 자동화
4. Docker 이미지 빌드 자동화
5. Kubernetes manifest 개선
6. Helm Chart 작성
7. Argo CD GitOps 배포
8. Prometheus/Grafana 모니터링 연결
9. 공식 문서 기반 RAG 구조 설계

---

## Vision

Cloud Native Korea Lab은 한국에서 가장 초보자 친화적인 클라우드 네이티브 학습 커뮤니티를 만드는 것을 목표로 합니다.

최종 목표는 공식 문서 기반 Cloud Native AI Docs Agent를 만들고, 그 에이전트를 실제 클라우드 네이티브 방식으로 운영하면서 교육 콘텐츠와 커뮤니티를 함께 성장시키는 것입니다.
