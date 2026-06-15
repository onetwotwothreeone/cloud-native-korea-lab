# Cloud Native Role Map

이 문서는 클라우드 네이티브 관련 직무를 초보자도 이해할 수 있게 정리한 역할 지도입니다.

목표는 직무 이름을 외우는 것이 아니라, 각 직무가 어떤 문제를 해결하는지 이해하는 것입니다.

---

## 1. Easy Summary

```text
Cloud Engineer는 클라우드 자원을 다루는 사람입니다.
DevOps Engineer는 개발과 운영 사이의 자동화 흐름을 만드는 사람입니다.
SRE는 서비스가 안정적으로 돌아가도록 관찰하고 개선하는 사람입니다.
Platform Engineer는 개발자가 쉽게 배포하고 운영할 수 있는 내부 플랫폼을 만드는 사람입니다.
Solutions Architect는 요구사항에 맞는 클라우드 구조를 설계하는 사람입니다.
```

---

## 2. Role Comparison

| Role | Easy Meaning | Main Focus | Related Labs |
|---|---|---|---|
| Cloud Engineer | 클라우드 서버와 네트워크를 관리하는 사람 | Cloud, Linux, Network, IAM | AWS/GCP/Azure 기초, Terraform |
| DevOps Engineer | 테스트, 빌드, 배포를 자동화하는 사람 | CI/CD, Docker, Kubernetes | GitHub Actions, Docker, Kubernetes |
| SRE | 서비스 안정성을 관찰하고 개선하는 사람 | Reliability, Monitoring | Prometheus, Grafana, Logs |
| Platform Engineer | 개발자를 위한 배포 플랫폼을 만드는 사람 | Kubernetes, GitOps | Helm, Argo CD |
| Kubernetes Engineer | Kubernetes 배포 환경을 관리하는 사람 | Cluster, Workload | Deployment, Service, Ingress |
| Infrastructure Engineer | 서버와 인프라 기반을 관리하는 사람 | Linux, Network, IaC | Terraform, Cloud Network |
| Solutions Architect | 전체 클라우드 구조를 설계하는 사람 | Architecture, Cost, Reliability | Cloud 설계, README 문서화 |

---

## 3. Beginner-Friendly Explanation

### Cloud Engineer

클라우드 위에 서버, 네트워크, 스토리지 같은 기본 자원을 만들고 관리하는 역할입니다.

관련 학습:

```text
Linux
Network
AWS / GCP / Azure
Terraform
Monitoring
```

### DevOps Engineer

개발자가 코드를 올렸을 때 테스트, 빌드, 배포가 자동으로 이어지도록 만드는 역할입니다.

관련 학습:

```text
Git
GitHub Actions
Docker
Docker Registry
Kubernetes
CI/CD
```

### SRE

서비스가 안정적으로 돌아가는지 지표를 보고, 문제가 생기기 전에 개선하는 역할입니다.

관련 학습:

```text
Monitoring
Logging
Metrics
Prometheus
Grafana
```

### Platform Engineer

개발자가 복잡한 인프라를 직접 몰라도 쉽게 배포할 수 있도록 내부 도구와 플랫폼을 만드는 역할입니다.

관련 학습:

```text
Kubernetes
Helm
Argo CD
GitOps
CI/CD
```

### Solutions Architect

요구사항에 맞게 클라우드 시스템 전체 구조를 설계하는 역할입니다.

관련 학습:

```text
Cloud Architecture
Network
Reliability
Cost Optimization
Scalability
```

---

## 4. Beginner Recommendation

초보자는 처음부터 직무를 하나로 고정하지 않아도 됩니다.

추천 흐름은 다음과 같습니다.

```text
1. Docker와 Kubernetes로 기본 운영 흐름 이해
2. GitHub Actions로 자동화 경험
3. Prometheus / Grafana로 관찰 경험
4. Terraform으로 인프라 코드화 경험
5. 그 후 관심 방향 선택
```

방향 선택 예시:

```text
자동화가 재미있다 → DevOps Engineer
안정성과 관찰이 재미있다 → SRE
Kubernetes와 배포 시스템이 재미있다 → Platform Engineer
클라우드 구조 설계가 재미있다 → Solutions Architect
```

---

## 5. Community Post Version

```text
[오늘의 클라우드 네이티브 커리어]

Cloud Engineer, DevOps Engineer, SRE, Platform Engineer는 이름이 어렵지만,
쉽게 보면 모두 서비스를 더 안정적으로 만들고 운영하기 위한 역할입니다.

차이는 초점입니다.

Cloud Engineer는 클라우드 자원을 다루고,
DevOps Engineer는 배포 자동화를 만들고,
SRE는 서비스 안정성을 관찰하고,
Platform Engineer는 개발자가 쉽게 배포할 수 있는 플랫폼을 만듭니다.

오늘의 질문:
여러분은 자동화, 안정성, 클라우드 설계 중 어떤 쪽이 가장 흥미로운가요?
```
