# Cloud Native Job Curation Template

이 문서는 Cloud Native Korea Lab에서 클라우드 네이티브 관련 채용공고를 학습 자료로 바꾸기 위한 템플릿입니다.

단순히 채용공고를 모으는 것이 아니라, 공고에 등장하는 기술 요구사항을 학습 로드맵, 실습, 포트폴리오와 연결하는 것이 목적입니다.

---

## 1. Basic Information

```text
Date:
Source:
Company:
Role:
Location:
Experience Level:
Employment Type:
Original Job Link:
```

---

## 2. Short Job Summary

```text
이 공고는 어떤 일을 하는 포지션인가?
초보자도 이해할 수 있게 3문장으로 정리한다.
```

예시:

```text
이 포지션은 서비스가 안정적으로 배포되고 운영되도록 자동화하는 역할입니다.
Docker와 Kubernetes를 사용해 애플리케이션 실행 환경을 관리하고,
CI/CD 도구로 테스트와 배포 과정을 자동화합니다.
```

---

## 3. Required Skills

채용공고에서 요구하는 기술을 그대로 적고, Cloud Native Korea Lab 학습 주제와 연결합니다.

| Job Requirement | Easy Meaning | Related Lab |
|---|---|---|
| Docker | 앱을 컨테이너로 포장하는 기술 | Docker 이미지 빌드 |
| Kubernetes | 컨테이너를 여러 서버에서 관리하는 기술 | Deployment / Service 배포 |
| CI/CD | 테스트와 배포를 자동화하는 흐름 | GitHub Actions |
| Terraform | 클라우드 인프라를 코드로 만드는 도구 | IaC 기초 실습 |
| Monitoring | 서비스 상태를 관찰하는 활동 | Prometheus / Grafana |

---

## 4. Learning Roadmap Mapping

이 공고를 준비하려면 어떤 순서로 공부해야 하는지 정리합니다.

```text
1. Linux / Shell 기본 명령어
2. Git / GitHub 기본 흐름
3. Docker 이미지와 컨테이너
4. Docker Compose 로컬 실행
5. Kubernetes Pod / Deployment / Service
6. GitHub Actions CI/CD
7. Helm Chart
8. Argo CD GitOps
9. Prometheus / Grafana Monitoring
10. Terraform / Cloud Deployment
```

---

## 5. Portfolio Evidence

이 공고에 지원한다고 가정했을 때 GitHub에 남겨야 할 증거입니다.

```text
□ Dockerfile 작성 기록
□ Docker 이미지 빌드 기록
□ Docker Compose 실행 기록
□ Kubernetes Deployment manifest
□ Kubernetes Service manifest
□ readinessProbe / livenessProbe 설정
□ GitHub Actions 테스트 성공 기록
□ Docker 이미지 자동 빌드 기록
□ GHCR 이미지 push 기록
□ commit SHA 기반 이미지 배포 기록
□ 에러 해결 기록
□ README에 아키텍처 설명
```

---

## 6. Difficulty for Beginners

```text
초보자 기준 난이도:
쉬움 / 보통 / 어려움

이유:

지금 바로 준비할 수 있는 부분:

나중에 준비할 부분:
```

---

## 7. Certification Connection

이 공고와 연결되는 자격증을 정리합니다.

| Certification | Why It Helps |
|---|---|
| KCNA | 클라우드 네이티브 전체 개념 입문 |
| CKA | Kubernetes 운영 역량 증명 |
| CKAD | Kubernetes 기반 애플리케이션 배포 역량 증명 |
| AWS SAA | AWS 인프라 설계 기본기 증명 |
| Google ACE | Google Cloud 운영 기본기 증명 |
| Azure Administrator | Azure 운영 기본기 증명 |

---

## 8. Community Post Version

```text
[오늘의 클라우드 네이티브 커리어]

오늘 살펴본 직무:

공고에서 자주 보인 기술:

초보자용 쉬운 설명:

이 기술을 배우는 이유:

Cloud Native Korea Lab에서 연결되는 실습:

GitHub 포트폴리오에 남기면 좋은 증거:

오늘의 질문:
여러분은 클라우드 네이티브 채용공고를 볼 때 어떤 기술 이름이 가장 어렵게 느껴지나요?
```

---

## 9. Important Note

채용공고는 수시로 변경되므로, 이 문서는 실시간 채용 데이터 저장소가 아닙니다.
Cloud Native Korea Lab에서는 채용공고를 학습 방향과 포트폴리오 준비를 위한 참고 자료로 사용합니다.
