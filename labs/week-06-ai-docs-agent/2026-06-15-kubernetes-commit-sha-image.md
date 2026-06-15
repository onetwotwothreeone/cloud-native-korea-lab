# Kubernetes Commit SHA Image Tag Lab

## 1. 실습 제목

Kubernetes manifest에 commit SHA 기반 이미지 태그 전략 적용하기

## 2. 실습 목표

Kubernetes Deployment가 `latest` 태그가 아니라 GitHub Actions가 생성한 commit SHA 기반 GHCR 이미지를 사용하도록 변경한다.

## 3. 전체 프로젝트에서의 역할

Cloud Native AI Docs Agent를 실제 운영하려면 어떤 코드가 어떤 이미지로 배포되었는지 추적할 수 있어야 한다.

이번 실습은 CI/CD 흐름 중 아래 단계에 해당한다.

```text
코드 변경
→ GitHub Actions 테스트
→ Docker 이미지 자동 빌드
→ GHCR push
→ Kubernetes가 특정 commit SHA 이미지로 실행
```

## 4. 변경 전 이미지

```yaml
image: ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform:latest
imagePullPolicy: Always
```

## 5. 변경 후 이미지

```yaml
image: ghcr.io/onetwotwothreeone/cnkl-fastapi-mini-platform:77792278870bd6fe9a926e98ff2fba46c46f266a
imagePullPolicy: IfNotPresent
```

## 6. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/fastapi-mini-platform

kubectl get pods
kubectl get deployment fastapi-mini-platform -o yaml | grep image:
kubectl describe pod -l app=fastapi-mini-platform

kubectl get svc
kubectl get endpoints fastapi-mini-platform-service
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
  -d '{"question":"Kubernetes에서 commit SHA 이미지 태그를 쓰면 뭐가 좋아요?"}' | python3 -m json.tool
```

## 7. 성공 확인 결과

- Deployment image 값이 commit SHA 기반 GHCR 이미지로 변경됨
- `imagePullPolicy: IfNotPresent` 설정 확인
- Kubernetes rollout 성공
- Pod 상태 `Running` 확인
- `kubectl describe pod`에서 commit SHA 이미지 확인
- Service와 Endpoint 연결 확인
- `/health` 정상 응답 확인
- `/version` 정상 응답 확인
- `/ask` 정상 응답 확인
- `/docs` 접속 확인

## 8. 오늘 배운 점

1. `latest` 태그는 편하지만 정확한 배포 추적에는 약하다.
2. commit SHA 태그를 사용하면 어떤 코드가 어떤 이미지로 배포되었는지 추적할 수 있다.
3. Kubernetes manifest의 `image` 값은 배포 버전을 결정하는 핵심 설정이다.
4. CI/CD에서 만든 commit SHA 이미지를 Kubernetes가 사용하면 운영 안정성이 좋아진다.
5. 운영 환경에서는 `latest`보다 명확한 버전 태그 또는 commit SHA 태그가 더 안전하다.

## 9. 다음 실습

Kubernetes manifest를 환경별로 관리하기 위한 kustomize 기초 실습을 시작한다.
