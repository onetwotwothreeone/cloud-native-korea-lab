# Company Tech Note Template

이 문서는 기업의 테크 블로그, 테크 노트, 엔지니어링 블로그 글을 Cloud Native Korea Lab의 커리어 리서치 자료로 정리하기 위한 템플릿입니다.

목표는 기업이 최근 어떤 기술 문제를 해결했고, 어떤 기술에 관심을 보이는지 학습 관점에서 해석하는 것입니다.

---

## 1. Basic Information

```text
Date:
Company:
Tech Note Title:
Published Date:
Author / Team:
Original Link:
Related Job Posting:
```

---

## 2. Easy Summary

```text
이 테크 노트는 어떤 문제를 다루는가?
초보자도 이해할 수 있게 3문장으로 정리한다.
```

예시:

```text
이 글은 서비스 배포를 더 안전하게 만들기 위한 경험을 다룹니다.
기존에는 배포 과정에서 사람이 직접 확인해야 할 부분이 많았지만,
자동화와 모니터링을 통해 문제를 더 빨리 발견하도록 개선했습니다.
```

---

## 3. What Problem Did They Solve?

기업이 해결하려고 한 문제를 정리합니다.

```text
Problem:

Why It Matters:

Before:

After:
```

예시:

```text
Problem:
배포 후 문제가 생겼을 때 원인을 빠르게 찾기 어려웠다.

Why It Matters:
서비스 장애 시간이 길어지면 사용자 경험과 비즈니스에 영향을 준다.

Before:
로그와 지표가 흩어져 있었다.

After:
모니터링 대시보드와 알림 체계를 개선했다.
```

---

## 4. Technologies Mentioned

테크 노트에 등장한 기술을 Cloud Native Korea Lab 학습 주제와 연결합니다.

| Technology | Easy Meaning | Related Lab |
|---|---|---|
| Kubernetes | 컨테이너를 운영 환경에서 관리하는 시스템 | Deployment / Service |
| GitHub Actions | 테스트와 빌드를 자동화하는 도구 | CI 실습 |
| Argo CD | Git 기준으로 배포 상태를 맞추는 도구 | GitOps 실습 |
| Prometheus | 시스템 상태 숫자를 수집하는 도구 | Monitoring 실습 |
| Grafana | 상태 데이터를 대시보드로 보여주는 도구 | Dashboard 실습 |
| Terraform | 인프라를 코드로 관리하는 도구 | IaC 실습 |

---

## 5. Connection to Job Posting

이 테크 노트가 채용공고와 어떻게 연결되는지 정리합니다.

```text
Related Role:

Related Job Requirement:

Why This Tech Note Matters:

Interview Preparation Point:
```

예시:

```text
Related Role:
DevOps Engineer

Related Job Requirement:
Kubernetes, CI/CD, Monitoring 경험

Why This Tech Note Matters:
이 회사가 배포 안정성과 관찰 가능성에 관심을 가지고 있을 가능성이 있다.

Interview Preparation Point:
readinessProbe, livenessProbe, rollout, rollback을 설명할 수 있어야 한다.
```

---

## 6. Portfolio Evidence

이 테크 노트와 비슷한 관심사를 보여주기 위해 GitHub에 남기면 좋은 증거입니다.

```text
□ 관련 실습 기록
□ 관련 manifest 또는 workflow 파일
□ README 설명
□ 에러 해결 기록
□ before / after 개선 기록
□ 초보자용 커뮤니티 글
```

예시:

```text
□ mini-platform/k8s/deployment.yaml
□ mini-platform/k8s/service.yaml
□ .github/workflows/fastapi-ci.yml
□ labs/week-05-kubernetes 배포 기록
□ content/community-posts 배포 안정화 설명 글
```

---

## 7. Beginner Learning Points

```text
오늘 배운 개념 1:

오늘 배운 개념 2:

오늘 배운 개념 3:

내가 추가로 실습할 것:
```

---

## 8. Important Caution

기업 테크 노트는 좋은 참고자료이지만, 회사 전체의 공식 기술 전략이라고 단정하면 안 됩니다.

```text
주의할 점:
- 오래된 글은 현재 상황과 다를 수 있다.
- 특정 팀의 경험일 수 있다.
- 홍보 성격이 있을 수 있다.
- 채용공고와 반드시 1:1로 일치하지 않을 수 있다.
```

따라서 표현은 아래처럼 사용합니다.

```text
이 회사가 이 기술에 관심이 있을 가능성이 있다.
이 글은 면접 준비와 학습 방향을 잡는 참고자료로 활용한다.
```

---

## 9. Community Post Version

```text
[오늘의 클라우드 네이티브 커리어]

오늘은 채용공고와 함께 기업 테크 노트를 보는 방법을 정리했습니다.

채용공고가 “우리가 이런 사람을 찾습니다”라면,
테크 노트는 “우리는 최근 이런 기술 문제를 해결했습니다”에 가깝습니다.

그래서 테크 노트를 보면 기업이 어떤 문제에 관심이 있는지,
어떤 기술을 실제로 사용하고 있는지 힌트를 얻을 수 있습니다.

오늘의 연결 흐름:
테크 노트 주제
→ 등장한 기술
→ 관련 실습
→ GitHub 포트폴리오 증거
→ 면접 준비 포인트

오늘의 질문:
여러분은 관심 있는 회사의 테크 블로그를 읽어본 적 있으신가요?
```
