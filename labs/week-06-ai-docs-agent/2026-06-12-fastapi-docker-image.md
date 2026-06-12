# FastAPI Mini Platform Docker Image Lab

## 1. 실습 제목

Python FastAPI Mini Platform을 Docker 이미지로 만들기

## 2. 실습 목표

FastAPI 기반 Mini Platform을 Docker 이미지로 빌드하고 컨테이너로 실행한다.

## 3. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

docker build -t cnkl-fastapi-mini-platform:0.1.0 .

docker images | grep cnkl-fastapi-mini-platform

docker rm -f cnkl-fastapi-mini-platform 2>/dev/null || true

docker run -d \
  --name cnkl-fastapi-mini-platform \
  -p 8001:8000 \
  cnkl-fastapi-mini-platform:0.1.0

docker ps

curl http://localhost:8001/health
curl http://localhost:8001/version

curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 Service는 왜 필요한가요?"}' | python3 -m json.tool
```

## 4. 성공 확인 결과

- Docker 이미지 `cnkl-fastapi-mini-platform:0.1.0` 생성 확인
- 컨테이너 `cnkl-fastapi-mini-platform` 실행 확인
- `0.0.0.0:8001->8000/tcp` 포트 연결 확인
- `/health`에서 `status: ok` 확인
- `/version`에서 Python, FastAPI 버전 응답 확인
- `/ask`에서 질문 JSON을 받고 예시 답변 반환 확인

## 5. 오늘 배운 점

1. FastAPI 앱도 Docker 이미지로 포장할 수 있다.
2. Dockerfile은 앱 실행 환경을 만드는 레시피다.
3. `-p 8001:8000`에서 앞은 내 MacBook 포트, 뒤는 컨테이너 내부 포트다.
4. Docker 이미지는 GitHub에 직접 올리는 것이 아니라, Dockerfile과 코드로 다시 만들 수 있게 관리한다.

## 6. 다음 실습

FastAPI Mini Platform을 Docker Compose로 실행한다.
