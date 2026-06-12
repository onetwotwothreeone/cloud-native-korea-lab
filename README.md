# Cloud Native Korea Lab

Cloud Native Korea Lab은 공식 문서 기반 Cloud Native AI Docs Agent를 만들고, 그 에이전트를 Docker, Kubernetes, CI/CD, GitOps, Monitoring, Terraform으로 운영하면서 초보자도 쉽게 따라올 수 있는 한국어 클라우드 네이티브 교육 콘텐츠와 커뮤니티를 만드는 프로젝트입니다.

## 목적

- 공식 문서 기반 Cloud Native AI Docs Agent 만들기
- Docker, Kubernetes, CI/CD, GitOps, Monitoring, Terraform을 프로젝트 중심으로 학습하기
- 클라우드 네이티브 전문 지식을 12살도 이해할 수 있을 만큼 쉽게 설명하되, 개념은 정확하게 정리하기
- 실습 중심의 학습 기록 관리
- 에러 해결 과정을 문서화하고 커뮤니티 학습 자료로 전환하기
- 네이버 카페 공유용 콘텐츠 제작
- 포트폴리오로 활용 가능한 프로젝트 기록 축적
- 최종적으로 한국에서 가장 초보자 친화적인 클라우드 네이티브 교육 커뮤니티로 성장하기

## Project Identity

Cloud Native Korea Lab의 핵심 프로젝트는 `mini-platform`입니다.

`mini-platform`은 단순한 작은 웹 앱이 아니라, 클라우드 네이티브 질문에 대해 공식 문서를 참고하여 쉽고 정확하게 답변하는 AI Docs Agent입니다.

이 프로젝트의 핵심 문장은 다음과 같습니다.

```text
클라우드 네이티브를 설명하는 AI를
클라우드 네이티브 방식으로 운영한다.
```

## Operating Principle

> 이 기술이 Mini Platform 완성에 어떤 역할을 하지?

> 12살도 이해할 수 있을 만큼 쉽게 설명하되, 개념은 정확하게 설명한다.

앞으로 모든 기술 학습은 단순 개념 암기가 아니라, Cloud Native Korea Lab Mini Platform을 완성하는 데 어떤 역할을 하는지 기준으로 연결합니다.

설명은 항상 초보자도 이해할 수 있게 쉽게 풀어 쓰되, Docker, Kubernetes, CI/CD, GitOps, Monitoring, Terraform, Cloud의 정확한 의미와 역할은 흐리지 않습니다.

## Repository Structure

```text
cloud-native-korea-lab
├── README.md
├── roadmap
├── labs
│   ├── week-01-linux-git
│   ├── week-02-network
│   ├── week-03-docker
│   └── week-04-docker-compose
├── error-logs
├── notes
├── content
├── portfolio
└── mini-platform
    ├── app
    ├── agent
    ├── docs-sources
    ├── rag
    ├── docker
    ├── compose
    ├── k8s
    ├── helm
    ├── cicd
    ├── gitops
    ├── monitoring
    └── terraform
```

## Folders

### roadmap
학습 로드맵, 주차별 계획, 커뮤니티 운영 계획을 정리합니다.

### labs
주차별 실습 결과물을 기록합니다.

### error-logs
실습 중 만난 에러와 해결 방법을 정리합니다.

### notes
공부하면서 정리한 개념 노트를 저장합니다.

### content
네이버 카페 업로드용 글감과 커뮤니티 콘텐츠 초안을 저장합니다.

### portfolio
실습 내용을 포트폴리오 형식으로 정리합니다.

### mini-platform
공식 문서 기반 Cloud Native AI Docs Agent를 관리합니다. 이 에이전트는 사용자의 클라우드 네이티브 질문을 받고, 공식 문서를 참고해 핵심 요약, 쉬운 비유, 정확한 설명, 실습 예시, 에러 해결, 커뮤니티 공유용 글로 답변하는 것을 목표로 합니다.

### mini-platform/app
AI Docs Agent의 API 서버와 애플리케이션 코드를 관리합니다.

### mini-platform/agent
AI 에이전트의 역할, 답변 규칙, 답변 템플릿을 관리합니다.

### mini-platform/docs-sources
Docker, Kubernetes, Helm, Argo CD, Prometheus, Grafana, Terraform, Cloud 공식 문서 소스 목록을 관리합니다.

### mini-platform/rag
공식 문서를 수집하고, 질문과 관련된 문서를 찾고, 답변에 출처를 연결하는 RAG 구조를 관리합니다.

### mini-platform/docker
AI Docs Agent를 Docker 이미지로 만들기 위한 Dockerfile을 관리합니다.

### mini-platform/compose
로컬 환경에서 AI Docs Agent를 실행하기 위한 Docker Compose 설정을 관리합니다.

### mini-platform/k8s
Kubernetes에서 AI Docs Agent를 실행하기 위한 Deployment, Service 등 Manifest를 관리합니다.

### mini-platform/helm
Kubernetes 설정을 패키지로 관리하기 위한 Helm Chart를 관리합니다.

### mini-platform/cicd
GitHub Actions 등 CI/CD 자동화 설정을 관리합니다.

### mini-platform/gitops
Argo CD 기반 GitOps 배포 설정을 관리합니다.

### mini-platform/monitoring
Prometheus와 Grafana 기반 모니터링 설정을 관리합니다.

### mini-platform/terraform
클라우드 인프라를 코드로 관리하기 위한 Terraform 설정을 관리합니다.

## Learning Direction

1. Linux & Git
2. Network
3. Docker
4. Docker Compose
5. Kubernetes
6. CI/CD
7. Helm
8. Argo CD
9. Prometheus / Grafana Monitoring
10. Terraform
11. Cloud Platform
12. Figma-based Design and Visualization
13. iOS App Experience and Mobile Distribution

## Tool Usage

- ChatGPT: 학습 코치, 기획, 설명, 콘텐츠화
- GitHub: 코드와 실습 기록 저장소
- Google Drive: 문서 보관소
- Google Calendar / Tasks: 학습 루틴 관리
- Naver Cafe: 커뮤니티 본점
- Figma: AI Docs Agent 화면 설계, 구조도, 카드뉴스 제작
- iOS Developer / Apple Developer: AI Docs Agent의 iPhone 앱 확장, 모바일 학습 경험 설계, 테스트 배포 준비
- Docker: AI Docs Agent를 컨테이너로 포장하고 실행
- Kubernetes: AI Docs Agent를 운영 환경에서 관리
- GitHub Actions: 빌드와 테스트 자동화
- Argo CD: GitOps 방식의 배포 상태 관리
- Prometheus / Grafana: 에이전트 상태 관찰
- Terraform: 클라우드 인프라 코드화

## Current Focus

현재 집중할 것은 Cloud Native AI Docs Agent v0.1을 만드는 것입니다.

첫 번째 구현 목표는 `/ask` API입니다.

```text
User Question
→ /ask API
→ Answer Template
→ Beginner-friendly Explanation
→ Official Docs Reference
→ Community Content
```

처음부터 완전한 AI/RAG 시스템을 만들기보다, 먼저 질문을 받고 정해진 답변 템플릿으로 응답하는 구조를 만든 뒤, 공식 문서 검색과 RAG 구조를 단계적으로 붙입니다.

## Future Mobile Direction

Cloud Native AI Docs Agent는 먼저 웹/API 기반으로 만들고, 이후 iOS 앱으로 확장할 수 있습니다.

모바일 확장 목표는 사용자가 iPhone에서 클라우드 네이티브 질문을 입력하고, 공식 문서 기반의 쉬운 설명과 실습 예시를 바로 확인할 수 있는 학습 경험을 만드는 것입니다.

```text
Web/API Agent
→ Figma Mobile Wireframe
→ iOS Learning App Prototype
→ Test Distribution
→ Community Feedback
```

## Vision

한국에서 가장 초보자 친화적인 클라우드 네이티브 학습 커뮤니티를 만드는 것을 목표로 합니다.

최종적으로는 공식 문서 기반 Cloud Native AI Docs Agent를 통해 초보자가 Docker, Kubernetes, CI/CD, GitOps, Monitoring, Terraform, Cloud를 실습 중심으로 배우고, 에러 해결과 포트폴리오 제작까지 이어갈 수 있도록 돕습니다.
