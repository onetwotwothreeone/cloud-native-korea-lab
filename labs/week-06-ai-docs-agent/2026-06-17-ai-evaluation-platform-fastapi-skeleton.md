# AI Evaluation Platform FastAPI Skeleton Lab

## 1. 실습 제목

AI Evaluation Platform v0.1 FastAPI 프로젝트 골격 만들기

## 2. 실습 목표

Cloud Native Korea Lab의 대표 포트폴리오 프로젝트인 `ai-evaluation-platform`의 FastAPI 기본 구조를 만든다.

이번 실습에서는 AI 평가 플랫폼의 가장 첫 API인 Task 생성/조회 기능을 만든다.

## 3. 전체 프로젝트에서의 역할

기존 `mini-platform`은 Docker, Kubernetes, GitHub Actions, GHCR, Kustomize 등을 연습하기 위한 sandbox였다.

이번 실습부터는 xAI 포트폴리오와 실제 서비스 확장을 위한 대표 프로젝트인 `ai-evaluation-platform`을 시작한다.

```text
mini-platform = practice sandbox
ai-evaluation-platform = flagship portfolio
```

AI Evaluation Platform은 AI 데이터 평가, annotation, human feedback, quality scoring, review workflow를 관리하는 클라우드 네이티브 플랫폼으로 발전시킬 예정이다.

## 4. 만든 API

```text
GET  /
GET  /health
GET  /version
POST /tasks
GET  /tasks
GET  /docs
```

## 5. 만든 폴더 구조

```text
ai-evaluation-platform
├── README.md
├── requirements.txt
├── pytest.ini
├── app
│   ├── __init__.py
│   └── main.py
└── tests
    └── test_main.py
```

## 6. Task 모델

```text
Task
├── id
├── title
├── task_type: text / audio
├── language
├── status: open / closed
├── description
└── created_at
```

## 7. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab

mkdir -p ai-evaluation-platform/app
mkdir -p ai-evaluation-platform/tests
touch ai-evaluation-platform/app/__init__.py
```

requirements 생성:

```bash
cat > ai-evaluation-platform/requirements.txt
```

FastAPI 앱 생성:

```bash
cat > ai-evaluation-platform/app/main.py
```

pytest 설정 생성:

```bash
cat > ai-evaluation-platform/pytest.ini
```

테스트 코드 생성:

```bash
cat > ai-evaluation-platform/tests/test_main.py
```

로컬 테스트 실행:

```bash
cd ~/cloud-native-korea-lab/ai-evaluation-platform

pip install -r requirements.txt
python -m pytest
```

로컬 서버 실행:

```bash
uvicorn app.main:app --reload --port 8010
```

API 확인:

```bash
curl http://localhost:8010/health
curl http://localhost:8010/version
```

Task 생성:

```bash
curl -X POST http://localhost:8010/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evaluate Korean AI Tutor response",
    "task_type": "text",
    "language": "ko",
    "description": "Check clarity, accuracy, and naturalness."
  }' | python3 -m json.tool
```

Task 목록 조회:

```bash
curl http://localhost:8010/tasks | python3 -m json.tool
```

브라우저 확인:

```text
http://localhost:8010/docs
```

## 8. 성공 확인 결과

- `ai-evaluation-platform` 폴더 생성
- FastAPI 앱 생성
- `/health` 정상 응답 확인
- `/version` 정상 응답 확인
- `POST /tasks` 정상 응답 확인
- `GET /tasks` 정상 응답 확인
- `/docs` 자동 API 문서 확인
- pytest 테스트 통과
- README 작성 완료

## 9. 오늘 배운 점

1. `mini-platform`은 연습장이고, `ai-evaluation-platform`은 대표 포트폴리오 프로젝트다.
2. AI 평가 플랫폼의 첫 출발은 평가 작업 Task를 생성하고 조회하는 API다.
3. Task는 평가할 샘플, annotation, evaluation을 묶는 기준 단위가 된다.
4. 처음부터 DB를 붙이지 않고 in-memory 구조로 API 흐름을 먼저 검증할 수 있다.
5. FastAPI와 pytest를 함께 사용하면 API 구조를 빠르게 검증할 수 있다.
6. README는 프로젝트의 목적, 현재 기능, 실행 방법, 다음 단계를 보여주는 첫 화면이다.

## 10. 다음 실습

AI Evaluation Platform v0.1에 Sample API를 추가한다.

다음 API 후보:

```text
POST /samples
GET  /samples
GET  /samples/{sample_id}
```

Sample은 실제로 평가할 텍스트나 음성 메타데이터를 등록하는 단위다.
