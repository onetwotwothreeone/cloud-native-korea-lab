# Python FastAPI Mini Platform 전환 실습

## 오늘 한 일

Cloud Native Korea Lab Mini Platform을 Node.js 기반에서 Python FastAPI 기반으로 전환했다.

## 왜 바꿨는가?

KT-cloud Tech Up 교육에서 Python 3.13을 사용하고 있고, 앞으로 만들 AI Docs Agent는 공식 문서 수집, RAG, AI 답변 생성 기능이 필요하다.

운영 효율을 고려하면 Node.js와 Python을 함께 쓰는 것보다 Python 하나로 API 서버와 AI Agent를 구성하는 것이 더 단순하다.

## 변경 전

- Node.js
- Express
- server.js 기반 API

## 변경 후

- Python 3.13.13
- FastAPI
- Uvicorn
- app/main.py 기반 API

## 만든 API

- GET /
- GET /health
- GET /version
- POST /ask

## 확인한 주소

- http://localhost:8000
- http://localhost:8000/health
- http://localhost:8000/version
- http://localhost:8000/docs

## 테스트한 명령어

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Kubernetes Pod가 무엇인가요?"}'
성공 결과

FastAPI 서버가 정상 실행되었고, /ask API가 질문 JSON을 받아 예시 답변 JSON을 반환했다.

헷갈렸던 부분
/ask는 POST API라서 브라우저 주소창으로 접근하면 405 Method Not Allowed가 나온다.
/favicon.ico 404는 브라우저가 아이콘을 찾는 과정에서 생기는 것이므로 현재 실습에서는 문제 아니다.
.venv는 개인 로컬 가상환경이므로 GitHub에 올리지 않는다.
배운 점
프로젝트 초반에는 기술을 많이 쓰는 것보다 최소 기술로 끝까지 운영해보는 것이 중요하다.
Python 버전은 교육 환경과 맞추는 것이 안전하다.
FastAPI는 Python으로 API 서버를 빠르게 만들 수 있게 도와준다.
FastAPI는 /docs 화면에서 API 문서를 자동으로 만들어준다.
기존 Node.js 실습은 삭제하지 않고 legacy 기록으로 보관했다.
다음 할 일
Dockerfile 작성 또는 점검
Docker 이미지 빌드
Docker Compose 구성
Kubernetes Deployment 작성
Kubernetes Service 작성
