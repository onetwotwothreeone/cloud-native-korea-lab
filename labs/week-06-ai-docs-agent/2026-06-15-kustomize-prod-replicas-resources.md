# Kustomize Prod Replicas and Resources Lab

## 1. 실습 제목

Kustomize prod overlay에 replica 수와 resource requests/limits 추가하기

## 2. 실습 목표

FastAPI Mini Platform의 prod 환경에만 replica 수와 container resources 설정을 추가한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 운영하려면 prod 환경에서 여러 Pod를 실행하고, 각 Pod가 사용할 CPU와 Memory 기준을 정해야 한다.

이번 실습은 아래 흐름 중 prod 운영 안정성 강화 단계에 해당한다.

```text
Kubernetes manifest
→ Kustomize base/overlay
→ dev/prod 환경 분리
→ prod replica/resources 설정
→ GitOps
→ Argo CD
→ 자동 배포
```

## 4. 추가한 파일

```text
mini-platform/k8s/overlays/prod/deployment-patch.yaml
```

## 5. prod patch 내용

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-mini-platform
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: fastapi-mini-platform
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
```

## 6. prod kustomization.yaml 변경 내용

```yaml
patches:
  - path: deployment-patch.yaml
```

## 7. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

kubectl kustomize k8s/overlays/prod | grep -E "name:|replicas:|image:|cpu:|memory:"

kubectl apply -k k8s/overlays/prod
kubectl rollout status deployment/fastapi-mini-platform-prod

kubectl get pods -l environment=prod
kubectl get pods -l environment=prod --no-headers | wc -l

kubectl describe pod -l environment=prod
kubectl get deployment fastapi-mini-platform-prod -o yaml | grep -A 10 resources:

kubectl get svc
kubectl get endpoints fastapi-mini-platform-service-prod
```

prod 접속 확인:

```bash
kubectl port-forward service/fastapi-mini-platform-service-prod 8005:80

curl http://localhost:8005/health
curl http://localhost:8005/version

curl -X POST http://localhost:8005/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 requests와 limits는 왜 필요한가요?"}' | python3 -m json.tool
```

## 8. 성공 확인 결과

- prod overlay에 `deployment-patch.yaml` 추가
- prod Deployment replicas가 2로 변경됨
- prod Pod 2개 Running 확인
- resource requests 설정 확인
  - cpu: 100m
  - memory: 128Mi
- resource limits 설정 확인
  - cpu: 500m
  - memory: 256Mi
- prod Service와 Endpoint 연결 확인
- `/health`, `/version`, `/ask` 정상 응답 확인

## 9. 오늘 배운 점

1. replicas는 같은 앱 Pod를 몇 개 실행할지 정하는 설정이다.
2. requests는 Kubernetes가 Pod 배치를 판단할 때 참고하는 최소 필요 자원이다.
3. limits는 컨테이너가 사용할 수 있는 최대 자원이다.
4. prod 환경에는 dev보다 더 명확한 운영 기준이 필요하다.
5. Kustomize patch를 사용하면 base를 직접 바꾸지 않고 prod 환경에만 설정을 추가할 수 있다.
6. resource 설정은 나중에 모니터링, 오토스케일링, 운영 안정성과 연결된다.

## 10. 다음 실습

Kubernetes namespace를 dev/prod로 분리한다.
