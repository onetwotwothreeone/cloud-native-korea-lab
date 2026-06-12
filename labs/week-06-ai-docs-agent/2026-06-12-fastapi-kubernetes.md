# FastAPI Mini Platform Kubernetes Lab

## 1. 실습 제목

FastAPI Mini Platform을 Kubernetes Deployment와 Service로 실행하기

## 2. 실습 목표

Docker 이미지로 만든 FastAPI Mini Platform을 Kubernetes Deployment와 Service로 실행한다.

## 3. 사용한 파일

```text
mini-platform
├── app
│   └── main.py
├── Dockerfile
└── k8s
    ├── deployment.yaml
    └── service.yaml
```
## 4. 실행한 명령어
```
cd ~/cloud-native-korea-lab/mini-platform

kubectl config get-contexts
kubectl config use-context docker-desktop
kubectl get nodes

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods
kubectl get svc
kubectl get endpoints fastapi-mini-platform-service

kubectl port-forward service/fastapi-mini-platform-service 8002:80
```
새 터미널에서 테스트:
```
curl http://localhost:8002/health
curl http://localhost:8002/version

curl -X POST http://localhost:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 Service는 왜 필요한가요?"}' | python3 -m json.tool
```
## 5. 성공 확인 결과
1. Kubernetes context docker-desktop 설정 확인
2. Node docker-desktop Ready 확인
3. Deployment fastapi-mini-platform 생성 확인
4. Service fastapi-mini-platform-service 생성 확인
5. Pod 상태 1/1 Running 확인
6. Endpoint 10.1.0.6:8000 연결 확인
7. port-forward로 localhost:8002 접속 확인
8. /health, /version, /ask, /docs 확인

## 6. 오늘 배운 점
Deployment는 FastAPI Pod를 원하는 상태로 유지한다.
Service는 Pod로 가는 안정적인 네트워크 입구다.
Endpoint는 Service가 실제로 연결한 Pod 주소를 보여준다.
port-forward는 내 MacBook과 Kubernetes Service를 임시로 연결한다.
Docker Compose는 로컬 실행에 좋고, Kubernetes는 운영 방식에 가깝다.

## 7. 다음 실습

FastAPI Mini Platform에 readinessProbe와 livenessProbe를 추가한다.
