# Kubernetes GHCR Image Lab

## 1. 실습 제목

Kubernetes manifest의 image 값을 GHCR 이미지로 변경하기

## 2. 실습 목표

FastAPI Mini Platform Kubernetes Deployment가 로컬 Docker 이미지가 아니라 GitHub Container Registry에 push된 Docker 이미지를 사용하도록 변경한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 클라우드 네이티브 방식으로 운영하려면 Kubernetes가 이미지 저장소에 올라간 이미지를 가져와 실행할 수 있어야 한다.

이번 실습은 CI/CD 흐름 중 아래 단계에 해당한다.

```text
코드 변경
→ GitHub Actions 테스트
→ Docker 이미지 자동 빌드
→ GHCR push
→ Kubernetes가 GHCR 이미지로 실행
```

## 4. 변경 전 이미지

```yaml
image: cnkl-fastapi-mini-platform:0.1.0
imagePullPolicy: IfNotPresent
```

## 5. 변경 후 이미지

```yaml
image: ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform:latest
imagePullPolicy: Always
```

## 6. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

kubectl config current-context
kubectl get nodes

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl rollout status deployment/fastapi-mini-platform

kubectl get pods
kubectl get svc
kubectl get endpoints fastapi-mini-platform-service

kubectl get deployment fastapi-mini-platform -o yaml | grep image:
```

port-forward 확인:

```bash
kubectl port-forward service/fastapi-mini-platform-service 8002:80
```

새 터미널에서 확인:

```bash
curl http://localhost:8002/health
curl http://localhost:8002/version

curl -X POST http://localhost:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes가 GHCR 이미지를 쓰면 뭐가 좋아요?"}' | python3 -m json.tool
```

## 7. 성공 확인 결과

- Deployment image 값이 GHCR 이미지로 변경됨
- `imagePullPolicy: Always` 설정 확인
- Kubernetes rollout 성공
- Pod 상태 `Running` 확인
- Service와 Endpoint 연결 확인
- `/health` 정상 응답 확인
- `/version` 정상 응답 확인
- `/ask` 정상 응답 확인
- `/docs` 접속 확인

## 8. 오늘 배운 점

1. Kubernetes는 로컬 이미지뿐 아니라 registry에 올라간 이미지를 가져와 실행할 수 있다.
2. GHCR은 GitHub에서 제공하는 Docker 이미지 저장소다.
3. `imagePullPolicy: Always`는 Kubernetes가 최신 이미지를 registry에서 확인하게 한다.
4. Kubernetes manifest의 image 값은 배포 대상 이미지를 결정하는 핵심 설정이다.
5. CI/CD에서 만든 이미지를 Kubernetes가 사용하면 운영 흐름이 더 자연스러워진다.

## 9. 다음 실습

Kubernetes manifest에 commit SHA 기반 이미지 태그 전략을 적용한다.
