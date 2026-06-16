# Kubernetes Namespace Dev/Prod Lab

## 1. 실습 제목

Kubernetes namespace를 dev/prod로 분리하기

## 2. 실습 목표

FastAPI Mini Platform의 dev 환경과 prod 환경을 각각 다른 Kubernetes namespace에 배포한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 운영하려면 개발 환경과 운영 환경을 분리해서 관리할 수 있어야 한다.

이번 실습은 아래 흐름 중 namespace 기반 환경 분리 단계에 해당한다.

```text
Kubernetes manifest
→ Kustomize base/overlay
→ dev/prod 환경 분리
→ namespace dev/prod 분리
→ GitOps
→ Argo CD
→ 자동 배포
```

## 4. 추가한 namespace

```text
cnkl-dev
cnkl-prod
```

## 5. 추가한 파일

```text
mini-platform/k8s/namespaces/dev.yaml
mini-platform/k8s/namespaces/prod.yaml
```

## 6. dev overlay 변경 내용

```yaml
namespace: cnkl-dev
```

## 7. prod overlay 변경 내용

```yaml
namespace: cnkl-prod
```

## 8. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

mkdir -p k8s/namespaces

kubectl kustomize k8s/overlays/dev | grep -E "name:|namespace:|image:|environment:"
kubectl kustomize k8s/overlays/prod | grep -E "name:|namespace:|image:|environment:|replicas:|cpu:|memory:"

kubectl delete deployment fastapi-mini-platform --ignore-not-found
kubectl delete service fastapi-mini-platform-service --ignore-not-found
kubectl delete deployment fastapi-mini-platform-dev --ignore-not-found
kubectl delete service fastapi-mini-platform-service-dev --ignore-not-found
kubectl delete deployment fastapi-mini-platform-prod --ignore-not-found
kubectl delete service fastapi-mini-platform-service-prod --ignore-not-found

kubectl apply -f k8s/namespaces/dev.yaml
kubectl apply -f k8s/namespaces/prod.yaml

kubectl get namespaces | grep cnkl

kubectl apply -k k8s/overlays/dev
kubectl apply -k k8s/overlays/prod

kubectl get pods -n cnkl-dev
kubectl get svc -n cnkl-dev
kubectl get endpoints fastapi-mini-platform-service-dev -n cnkl-dev

kubectl get pods -n cnkl-prod
kubectl get svc -n cnkl-prod
kubectl get endpoints fastapi-mini-platform-service-prod -n cnkl-prod

kubectl get all --all-namespaces | grep fastapi-mini-platform
```

dev 접속 확인:

```bash
kubectl port-forward -n cnkl-dev service/fastapi-mini-platform-service-dev 8002:80

curl http://localhost:8002/health
curl http://localhost:8002/version
```

prod 접속 확인:

```bash
kubectl port-forward -n cnkl-prod service/fastapi-mini-platform-service-prod 8005:80

curl http://localhost:8005/health
curl http://localhost:8005/version

curl -X POST http://localhost:8005/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes namespace는 왜 필요한가요?"}' | python3 -m json.tool
```

## 9. 성공 확인 결과

- `cnkl-dev` namespace 생성 확인
- `cnkl-prod` namespace 생성 확인
- dev 리소스가 `cnkl-dev` namespace에 생성됨
- prod 리소스가 `cnkl-prod` namespace에 생성됨
- dev Pod Running 확인
- prod Pod Running 확인
- dev Service와 Endpoint 연결 확인
- prod Service와 Endpoint 연결 확인
- dev `/health`, `/version` 정상 응답 확인
- prod `/health`, `/version`, `/ask` 정상 응답 확인

## 10. 오늘 배운 점

1. namespace는 하나의 Kubernetes 클러스터 안에서 리소스를 분리하는 공간이다.
2. dev와 prod를 namespace로 분리하면 리소스를 더 명확하게 관리할 수 있다.
3. 같은 이름의 리소스라도 namespace가 다르면 구분될 수 있다.
4. `kubectl` 명령에서 namespace를 보려면 `-n <namespace>` 옵션을 사용한다.
5. port-forward도 namespace를 지정해야 올바른 Service에 연결된다.
6. namespace 분리는 나중에 권한, 리소스 쿼터, GitOps 운영과 연결된다.

## 11. 다음 실습

Kubernetes namespace별 context 사용법과 리소스 정리 전략을 실습한다.
