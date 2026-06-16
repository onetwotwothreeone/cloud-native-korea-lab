# Kustomize Basic Lab

## 1. 실습 제목

Kubernetes manifest를 Kustomize base/overlay 구조로 관리하기

## 2. 실습 목표

FastAPI Mini Platform의 Kubernetes manifest를 `base`와 `overlays/dev` 구조로 나누어 관리한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 운영하려면 개발 환경, 테스트 환경, 운영 환경처럼 여러 환경의 Kubernetes 설정을 관리할 수 있어야 한다.

이번 실습은 GitOps와 Argo CD로 가기 위한 manifest 관리 기초 단계다.

```text
Kubernetes manifest
→ Kustomize base/overlay
→ GitOps
→ Argo CD
→ 자동 배포
```

## 4. 변경 전 구조

```text
mini-platform/k8s
├── deployment.yaml
└── service.yaml
```

## 5. 변경 후 구조

```text
mini-platform/k8s
├── base
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays
    └── dev
        └── kustomization.yaml
```

## 6. base/kustomization.yaml

```yaml
resources:
  - deployment.yaml
  - service.yaml
```

## 7. overlays/dev/kustomization.yaml

```yaml
resources:
  - ../../base

nameSuffix: -dev

labels:
  - pairs:
      environment: dev
    includeSelectors: true
```

## 8. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

mkdir -p k8s/base
mkdir -p k8s/overlays/dev

mv k8s/deployment.yaml k8s/base/deployment.yaml
mv k8s/service.yaml k8s/base/service.yaml

cat > k8s/base/kustomization.yaml <<'EOF_INNER'
resources:
  - deployment.yaml
  - service.yaml
EOF_INNER

cat > k8s/overlays/dev/kustomization.yaml <<'EOF_INNER'
resources:
  - ../../base

nameSuffix: -dev

labels:
  - pairs:
      environment: dev
    includeSelectors: true
EOF_INNER

kubectl kustomize k8s/overlays/dev
kubectl delete deployment fastapi-mini-platform --ignore-not-found
kubectl delete service fastapi-mini-platform-service --ignore-not-found
kubectl apply -k k8s/overlays/dev

kubectl get pods
kubectl get svc
kubectl get endpoints fastapi-mini-platform-service-dev
```

port-forward 확인:

```bash
kubectl port-forward service/fastapi-mini-platform-service-dev 8002:80
```

새 터미널에서 확인:

```bash
curl http://localhost:8002/health
curl http://localhost:8002/version

curl -X POST http://localhost:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kustomize는 Kubernetes manifest 관리에서 왜 필요한가요?"}' | python3 -m json.tool
```

## 9. 성공 확인 결과

- `k8s/base` 구조 생성
- `k8s/overlays/dev` 구조 생성
- `kubectl kustomize k8s/overlays/dev` 미리보기 성공
- `kubectl apply -k k8s/overlays/dev` 적용 성공
- `fastapi-mini-platform-dev` Deployment 생성 확인
- `fastapi-mini-platform-service-dev` Service 생성 확인
- Pod 상태 `Running` 확인
- Endpoint 연결 확인
- `/health`, `/version`, `/ask`, `/docs` 정상 확인

## 10. 오늘 배운 점

1. Kustomize는 Kubernetes manifest를 환경별로 관리할 수 있게 해준다.
2. base는 공통 설정이고, overlay는 환경별 차이를 적용하는 설정이다.
3. `kubectl apply -k`는 kustomization.yaml 기준으로 리소스를 적용한다.
4. nameSuffix를 사용하면 dev/prod 같은 환경 구분을 리소스 이름에 반영할 수 있다.
5. Kustomize는 나중에 Argo CD와 GitOps로 가기 위한 중요한 기초다.

## 11. 다음 실습

Kustomize prod overlay를 만들고 dev/prod 이미지 태그 전략을 분리한다.
