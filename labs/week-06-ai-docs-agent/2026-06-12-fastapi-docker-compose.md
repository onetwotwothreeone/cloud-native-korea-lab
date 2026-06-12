# FastAPI Mini Platform Docker Compose Lab

## 1. 실습 제목

FastAPI Mini Platform을 Docker Compose로 실행하기

## 2. 실습 목표

긴 docker run 명령어 대신 docker-compose.yml 파일로 FastAPI Mini Platform 실행 설정을 관리한다.

## 3. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab/mini-platform

docker rm -f cnkl-fastapi-mini-platform 2>/dev/null || true
docker rm -f cnkl-fastapi-mini-platform-compose 2>/dev/null || true

docker compose -f compose/docker-compose.yml up -d --build

docker ps

curl http://localhost:8001/health
curl http://localhost:8001/version

curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes에서 Service는 왜 필요한가요?"}' | python3 -m json.tool

docker compose -f compose/docker-compose.yml logs
docker compose -f compose/docker-compose.yml down
## 4. 성공 확인 결과
Docker Compose로 FastAPI 이미지 빌드 성공
컨테이너 cnkl-fastapi-mini-platform-compose 실행 확인
0.0.0.0:8001->8000/tcp 포트 연결 확인
/health, /version, /ask, /docs 확인
## 5. 오늘 배운 점
Docker Compose는 긴 docker run 명령어를 YAML 파일로 정리해준다.
docker compose up -d --build는 빌드와 실행을 함께 처리한다.
docker compose down은 Compose로 만든 컨테이너와 네트워크를 정리한다.
## 6. 다음 실습

FastAPI Mini Platform을 Kubernetes Deployment와 Service로 실행한다.
