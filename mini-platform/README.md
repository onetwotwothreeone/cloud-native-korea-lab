# Cloud Native Korea Lab Mini Platform

Cloud Native Korea Lab Mini Platform은 공식 문서 기반으로 클라우드 네이티브 질문에 쉽고 정확하게 답변하는 AI 학습 에이전트를 만드는 프로젝트입니다.

이 프로젝트는 단순한 웹 앱이 아니라, Docker, Kubernetes, Helm, Argo CD, Prometheus, Grafana, Terraform, Cloud 같은 기술을 질문하면 공식 문서를 참고해 초보자도 이해할 수 있게 설명하는 AI 에이전트를 목표로 합니다.

## Problem

클라우드 네이티브를 처음 배우는 사람은 공식 문서를 봐도 아래 문제를 자주 겪습니다.

- 문서가 영어라서 읽기 어렵다.
- 용어가 많아서 어디부터 봐야 할지 모르겠다.
- Docker, Kubernetes, CI/CD, GitOps, Monitoring, Terraform이 서로 어떻게 연결되는지 이해하기 어렵다.
- 실습 중 에러가 나도 공식 문서에서 어떤 부분을 봐야 할지 모르겠다.

## Solution

Cloud Native Korea Lab Mini Platform은 사용자의 클라우드 네이티브 질문을 받고, 공식 문서를 기준으로 아래 형식으로 답변하는 AI 학습 에이전트가 되는 것을 목표로 합니다.

1. 핵심 요약
2. 12살도 이해할 수 있는 쉬운 비유
3. 공식 문서 기반의 정확한 설명
4. Mini Platform 완성에서의 역할
5. 실습 명령어
6. 자주 발생하는 에러와 해결법
7. 네이버 카페 공유용 짧은 글

## Operating Principle

> 이 기술이 Mini Platform 완성에 어떤 역할을 하지?

> 12살도 이해할 수 있을 만큼 쉽게 설명하되, 개념은 정확하게 설명한다.

앞으로 Docker, Docker Compose, Kubernetes, Helm, GitHub Actions, Argo CD, Prometheus, Grafana, Terraform, Cloud를 공부할 때마다 위 질문을 기준으로 학습합니다.

설명은 쉬운 비유와 실습 예시를 사용하되, 실제 기술의 역할과 한계는 정확하게 기록합니다.

## Goal

공식 문서를 참고해서 클라우드 네이티브 전문 지식을 쉽고 정확하게 답변하는 AI 에이전트를 만들고, 그 에이전트 자체를 클라우드 네이티브 방식으로 운영합니다.

```text
Cloud Native Question
→ Official Docs Reference
→ AI Agent Answer
→ Easy Explanation
→ Lab Example
→ Community Content
```

운영 방식은 아래처럼 단계적으로 발전시킵니다.

```text
Local Agent App
→ Docker Image
→ Docker Container
→ Docker Compose
→ Kubernetes
→ Helm
→ GitHub Actions
→ Argo CD
→ Prometheus / Grafana
→ Terraform
→ Cloud Deployment
```

## v0.1 Features

- `/` : 에이전트 소개 페이지
- `/health` : 애플리케이션 상태 확인
- `/version` : 현재 버전 확인
- `/ask` : 클라우드 네이티브 질문을 받는 API로 확장 예정

## Directory Structure

```text
mini-platform
├── README.md
├── app
│   ├── package.json
│   └── server.js
├── docker
│   └── Dockerfile
├── compose
│   └── docker-compose.yml
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
├── helm
├── cicd
├── gitops
├── monitoring
└── terraform
```

## Future Structure

AI 에이전트 기능이 추가되면 아래 구조로 확장합니다.

```text
mini-platform
├── agent
│   ├── prompt.md
│   ├── system-rules.md
│   └── answer-template.md
├── docs-sources
│   ├── docker.md
│   ├── kubernetes.md
│   ├── helm.md
│   ├── argocd.md
│   ├── prometheus.md
│   ├── grafana.md
│   └── terraform.md
└── rag
    ├── ingest.md
    ├── retrieval.md
    └── citations.md
```

## Learning Connection

- Docker Image: AI 에이전트를 어디서든 실행 가능한 패키지로 만들기
- Docker Container: AI 에이전트를 실제로 실행하기
- Docker Compose: 로컬에서 에이전트 실행 구조 관리하기
- Kubernetes: 에이전트를 클러스터에서 운영하기
- Helm: Kubernetes 설정을 패키지로 관리하기
- GitHub Actions: 빌드와 테스트 자동화하기
- Argo CD: Git 기준으로 배포 상태 유지하기
- Prometheus / Grafana: 에이전트 상태 관찰하기
- Terraform: 클라우드 인프라를 코드로 만들기

## Final Vision

클라우드 네이티브를 설명하는 AI를 클라우드 네이티브 방식으로 운영합니다.
