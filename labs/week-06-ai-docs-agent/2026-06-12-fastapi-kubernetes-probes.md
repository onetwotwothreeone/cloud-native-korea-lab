# FastAPI Mini Platform Kubernetes Probe Lab

## 1. 실습 제목

FastAPI Mini Platform에 readinessProbe와 livenessProbe 추가하기

## 2. 실습 목표

Kubernetes Deployment에 readinessProbe와 livenessProbe를 추가해서 FastAPI 앱의 준비 상태와 생존 상태를 Kubernetes가 직접 확인하게 만든다.

## 3. 사용한 API

```text
GET /health
4. 추가한 Kubernetes 설정
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 15
  periodSeconds: 20
  timeoutSeconds: 3
  failureThreshold: 3
5. 실행한 명령어
cd ~/cloud-native-korea-lab/mini-platform

kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/fastapi-mini-platform

kubectl get pods
kubectl describe pod -l app=fastapi-mini-platform

kubectl port-forward service/fastapi-mini-platform-service 8002:80

새 터미널에서 확인:

curl http://localhost:8002/health
curl http://localhost:8002/version

curl -X POST http://localhost:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 readinessProbe와 livenessProbe는 왜 필요한가요?"}' | python3 -m json.tool
6. 성공 확인 결과
Pod 상태 1/1 Running 확인
Ready: True 확인
ContainersReady: True 확인
Restart Count: 0 확인
readinessProbe가 /health를 확인하는 것 확인
livenessProbe가 /health를 확인하는 것 확인
/health, /version, /ask, /docs 정상 확인
7. 오늘 배운 점
Pod가 Running이어도 앱이 요청을 받을 준비가 된 것은 아닐 수 있다.
readinessProbe는 Pod가 트래픽을 받을 준비가 되었는지 확인한다.
livenessProbe는 앱이 살아 있는지 확인하고, 실패가 반복되면 컨테이너를 재시작하게 한다.
/health API는 Kubernetes 운영에서 매우 중요한 상태 확인 입구다.
8. 다음 실습

FastAPI Mini Platform Kubernetes 리소스를 정리하고 README를 최신 구조로 업데이트한다.
