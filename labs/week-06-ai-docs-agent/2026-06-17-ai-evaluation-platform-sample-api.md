# AI Evaluation Platform Sample API Lab

## 1. 실습 제목

AI Evaluation Platform v0.1에 Sample API 추가하기

## 2. 실습 목표

AI Evaluation Platform에 실제 평가 대상이 되는 텍스트 또는 음성 메타데이터를 등록하는 Sample API를 추가한다.

## 3. 전체 프로젝트에서의 역할

기존 `mini-platform`은 클라우드 네이티브 기술을 익히기 위한 sandbox였다.

`ai-evaluation-platform`은 xAI 포트폴리오와 실제 서비스 확장을 위한 대표 프로젝트다.

이번 실습은 AI 평가 workflow 중 아래 단계에 해당한다.

```text
Task 생성
→ Sample 등록
→ Annotation 제출
→ Evaluation 점수 제출
→ review_required 표시
→ PostgreSQL 저장
```

## 4. 추가한 API

```text
POST /samples
GET  /samples
GET  /samples/{sample_id}
```

## 5. Sample 모델

```text
Sample
├── id
├── task_id
├── sample_type: text / audio
├── content
├── transcript
├── language
├── metadata
└── created_at
```

## 6. 만든 기능

- 존재하는 Task에 Sample 등록
- Sample 목록 조회
- Sample ID로 단일 Sample 조회
- 존재하지 않는 Task에 Sample 등록 시 404 반환
- 존재하지 않는 Sample 조회 시 404 반환

## 7. 실행한 명령어

```bash
cd ~/cloud-native-korea-lab

cat > ai-evaluation-platform/app/main.py
cat > ai-evaluation-platform/tests/test_main.py
```

README 업데이트:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path("ai-evaluation-platform/README.md")
text = path.read_text()
text = text.replace(
"""GET  /tasks
GET  /docs""",
"""GET  /tasks
POST /samples
GET  /samples
GET  /samples/{sample_id}
GET  /docs"""
)
path.write_text(text)
PY
```

테스트 실행:

```bash
cd ~/cloud-native-korea-lab/ai-evaluation-platform
python -m pytest
```

서버 실행:

```bash
uvicorn app.main:app --reload --port 8010
```

Task 생성:

```bash
curl -X POST http://localhost:8010/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evaluate Korean cloud native answer",
    "task_type": "text",
    "language": "ko",
    "description": "Evaluate clarity, accuracy, and naturalness."
  }' | python3 -m json.tool
```

Sample 생성:

```bash
curl -X POST http://localhost:8010/samples \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK_ID_HERE",
    "sample_type": "text",
    "content": "Kubernetes Service는 Pod에 안정적으로 접근하게 해주는 네트워크 입구입니다.",
    "language": "ko",
    "metadata": {
      "source": "synthetic",
      "domain": "cloud-native"
    }
  }' | python3 -m json.tool
```

Sample 목록 조회:

```bash
curl http://localhost:8010/samples | python3 -m json.tool
```

## 8. 성공 확인 결과

- `POST /samples` 정상 응답 확인
- `GET /samples` 정상 응답 확인
- `GET /samples/{sample_id}` 정상 응답 확인
- 존재하지 않는 Task ID로 Sample 생성 시 404 확인
- 존재하지 않는 Sample ID 조회 시 404 확인
- pytest 테스트 통과
- README 기능 목록 업데이트 완료
- GitHub push 완료

## 9. 오늘 배운 점

1. Task는 평가 프로젝트 폴더이고, Sample은 실제 평가할 데이터다.
2. Sample은 text 또는 audio 타입을 가질 수 있다.
3. text sample은 content를 중심으로 저장하고, audio sample은 transcript와 metadata를 함께 저장할 수 있다.
4. Sample은 반드시 특정 Task에 연결되어야 한다.
5. 잘못된 task_id를 받았을 때 404를 반환하면 API 사용자가 문제를 더 쉽게 이해할 수 있다.
6. in-memory 구조로 먼저 API 흐름을 검증한 뒤 PostgreSQL을 붙이는 방식이 안전하다.

## 10. 다음 실습

AI Evaluation Platform v0.1에 Annotation API를 추가한다.

다음 API 후보:

```text
POST /annotations
GET  /annotations
GET  /annotations/{annotation_id}
```
