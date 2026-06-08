# Cloud Native Korea Lab Mini Platform

Cloud Native Korea Lab Mini Platform은 클라우드 네이티브 기술을 프로젝트 중심으로 학습하기 위한 작은 웹 애플리케이션입니다.

## Operating Principle

> 이 기술이 Mini Platform 완성에 어떤 역할을 하지?

앞으로 Docker, Docker Compose, Kubernetes, Helm, GitHub Actions, Argo CD, Prometheus, Grafana, Terraform, Cloud를 공부할 때마다 위 질문을 기준으로 학습합니다.

## Goal

아주 작은 웹 앱을 만들고, 이를 단계적으로 클라우드 네이티브 방식으로 발전시킵니다.

```text
Local App
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

- `/` : 메인 페이지
- `/health` : 애플리케이션 상태 확인
- `/version` : 현재 버전 확인

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

## Learning Connection

- Docker Image: 앱을 어디서든 실행 가능한 패키지로 만들기
- Docker Container: 이미지를 실제로 실행하기
- Docker Compose: 로컬에서 실행 구조 관리하기
- Kubernetes: 컨테이너를 클러스터에서 운영하기
- Helm: Kubernetes 설정을 패키지로 관리하기
- GitHub Actions: 빌드와 테스트 자동화하기
- Argo CD: Git 기준으로 배포 상태 유지하기
- Prometheus / Grafana: 앱 상태 관찰하기
- Terraform: 클라우드 인프라를 코드로 만들기
