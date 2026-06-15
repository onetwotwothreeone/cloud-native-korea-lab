# Cloud Native Portfolio Checklist

이 문서는 Cloud Native Korea Lab 실습 기록을 채용공고와 연결하기 위한 포트폴리오 점검표입니다.

목표는 단순히 공부했다는 말을 하는 것이 아니라, GitHub에 남은 기록으로 증명하는 것입니다.

---

## 1. Easy Summary

```text
채용공고는 “이 기술을 써본 적 있나요?”라고 묻습니다.
포트폴리오는 “네, 여기 GitHub 기록이 있습니다.”라고 답하는 증거입니다.
```

---

## 2. Basic Project Evidence

```text
□ 프로젝트 목표가 README에 적혀 있다
□ 기술 스택이 README에 정리되어 있다
□ 실행 방법이 README에 있다
□ 폴더 구조가 README에 있다
□ 완료한 실습 목록이 있다
□ 다음 단계가 정리되어 있다
```

---

## 3. Docker Evidence

```text
□ Dockerfile이 있다
□ Docker 이미지 빌드 명령어를 기록했다
□ 컨테이너 실행 명령어를 기록했다
□ Docker Compose 실행 기록이 있다
□ 이미지와 컨테이너 차이를 설명할 수 있다
```

---

## 4. Kubernetes Evidence

```text
□ Deployment manifest가 있다
□ Service manifest가 있다
□ Pod 상태 확인 명령어를 기록했다
□ rollout status 확인 기록이 있다
□ readinessProbe 설정 기록이 있다
□ livenessProbe 설정 기록이 있다
□ imagePullPolicy를 이해하고 설정했다
□ commit SHA 기반 이미지 배포 기록이 있다
```

---

## 5. CI/CD Evidence

```text
□ GitHub Actions workflow 파일이 있다
□ push 또는 pull_request 시 테스트가 실행된다
□ pytest 실행 기록이 있다
□ Docker 이미지 자동 빌드 기록이 있다
□ GHCR push 기록이 있다
□ 테스트 실패 시 배포가 막히는 구조를 설명할 수 있다
```

---

## 6. GitOps / Helm Evidence

```text
□ Helm Chart 구조를 만들었다
□ values.yaml로 설정을 분리했다
□ Argo CD가 Git 저장소와 클러스터 상태를 비교하는 방식을 설명할 수 있다
□ GitOps가 왜 운영 기준을 Git으로 두는지 설명할 수 있다
```

---

## 7. Monitoring Evidence

```text
□ /health API가 있다
□ /version API가 있다
□ Prometheus가 어떤 지표를 수집하는지 설명할 수 있다
□ Grafana가 왜 필요한지 설명할 수 있다
□ 로그와 메트릭의 차이를 설명할 수 있다
```

---

## 8. Terraform / Cloud Evidence

```text
□ Terraform의 역할을 설명할 수 있다
□ provider, resource, state 개념을 이해한다
□ plan과 apply의 차이를 설명할 수 있다
□ AWS/GCP/Azure 중 하나의 기본 배포 흐름을 정리했다
```

---

## 9. Troubleshooting Evidence

```text
□ 에러 로그를 최소 3개 이상 기록했다
□ 에러의 원인과 해결 방법을 정리했다
□ 같은 에러를 예방하는 방법을 작성했다
□ 에러에서 배운 개념을 커뮤니티 글로 바꿨다
```

---

## 10. Community Evidence

```text
□ 실습 하나를 네이버 카페 글로 바꿨다
□ 초보자용 쉬운 비유를 포함했다
□ 실행 명령어와 성공 확인 방법을 포함했다
□ 댓글 유도 질문을 포함했다
□ 다음 실습 예고를 작성했다
```

---

## 11. Resume Sentence Examples

### DevOps Direction

```text
FastAPI 기반 Cloud Native AI Docs Agent를 Docker, Kubernetes, GitHub Actions, GHCR 기반 CI/CD 흐름으로 구성하고, 배포 추적성을 높이기 위해 commit SHA 기반 이미지 태그를 적용했습니다.
```

### Kubernetes Direction

```text
Kubernetes Deployment, Service, readinessProbe, livenessProbe를 적용해 FastAPI 애플리케이션의 배포와 상태 확인 흐름을 실습했습니다.
```

### Community / Education Direction

```text
클라우드 네이티브 학습 과정을 GitHub 실습 기록과 초보자용 커뮤니티 콘텐츠로 전환하며, Docker, Kubernetes, CI/CD 개념을 비전공자도 이해할 수 있게 문서화했습니다.
```

---

## 12. Weekly Review Template

```text
이번 주 완료한 실습:

채용공고와 연결되는 기술:

GitHub에 남긴 증거:

아직 부족한 부분:

다음 주 보완할 실습:

커뮤니티에 공유한 글:
```
