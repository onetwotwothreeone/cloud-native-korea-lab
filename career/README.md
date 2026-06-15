# Cloud Native Career Guide

Cloud Native Career Guide는 Cloud Native Korea Lab의 커리어 확장 문서입니다.

목표는 클라우드 네이티브를 공부하는 초보자가 아래 질문에 답할 수 있도록 돕는 것입니다.

```text
내가 지금 배우는 Docker, Kubernetes, CI/CD, Terraform은 실제 채용공고에서 어떻게 쓰일까?
어떤 자격증을 어떤 순서로 준비하면 좋을까?
내 GitHub 포트폴리오는 채용공고 요구사항과 연결되어 있을까?
관심 있는 기업은 실제로 어떤 기술 문제를 해결하고 있을까?
```

---

## Why This Exists

Cloud Native Korea Lab의 핵심 흐름은 다음과 같습니다.

```text
학습
→ 실습
→ 에러 기록
→ GitHub 포트폴리오
→ 커뮤니티 콘텐츠
→ 커리어 연결
```

처음에는 Docker, Kubernetes, GitHub Actions, Terraform 같은 기술 이름이 따로따로 보입니다.
하지만 실제 채용공고와 기업 테크 노트를 보면 이 기술들은 하나의 운영 흐름으로 연결됩니다.

```text
Linux / Git
→ Docker
→ Kubernetes
→ CI/CD
→ Helm / Argo CD
→ Monitoring
→ Terraform
→ Cloud Platform
```

이 문서는 그 연결을 초보자도 이해할 수 있게 정리하기 위한 기준 문서입니다.

---

## Directory Structure

```text
career
├── README.md
├── jobs
│   └── job-curation-template.md
├── tech-notes
│   └── company-tech-note-template.md
├── certifications
│   └── cloud-native-certification-roadmap.md
├── roles
│   └── cloud-native-role-map.md
└── portfolio-checklist.md
```

---

## Core Principles

### 1. 채용공고를 그대로 복사하지 않는다

채용공고는 시간이 지나면 사라지거나 내용이 바뀔 수 있습니다.
따라서 Cloud Native Korea Lab에서는 채용공고를 단순 저장하지 않고, 아래처럼 학습 관점으로 번역합니다.

```text
채용공고 요구 기술
→ 배워야 할 개념
→ 해볼 실습
→ GitHub 포트폴리오 증거
→ 커뮤니티 설명 글
```

### 2. 기업 테크 노트는 관심사의 힌트로 사용한다

기업 테크 노트는 그 회사가 최근 어떤 기술 문제를 해결했고, 어떤 기술을 중요하게 다루는지 보여주는 좋은 참고자료입니다.

다만 테크 노트 하나를 회사 전체의 공식 전략으로 단정하지 않습니다.
아래처럼 학습과 면접 준비를 위한 힌트로 사용합니다.

```text
기업 테크 노트
→ 기업이 해결한 문제
→ 등장한 기술
→ 관련 채용공고 요구사항
→ 연결되는 실습
→ 포트폴리오 증거
```

### 3. 자격증은 목표가 아니라 학습 경로로 본다

자격증은 실력을 자동으로 보장하지 않습니다.
하지만 학습 범위를 정리하고, 기본기를 점검하고, 커리어 방향을 잡는 데 도움이 됩니다.

### 4. 모든 커리어 정보는 실습과 연결한다

Cloud Native Korea Lab은 이론 중심 커뮤니티가 아닙니다.
따라서 커리어 정보도 반드시 실습으로 연결합니다.

예시:

```text
채용공고에 Kubernetes가 나온다
→ 관련 기업 테크 노트에서 배포 안정화 사례를 읽는다
→ Deployment / Service / Probe 실습을 한다
→ GitHub에 manifest를 기록한다
→ README에 배포 흐름을 설명한다
→ 네이버 카페에 초보자용 글로 공유한다
```

---

## Recommended First Use

1. `roles/cloud-native-role-map.md`에서 직무 차이를 이해합니다.
2. `certifications/cloud-native-certification-roadmap.md`에서 자격증 흐름을 확인합니다.
3. `jobs/job-curation-template.md`로 주간 채용공고 큐레이션 글을 작성합니다.
4. `tech-notes/company-tech-note-template.md`로 기업 테크 노트를 학습 자료로 정리합니다.
5. `portfolio-checklist.md`로 현재 GitHub 포트폴리오 상태를 점검합니다.

---

## Short Definition

```text
Cloud Native Career Guide는 초보자가 클라우드 네이티브 학습 내용을 실제 직무, 채용공고, 기업 테크 노트, 자격증, 포트폴리오와 연결하도록 돕는 커리어 문서입니다.
```
