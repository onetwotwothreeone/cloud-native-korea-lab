# 설계 변천사 (Design History)

> Cloud Native Korea Lab 저장소의 설계가 어떻게 변해 왔는지를 git 히스토리 전체(커밋 168개)를 분석해 정리한 문서입니다.
> 폐기됐다 부활한 아이디어(♻️)와 일관성이 깨진 지점(⚠️)을 함께 표시합니다.

- 분석 대상: `git log` 전체, 168 commits
- 기간: 2026-06-06 → 2026-06-25 (약 3주)
- 작성 기준일: 2026-06-25
- 작성자 식별자: `Sol Kim <skthf9@gmail.com>` (96) + `onetwotwothreeone <noreply@github>` (72) — 동일인의 서로 다른 git identity (아래 ⚠️-7 참조)

> **명칭 정의 (Canonical Naming)**: 본 문서에서 **HYEAN/GWAN**으로 부르는 시스템은 곧 **이동형 지구 우주 항법 시스템 (Mobile Earth Navigation System)** 이다. 세 표현은 동일한 대상을 가리키며, 프로젝트 공식 명칭은 루트 [`CLAUDE.md`](../CLAUDE.md)에 정의되어 있다. 아래 본문은 git 히스토리에 실제 기록된 명칭(HYEAN/GWAN)을 그대로 사용한다.

---

## 1. 한눈에 보는 변천 흐름

```text
클라우드 네이티브 학습 scaffolding   (06-06)
  → Node.js mini-platform           (06-08)
  → AI Docs Agent + RAG 구상         (06-10~11)
  → Node → Python FastAPI 전환 (PR#1) (06-12)   ← 첫 번째 큰 피벗
  → FastAPI 위에 Docker/Compose/K8s/Kustomize/CI/GHCR 체인 구축 (06-12~16)
  → xAI 커리어 피벗 + ai-evaluation-platform를 "대표 포트폴리오"로 선언 (06-17~18) ← 두 번째 큰 피벗
  → HYEAN / GWAN 우주 시뮬레이션 백엔드 등장 (06-22)                            ← 세 번째 큰 피벗
  → GWAN Kubernetes 하드닝 (관측성/리소스/HPA/PDB/NetworkPolicy/RBAC/SecurityContext) (06-23~24)
  → GWAN StatefulSet 마이그레이션 "승인 의식" 대장정 (06-24~25)
```

세 번의 큰 방향 전환(피벗)이 있었고, 매번 이전 산출물을 **삭제하지 않고 보존**하는 정책을 따랐습니다. 그 결과 학습 기록으로서의 가치는 높지만, "현재의 대표 프로젝트가 무엇인가"에 대한 문서와 실제 작업량이 어긋나는 지점들이 생겼습니다(2·5절).

---

## 2. 단계별 설계 변천

### Phase 0 — 클라우드 네이티브 학습 저장소 scaffolding (2026-06-06 ~ 06-08)
- `9812d53 Initial cloud native lab structure`로 시작.
- `labs/`, `notes/`, `error-logs/`, `content/`, `roadmap/` 등 학습 기록용 디렉터리와 템플릿 위주.
- 첫 실습: Docker Nginx 컨테이너 (`ff09dac`), Docker 컨테이너 라이프사이클 기록.
- **설계 의도**: 주차별(week-XX) 클라우드 네이티브 실습 로그 저장소.

### Phase 1 — Node.js mini-platform (2026-06-08)
- `mini-platform`을 **Node.js + Express**로 시작 (`0bcf060`, `06e2869` "Add mini platform server", `server.js`).
- Dockerfile, docker-compose, k8s `deployment.yaml`/`service.yaml`, 그리고 `helm/`, `gitops/`, `cicd/`, `monitoring/`, `terraform/` **빈 placeholder** 디렉터리(`.gitkeep`)를 대량 생성.
- **설계 의도**: "풀스택 클라우드 네이티브 플랫폼"의 골격을 미리 잡아두기. (이 placeholder들은 나중에 거의 채워지지 않고 legacy로 이동 — ⚠️-3)

### Phase 2 — "AI Docs Agent" + RAG 구상 (2026-06-10 ~ 06-11)
- `0511b28 Update mini platform goal to AI docs agent` — mini-platform의 목표가 **범용 플랫폼 → "Cloud Native AI Docs Agent"**로 변경.
- agent 규칙 도입: `agent/prompt.md`, `system-rules.md`, `answer-template.md`.
- **RAG 파이프라인 설계 문서 3종** 추가: `rag/ingest.md`, `rag/retrieval.md`, `rag/citations.md` (`6c519f1`, `f51b57f`, `b0c6d26`).
- `99ac686 Add ask API for cloud native docs agent` — Node 서버에 `/ask` 엔드포인트.
- **설계 의도**: 클라우드 네이티브 문서를 RAG로 검색·인용해 답하는 에이전트. → 이 RAG 구상은 곧 동결됩니다 (♻️-1).

### Phase 3 — Node → Python FastAPI 전환 (2026-06-12, PR #1) ★ 첫 번째 큰 피벗
- 브랜치 `refactor/python-fastapi-mini-platform` → `8f3d89b Merge pull request #1`.
- 핵심 커밋 `ffb1bb2 Refactor mini platform to Python FastAPI`:
  - 기존 Node 구현 전체를 **`labs/legacy/node-mini-platform-v0/`로 이동(rename)** — 삭제가 아닌 보존.
  - 새 `mini-platform/app/main.py` (FastAPI) + `requirements.txt` 신설.
- 전환 근거는 `labs/week-04-python-fastapi/2026-06-12-python-fastapi-transition.md`에 기록.
- **설계 의도**: 언어 스택을 Python으로 통일(AI/데이터 평가 친화). 이때 RAG 설계 문서도 legacy로 함께 묻힘 (♻️-1).

### Phase 4 — FastAPI 위 클라우드 네이티브 전달 체인 (2026-06-12 ~ 06-16)
- Dockerfile → docker-compose → Kubernetes manifests → readiness/liveness probe.
- GitHub Actions CI (`fastapi-ci.yml`), Docker 이미지 빌드 잡, **GHCR 푸시**.
- 이미지 태그 전략 진화: `latest` → **GHCR 이미지** → **commit SHA 태그**(`5c4eeac`).
- **Kustomize 도입**: base + dev/prod overlay, dev/prod **namespace 분리**, prod replicas/리소스 한도.
- **설계 의도**: 작은 FastAPI 앱을 "운영처럼" 빌드·배포하는 표준 파이프라인 확립. (이 단계가 이후 GWAN에 그대로 재사용됨)

### Phase 5 — xAI 커리어 피벗 + ai-evaluation-platform "대표 포트폴리오" 선언 (2026-06-17 ~ 06-18) ★ 두 번째 큰 피벗
- `onetwotwothreeone` identity가 전략 문서들을 대량 투입:
  - `docs/career/integrated-xai-strategy.md`, `xai-roadmap.md`, `portfolio-first-service-next.md`.
  - `portfolio/xai/korean-voice-data-evaluation/README.md` (한국어 음성 데이터 평가 포트폴리오).
  - `docs/automation/codex-apply-xai-integration.md` + `AGENTS.md` (Codex 자동화 워크플로우).
- **프로젝트 정체성 재정의** (`092b11b`, README): 
  - `mini-platform = practice sandbox` (연습장으로 강등)
  - `ai-evaluation-platform = flagship portfolio` (대표작으로 승격)
- `366bb91 Add AI evaluation platform FastAPI skeleton` + Sample API.
- **"Top-down Completion Principle"** 도입 (`5207114`, `ff73e26`): 완성형을 먼저 정의하고 역순으로 작업.
- **설계 의도**: 저장소를 "학습 로그"에서 "xAI 지원용 포트폴리오 + 한국어 AI 평가 서비스"로 재포지셔닝.
- ⚠️ 그러나 선언된 flagship(`ai-evaluation-platform`)은 이후 **단 3개 커밋**에 그치고 skeleton 상태로 정체됨 (⚠️-1).

### Phase 6 — HYEAN / GWAN 시뮬레이션 백엔드 등장 (2026-06-22) ★ 세 번째 큰 피벗
- `a6af4e2 Add HYEAN GWAN simulation integration with CI` — `hyean-gwan/simulation-integration/` 라는 **완전히 새로운 도메인**이 한 번에 투입(자체 AGENTS.md, codex 프롬프트, docs, tests 포함).
- 도메인 정의(README): **HYEAN** = 이동형 우주 거주지를 위한 생존 지향 우주 지능 서비스, **GWAN** = 그 안의 관측·해석·점수·결정·기억 엔진. 이 HYEAN/GWAN 시스템 전체가 곧 **이동형 지구 우주 항법 시스템(Mobile Earth Navigation System)** 이다 (CLAUDE.md 기준 공식 명칭).
- 작업 방식: **Codex 프롬프트 → docs 단계 문서 → 구현/테스트**를 번호(09, 10, 11 …)로 이어가는 파이프라인.
- **설계 의도**: Phase 4에서 익힌 클라우드 네이티브 전달 체인을, 추상적인 "AI 평가 플랫폼" 대신 구체적 스토리(우주 생존 엔진) 위에서 끝까지 구현.
- ⚠️ GWAN은 이후 저장소에서 **가장 활발한 프로젝트(71 commits)**가 되지만, 루트 README의 "Current Core Projects"에는 **등재되지 않음** (⚠️-2).

### Phase 7 — GWAN Kubernetes 하드닝 (2026-06-23 ~ 06-24)
- 단계 19~38: CI → Docker 빌드 → Compose CI → GHCR → manifests → local/prod overlay → kind CI → 관측성 → 리소스 requests/limits → namespace 정책 → **HPA → metrics server → HPA behavior → PodDisruptionBudget → NetworkPolicy → ServiceAccount RBAC → SecurityContext**.
- `11b1d5d Align GWAN implementation with HYEAN prevention layer` — `35_2`로 끼워 넣은 정렬 단계(번호 체계 일탈 — ⚠️-5).
- **설계 의도**: GWAN을 "프로덕션급 K8s 워크로드"처럼 보이도록 운영 기능을 순차 적층.

### Phase 8 — GWAN StatefulSet 마이그레이션 "승인 의식" 대장정 (2026-06-24 ~ 06-25)
- 단계 39~74(약 30단계 이상)가 **PostgreSQL을 Deployment → StatefulSet으로 옮기는 단일 마이그레이션** 하나에 집중.
- 흐름: persistence baseline → StatefulSet 설계 리뷰 → 마이그레이션 플랜 → backup/restore → draft manifest → dry run → runbook → rollback dry run → cutover checklist → **decision gate → approval record → operator approval template → manual approval record → approval gate → premigration final check → final approval review → go/no-go → execution plan → command dry run → command review → risk register → risk mitigation → pre-execution safety snapshot → backup freshness → data integrity → readiness summary → operator final approval → final approval gate → final preflight → portfolio demo readiness → demo script → demo readme → final verification**.
- `773cb22 Add GWAN judgment model v0.1`로 마무리(현재 HEAD).
- ⚠️ 실제 한 줄짜리 로컬 마이그레이션에 **엔터프라이즈급 승인 절차가 과잉 적층**됨. "Fix … wording" 류 미세 수정 커밋만 6건, 전체 `Fix` 커밋 20건 (⚠️-4).

---

## 3. ♻️ 폐기됐다가 (부분) 부활했거나, 폐기된 채 남은 아이디어

| # | 아이디어 | 도입 | 폐기/동결 | 부활 여부 |
|---|----------|------|-----------|-----------|
| ♻️-1 | **RAG 파이프라인** (`rag/ingest·retrieval·citations.md`, `/ask`) | Phase 2 (06-11, Node AI Docs Agent용) | Phase 3에서 Node와 함께 `labs/legacy/`로 이동 | **미부활**. 현재 루트 README도 "`/ask`는 실제 AI/RAG 연결 전 단계, 고정 예시 응답"이라고 명시 — 구상만 남고 구현은 계속 보류 중인 **동결 아이디어**. |
| ♻️-2 | **"AI Docs Agent" 콘셉트** | Phase 2 | Phase 5에서 "ai-evaluation-platform"에 사실상 흡수 | mini-platform의 `/ask` 설명에만 흔적으로 잔존. 대표 콘셉트 자리에서는 폐기. |
| ♻️-3 | **빈 인프라 placeholder** (`helm/`, `gitops/`, `cicd/`, `monitoring/`, `terraform/`) | Phase 1 (06-08, Node) | 채워지지 않은 채 legacy로 이동 | GWAN에서 동일 개념(CI/관측성/리소스)이 **다른 형태로 재구현**됨. 원래 placeholder는 미부활. |
| ♻️-4 | **StatefulSet "Cutover Decision Gate" (49단계)** | — | 50~53단계를 먼저 만든 뒤 **빠진 것을 뒤늦게 발견** | `b1b2019 Add missing StatefulSet cutover decision gate`로 **순서를 거슬러 소급 추가**. 누락 후 부활한 단계. |
| ♻️-5 | **GWAN API DB 환경변수 계약** | 초기 GWAN | — | `34e2a52 Restore GWAN API database env contract` — 제목은 "Restore"지만 실제로는 39단계(Config/Secret 분리) **신규 리팩터링**. 되살린 게 아니라 **재정의** (⚠️-6의 wording 문제와 연결). |

---

## 4. ⚠️ 일관성이 깨진 지점

**⚠️-1. 선언된 "flagship"과 실제 작업량의 불일치**
- 루트 README는 `ai-evaluation-platform = flagship portfolio`라고 선언(Phase 5).
- 그러나 실제 커밋 분포는: `ai-evaluation-platform` **3 commits** vs `hyean-gwan(GWAN)` **71 commits** vs `mini-platform` **42 commits**.
- 즉 문서상 대표작은 거의 정체돼 있고, 실질 주력은 문서가 거의 언급하지 않는 GWAN.

**⚠️-2. GWAN이 루트 README에 미등재**
- 가장 활발한 프로젝트(GWAN/hyean-gwan)가 루트 README "Current Core Projects"에 없음(mini-platform·ai-evaluation-platform만 등재).
- 신규 방문자는 저장소의 실제 주력을 README만 보고는 알 수 없음.

**⚠️-3. mini-platform 목표의 잦은 재정의**
- `범용 mini-platform`(P1) → `AI Docs Agent`(P2) → `FastAPI 연습장`(P3) → `practice sandbox로 강등`(P5).
- "beginner-friendly accuracy principle"이 **3번 중복 추가**됨(`ce27fba` 루트, `8038eee` 루트/mini, `51e803d` mini) — 같은 원칙이 여러 README에 산발 복제.

**⚠️-4. StatefulSet 마이그레이션의 프로세스 과적층**
- 단일 로컬 PostgreSQL 마이그레이션에 decision gate / approval record / operator approval / final approval / preflight / readiness 등 **승인·게이트 단계가 ~30개** 누적.
- `Fix … wording` 6건 등 미세 문구 수정 반복 → 산출물 본질보다 절차 문서의 워딩에 churn이 집중.
- 포트폴리오 데모 규모 대비 절차가 과대(엔터프라이즈 변경관리 흉내).

**⚠️-5. 단계 번호 체계의 불연속**
- 정수 시퀀스에 `35_2_HYEAN_GWAN_Prevention_Layer_Alignment`처럼 **소수점 끼워넣기**.
- 49단계(decision gate)는 50~53 이후 **소급 삽입**(♻️-4).

**⚠️-6. Codex 프롬프트 ↔ docs 파이프라인의 단절**
- 초기 규율은 "Codex 프롬프트(`codex/NN_*.md`) → 단계 문서(`docs/NN_*.md`) → 구현".
- 그러나 `codex/`는 09~53(+34·35·49 누락)과 61·62까지만 존재하고, `docs/`는 **74까지** 존재.
- 즉 **53단계 이후 Codex 프롬프트 작성 규율이 사실상 폐기**되고 docs만 단독 진행 → 초기 워크플로우 약속이 후반부에 깨짐.

**⚠️-7. README 단편 파일 누적(append 워크플로우의 잔재)**
- 루트에 `README_20_APPEND.md … README_31/33_APPEND.md`가 **고아 파일**로 남음. 내용은 GWAN 20·31·33단계 설명 — 즉 **GWAN 문서가 루트로 새어 나와** 본 README에 병합되지 못한 조각들.
- 이후 같은 패턴이 `hyean-gwan/.../README_41_APPEND.md`로 자리만 옮겨 반복 → README 구성 방식이 통일되지 않음.

**⚠️-8. git author identity 이원화**
- 동일인이 `Sol Kim <skthf9@gmail.com>`(96)과 `onetwotwothreeone <noreply@github>`(72)로 분리 커밋.
- 대체로 **코드/CI 변경 = Sol Kim**, **문서/전략/GitHub 웹 편집 = onetwotwothreeone** 경향. 블레임·기여도 추적 시 혼선 소지.

**⚠️-9. "Restore"라는 커밋 제목의 부정확성**
- `34e2a52 Restore GWAN API database env contract`는 실제로 **신규 Config/Secret 분리(39단계)** 작업 → 제목과 내용 불일치(♻️-5).

---

## 5. 종합 평가

- **강점**: 모든 피벗에서 이전 결과물을 보존(legacy 이동) → 학습 기록·증거로서 일관됨. 클라우드 네이티브 전달 체인(Docker→Compose→K8s→Kustomize→CI→GHCR→HPA→StatefulSet)을 두 프로젝트(mini-platform, GWAN)에 걸쳐 반복 숙달한 흔적이 뚜렷.
- **약점**: 문서가 선언하는 "대표 프로젝트"와 실제 주력(GWAN)의 괴리(⚠️-1·2), 후반부 프로세스 과적층(⚠️-4), 초기 워크플로우 규율(Codex 프롬프트, RAG)의 미완·단절(⚠️-6·♻️-1).

### 정합성 회복을 위한 제안(선택)
1. 루트 README "Current Core Projects"에 **GWAN을 명시적으로 등재**하고, ai-evaluation-platform의 현재 상태(skeleton)를 솔직히 표기 — ⚠️-1·2 해소.
2. 루트의 `README_NN_APPEND.md` 고아 파일들을 해당 README에 병합하거나 제거 — ⚠️-7 해소.
3. RAG/`/ask`의 현재 위치를 "보류/동결"로 명문화하거나 로드맵에서 정식 항목으로 복원 — ♻️-1 해소.
4. git `user.name`/`user.email`을 하나로 통일 — ⚠️-8 해소.

---

*이 문서는 `git log` 분석 시점(2026-06-25, HEAD `773cb22`) 기준이며, 이후 커밋에는 자동 반영되지 않습니다.*
