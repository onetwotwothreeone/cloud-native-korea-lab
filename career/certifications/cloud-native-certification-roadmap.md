# Cloud Native Certification Roadmap

이 문서는 Cloud Native Korea Lab에서 클라우드 네이티브 관련 자격증을 학습 경로로 정리하기 위한 문서입니다.

자격증은 최종 목표가 아니라, 학습 범위를 확인하고 실습 방향을 잡기 위한 도구로 사용합니다.

---

## 1. Beginner First Principle

초보자는 처음부터 어려운 자격증을 목표로 잡기보다, 아래 순서로 접근하는 것이 좋습니다.

```text
기본 개념 이해
→ 작은 실습 완료
→ GitHub 기록
→ 쉬운 설명 글 작성
→ 자격증 범위와 비교
→ 부족한 부분 보완
```

---

## 2. Recommended Path

### Path A. Kubernetes / Cloud Native 운영 방향

```text
KCNA
→ CKA
→ CKS
```

- KCNA: 클라우드 네이티브와 Kubernetes 기본 개념을 넓게 이해
- CKA: Kubernetes 클러스터 운영과 문제 해결 역량 확인
- CKS: Kubernetes 보안 역량 확인

### Path B. Kubernetes 애플리케이션 배포 방향

```text
KCNA
→ CKAD
```

- KCNA: 기본 개념 입문
- CKAD: Kubernetes에서 애플리케이션을 배포하고 설정하는 역량 확인

### Path C. Cloud Platform 입문 방향

```text
AWS Cloud Practitioner / Azure Fundamentals
→ AWS Solutions Architect Associate / Google Associate Cloud Engineer / Azure Administrator
```

- 클라우드 기본 개념을 먼저 이해
- 이후 실제 인프라 설계와 운영 역량으로 확장

---

## 3. Certification Map

| Area | Certification | Good For | Related Cloud Native Korea Lab Topics |
|---|---|---|---|
| Cloud Native Intro | KCNA | 클라우드 네이티브 전체 개념 입문 | Kubernetes, CNCF, Container, Observability |
| Kubernetes Admin | CKA | Kubernetes 운영자 방향 | Pod, Deployment, Service, Cluster, Troubleshooting |
| Kubernetes App Developer | CKAD | Kubernetes 앱 배포 방향 | Manifest, ConfigMap, Secret, Volume, Deployment |
| Kubernetes Security | CKS | Kubernetes 보안 방향 | RBAC, NetworkPolicy, Security Context |
| AWS Intro | AWS Cloud Practitioner | AWS 기본 개념 | Cloud, Region, IAM, Compute, Storage |
| AWS Architecture | AWS Solutions Architect Associate | AWS 인프라 설계 입문 | VPC, EC2, Load Balancer, RDS, IAM |
| Google Cloud | Google Associate Cloud Engineer | GCP 운영 입문 | Compute, IAM, Networking, Kubernetes Engine |
| Azure | Azure Administrator | Azure 운영 입문 | VM, Network, Identity, AKS |
| Terraform | Terraform Associate | Infrastructure as Code 입문 | Terraform, Provider, State, Plan, Apply |

---

## 4. Schedule Management Template

클라우드 자격증은 고정된 시험일보다 온라인 또는 시험센터 예약 방식인 경우가 많습니다.
따라서 Cloud Native Korea Lab에서는 날짜만 외우기보다, 아래 형식으로 준비 일정을 관리합니다.

```text
Certification:
Official Page:
Exam Provider:
Target Month:
Study Start Date:
Practice Exam Date:
Booking Status:
Exam Date:
Result:
Retake Plan:
```

---

## 5. 4-Week Preparation Example

### Week 1. Concept Mapping

```text
목표:
자격증 범위를 Cloud Native Korea Lab 로드맵과 연결한다.

해야 할 일:
- 공식 시험 가이드 확인
- 모르는 용어를 glossary에 추가
- 관련 실습 목록 만들기
```

### Week 2. Hands-on Labs

```text
목표:
이론을 실습으로 확인한다.

해야 할 일:
- Docker / Kubernetes / Cloud 실습 진행
- 명령어와 결과를 GitHub에 기록
- 에러 발생 시 error-logs에 기록
```

### Week 3. Review and Practice

```text
목표:
부족한 영역을 점검한다.

해야 할 일:
- 기출 유형 또는 연습 문제 풀이
- 자주 틀리는 개념 정리
- 공식 문서 다시 읽기
```

### Week 4. Portfolio and Exam Readiness

```text
목표:
시험 준비와 포트폴리오 정리를 함께 마무리한다.

해야 할 일:
- GitHub README에 배운 내용 정리
- 커뮤니티에 자격증 준비 회고 글 작성
- 시험 예약 상태 확인
```

---

## 6. Official References

자격증 정보는 반드시 공식 페이지 기준으로 확인합니다.

- CNCF Certification: https://www.cncf.io/training/certification/
- Kubernetes Certifications: https://training.linuxfoundation.org/certification/catalog/?_sft_technology=kubernetes
- AWS Certification: https://aws.amazon.com/certification/
- Google Cloud Certification: https://cloud.google.com/learn/certification
- Microsoft Certifications: https://learn.microsoft.com/credentials/browse/
- HashiCorp Terraform Associate: https://developer.hashicorp.com/certifications/infrastructure-automation

---

## 7. Community Post Version

```text
[오늘의 클라우드 네이티브 커리어]

자격증은 목표가 아니라 학습 경로입니다.

처음부터 CKA, CKAD 같은 어려운 시험을 바로 준비하기보다,
먼저 Docker, Kubernetes, CI/CD, Terraform을 작은 실습으로 경험하고,
그 다음 자격증 범위와 비교해보는 것이 좋습니다.

Cloud Native Korea Lab에서는 자격증을 이렇게 바라봅니다.

개념 이해
→ 실습
→ 에러 기록
→ GitHub 포트폴리오
→ 자격증 범위 점검

오늘의 질문:
여러분은 클라우드 자격증 중 어떤 시험이 가장 궁금하신가요?
```
