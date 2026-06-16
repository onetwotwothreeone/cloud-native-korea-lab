# Kustomize Dev/Prod Image Strategy Lab

## 1. 실습 제목

Kustomize로 dev/prod 환경의 이미지 태그 전략 분리하기

## 2. 실습 목표

FastAPI Mini Platform의 Kubernetes manifest를 Kustomize base/overlay 구조로 관리하고, dev 환경과 prod 환경의 Docker 이미지 태그 전략을 분리한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 운영하려면 개발 환경과 운영 환경을 나누어 관리할 수 있어야 한다.

이번 실습은 아래 흐름 중 Kustomize 기반 환경 분리 단계에 해당한다.

```text
Kubernetes manifest
→ Kustomize base/overlay
→ dev/prod 환경 분리
→ GitOps
→ Argo CD
→ 자동 배포
```

## 4. 변경 전 구조

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

## 5. 변경 후 구조

```text
mini-platform/k8s
├── base
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays
    ├── dev
    │   └── kustomization.yaml
    └── prod
        └── kustomization.yaml
```

## 6. dev 이미지 전략

```yaml
images:
  - name: ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform
    newTag: latest
```

dev 환경은 빠르게 최신 이미지를 확인하기 위해 `latest` 태그를 사용한다.

## 7. prod 이미지 전략

```yaml
images:
  - name: ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform
    newTag: 2d2dd9c7850342517634879db4123e3106ede24b
```

prod 환경은 어떤 코드가 배포되었는지 추적하기 위해 commit SHA 태그를 사용한다.

## 8. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

mkdir -p k8s/overlays/prod

kubectl kustomize k8s/overlays/dev | grep -E "name:|image:|environment:"
kubectl kustomize k8s/overlays/prod | grep -E "name:|image:|environment:"

kubectl delete deployment fastapi-mini-platform --ignore-not-found
kubectl delete service fastapi-mini-platform-service --ignore-not-found
kubectl delete deployment fastapi-mini-platform-dev --ignore-not-found
kubectl delete service fastapi-mini-platform-service-dev --ignore-not-found
kubectl delete deployment fastapi-mini-platform-prod --ignore-not-found
kubectl delete service fastapi-mini-platform-service-prod --ignore-not-found

kubectl apply -k k8s/overlays/dev
kubectl apply -k k8s/overlays/prod

kubectl get pods
kubectl get svc
kubectl get endpoints fastapi-mini-platform-service-dev
kubectl get endpoints fastapi-mini-platform-service-prod

kubectl get deployment fastapi-mini-platform-dev -o yaml | grep image:
kubectl get deployment fastapi-mini-platform-prod -o yaml | grep image:
```

dev 접속 확인:

```bash
kubectl port-forward service/fastapi-mini-platform-service-dev 8002:80

curl http://localhost:8002/health
curl http://localhost:8002/version
```

prod 접속 확인:

```bash
kubectl port-forward service/fastapi-mini-platform-service-prod 8005:80

curl http://localhost:8005/health
curl http://localhost:8005/version

curl -X POST http://localhost:8005/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"dev와 prod 환경을 왜 나눠야 하나요?"}' | python3 -m json.tool
```

## 9. 성공 확인 결과

- `k8s/overlays/prod` 구조 생성
- dev overlay는 `latest` 이미지 사용 확인
- prod overlay는 commit SHA 이미지 사용 확인
- `fastapi-mini-platform-dev` Deployment 생성 확인
- `fastapi-mini-platform-prod` Deployment 생성 확인
- dev/prod Service 생성 확인
- dev/prod Endpoint 연결 확인
- dev `/health`, `/version` 정상 응답 확인
- prod `/health`, `/version`, `/ask` 정상 응답 확인

## 10. 오늘 배운 점

1. Kustomize base는 공통 Kubernetes 설정을 담는다.
2. overlay는 dev/prod 같은 환경별 차이를 표현한다.
3. dev 환경은 빠른 확인을 위해 `latest` 태그를 사용할 수 있다.
4. prod 환경은 추적 가능한 배포를 위해 commit SHA 태그를 사용하는 것이 더 안전하다.
5. 같은 base를 사용해도 overlay를 다르게 만들면 환경별 Kubernetes 리소스를 만들 수 있다.
6. Kustomize는 Argo CD와 GitOps로 넘어가기 전 중요한 manifest 관리 기초다.

## 11. 다음 실습

Kustomize prod overlay에 replica 수와 resource requests/limits를 추가한다.
