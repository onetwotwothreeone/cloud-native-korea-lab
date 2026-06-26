# 재정렬 백로그 (Realignment Backlog)

> 맥락([PHILOSOPHY](PHILOSOPHY.md) · [DECISIONS](DECISIONS.md) · [CONTEXT](CONTEXT.md))과 실제 코드 사이의 불일치를 **심각도(High/Medium/Low)** 순으로 정리한 실행 체크리스트.
> 근거 분석: [CONTEXT_VS_CODE.md](CONTEXT_VS_CODE.md). 설계 이력: [DESIGN_HISTORY.md](DESIGN_HISTORY.md).
> 심각도 기준 — **High**: 명문화된 원칙 위반 또는 핵심 정체성/신뢰성 직결. **Medium**: 비전 미반영이나 v0.1 범위에서 다룰 수 있음. **Low**: 문서/편의/명명 수준.

작업 규칙: 항목 착수 전 [CLAUDE.md](../CLAUDE.md)에 따라 관련 모듈과 본 백로그를 먼저 읽고, 기존 결정과 충돌 시 충돌을 먼저 명시·확인받을 것.

---

## 🔴 High

- [ ] **H1. Kubernetes/StatefulSet 과적층이 "보류 원칙"과 정반대** — *원칙 위반 (가장 큰 충돌)*
  - 근거: [CONTEXT](CONTEXT.md) 3.5·3.13·4.14는 "K8s 과도한 고도화", "실제 StatefulSet 운영 전환", "처음부터 K8s 중심 구현"을 보류/금지로 명시. 그러나 GWAN 단계 23~74 대부분이 K8s, StatefulSet 마이그레이션에 ~30단계 승인 절차 축적.
  - 제안 액션: (a) 이 일탈을 **의식적 결정으로 명문화**할지(학습 목적이었음을 [DESIGN_HISTORY](DESIGN_HISTORY.md)에 기록) vs (b) StatefulSet 승인 의식 단계들을 **포트폴리오 데모로 격리**하고 핵심 경로에서 분리할지 결정. 추가 K8s 고도화는 동결.
  - 관련: `hyean-gwan/simulation-integration/{k8s,scripts/k8s,docs/4x~7x}`

- [ ] **H2. 예방 레이어(Prevention Layer)가 문서만 존재, 코드 미구현** — *핵심 정체성 미반영 + 테스트 착시*
  - 근거: [DECISIONS](DECISIONS.md) 2.16 / [CONTEXT](CONTEXT.md) 4.9가 요구한 `trend_score, imbalance_score, early_warning_score, preventive_action_priority, prevention_status` 가 코드에 없음. 테스트 `test_gwan_prevention_layer_alignment.py`는 마크다운에 단어가 있는지만 검사 → 구현됐다는 착시.
  - 제안 액션: 예방 점수 필드를 `gwan_judgment` 또는 신규 `prevention.py`에 실제 구현 + `prevention_status`(normal/watch/adjust/restrict/shelter_or_abort) 산출 + 값 검증 테스트 추가. 정렬 테스트를 "문서 존재"가 아닌 "동작 검증"으로 강화.
  - 관련: `app/services/gwan_judgment.py`, `tests/test_gwan_prevention_layer_alignment.py`

- [ ] **H3. 결정 엔진 이중화 — `gwan_scoring` vs `gwan_judgment`** — *일관성/신뢰성 위험*
  - 근거: 두 모듈이 모두 행동을 추천하나 입력 스키마가 다름(6점수 입력 vs 8원신호 입력). 맥락의 단일 계약과도 둘 다 어긋남.
  - 제안 액션: 두 엔진의 역할 경계를 문서화하고(예: judgment=원신호→점수, scoring=점수→행동) 한 쪽이 다른 쪽을 호출하도록 통합하거나, 하나를 정식 경로로 지정하고 나머지를 deprecate.
  - 관련: `app/services/gwan_scoring.py`, `app/services/gwan_judgment.py`, `app/api/routes_gwan.py`

- [ ] **H4. 판단 모델 입출력 계약이 문서와 불일치** — *계약 일관성*
  - 근거: [CONTEXT](CONTEXT.md) 4.8 입력/출력 필드명과 실제 `GWANJudgmentInput/Result` 불일치(`prevention_status`→`severity`, `human_review_required`→`requires_human_review`, 입력에 `data_classification` 없음).
  - 제안 액션: 문서를 코드에 맞추거나(역방향) 코드를 문서 계약에 맞춰 정렬. **단일 출처**(Data Contract)를 정하고 양쪽을 동기화. `data_classification`을 판단 입력에 포함할지 결정.
  - 관련: `app/services/gwan_judgment.py`, [CONTEXT.md](CONTEXT.md) 4.8

---

## 🟡 Medium

- [ ] **M1. HYEAN 8개 시스템 모듈 구조 부재** — 특히 Spectral Intelligence / Micro-Probe / Position
  - 근거: [DECISIONS](DECISIONS.md) 2.4. 코드는 GWAN 엔진 중심이고 8시스템 모듈 경계가 없음. `spectrum_summary`는 단순 옵션 문자열.
  - 제안 액션: v0.1 범위에서 최소한 **시스템 경계를 문서/패키지 네임스페이스로 표현**(전체 구현 아님). 분광은 [CONTEXT](CONTEXT.md) 4.4 학습 경로부터.

- [ ] **M2. 시나리오 fixtures(sim_001~sim_006) 부재** — 시나리오 검증 공백
  - 근거: [CONTEXT](CONTEXT.md) 4.11. 실제는 `sample_gwan_simulation_request.json`, `gwan_scoring_cases.json`만 존재.
  - 제안 액션: 6개 명명 fixture 생성 + 각 fixture의 판단 규칙(자원↑·위험↑→접근금지, 불확실↑→추가관측, missing→human_review 등) 검증 테스트.
  - 관련: `tests/fixtures/`

- [ ] **M3. 엔드포인트 명명/누락** — `/gwan/schema`, `/gwan/reports/{report_id}` 없음, health 위치 상이
  - 근거: [CONTEXT](CONTEXT.md) 4.10. health가 `/gwan/health`가 아닌 `/health`.
  - 제안 액션: `/gwan/schema`(계약 노출), `/gwan/reports/{report_id}` 추가 또는 문서에서 제외. health 경로 정책 확정.
  - 관련: `app/api/routes_gwan.py`, `app/main.py`

- [ ] **M4. Onboard/Ground/Cloud 분리 + Sync Layer 아키텍처 미반영**
  - 근거: [DECISIONS](DECISIONS.md) 2.9. 현재 sync는 JSONL↔DB 동기화이지, 온보드 오프라인 생존지도/긴급 로컬 감지 분리가 아님.
  - 제안 액션: v0.1에서는 **아키텍처 의도를 문서로 고정**하고, 온보드 경로는 추후. 현재 sync의 의미를 오해 없게 명명/주석.

---

## 🟢 Low

- [ ] **L1. `severity` ↔ `prevention_status` 네이밍 정합** — H2 해결 시 함께 정리(`abort` vs `shelter_or_abort` 포함).
- [ ] **L2. GWAN 5레이어 중 Data Intake / Interpretation Layer 명시 모듈 부재** — 암묵 처리로 충분한지 판단 후, 필요 시 주석/모듈 경계만 표시.
- [ ] **L3. Space Data Source Map 문서 미작성** ([CONTEXT](CONTEXT.md) 4.3) — 공개 데이터 분류표 작성.
- [ ] **L4. Spectroscopy Learning Path 문서 미작성** ([CONTEXT](CONTEXT.md) 4.4) — 초보자용 분광 학습 경로.
- [ ] **L5. Operator Interface mockup/UI 미작성** ([CONTEXT](CONTEXT.md) 4.12) — *의도된 보류와 부합*. 착수 우선순위 낮음, 보류 상태임을 README에 명시.

---

## 우선순위 제안

1. **H2 + H4 + L1**를 한 묶음으로 — 예방 레이어를 실제 구현하면서 판단 계약을 단일화(가장 높은 정체성 가치, 코드 규모 적정).
2. **H3** — 결정 엔진 이중화 정리(H2/H4와 같은 파일을 건드리므로 연계).
3. **H1** — K8s/StatefulSet 일탈을 "의식적 결정"으로 명문화할지 결정(코드 변경보다 기록/격리 위주).
4. 이후 **M1~M4**, 마지막으로 **L3~L5** 문서 보강.
