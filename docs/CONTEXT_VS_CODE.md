# 맥락 ↔ 실제 코드 비교 (Context vs Code)

> ChatGPT에서 이관한 프로젝트 맥락([PHILOSOPHY.md](PHILOSOPHY.md) · [DECISIONS.md](DECISIONS.md) · [CONTEXT.md](CONTEXT.md))과 실제 레포 코드(`hyean-gwan/simulation-integration/`)를 대조한 결과.
> 대상 시스템: HYEAN/GWAN = 이동형 지구 우주 항법 시스템(Mobile Earth Navigation System).
> 작성 기준: HEAD 기준 코드 스냅샷. 실행 가능한 재정렬 작업 목록은 [REALIGNMENT_BACKLOG.md](REALIGNMENT_BACKLOG.md) 참조.

---

## 0. 한 줄 종합

> 실제 빌드는 **"수단"인 Cloud Native**(메모리 영속화·PostgreSQL·StatefulSet·K8s 운영)에 **과투자**되어 맥락이 요구한 수준을 넘어선 반면, **"정체성"인 HYEAN 8시스템·예방 레이어·분광 지능에는 코드가 거의 없다.** 이는 [DECISIONS.md](DECISIONS.md) 2.8 *"Cloud Native는 정체성이 아니라 수단"* 원칙이 실제로는 뒤집힌 상태임을 보여준다.

---

## 1. ✅ 일치 (맥락대로 구현됨)

주로 Data Contract / Operator Interface 영역에서 일치도가 높다.

| 맥락 항목 | 코드 위치 | 상태 |
|-----------|-----------|------|
| Data Contract enum 7종 (DECISIONS 2.14) | `app/schemas/gwan_interface.py` | **정확히 일치** (+ `AlertCategory`, `RangeScale` 추가) |
| Operator Interface 5개 패키지 (2.11) | `GWANOutputPackages` | spatial / sidebar / alert_feed / uncertainty / decision_report 모두 구현 |
| 검증 규칙 (2.15) | `gwan_interface.py` model_validator | object_id 교차참조, AU/km 혼용 금지(`Position3D`), score 0~1, 불확실시 reason 필수, reasoning_steps 필수 모두 구현 |
| 6개 점수 체계 (2.6) | `Scores` 모델 | energy/resource/risk/exploration_value/uncertainty/survival_priority 6개 모두 존재 |
| recommended_action 8값 (2.7) | `RecommendedAction` enum | 정확히 일치 |
| GWAN v0.1 rule-based 한정 (CONTEXT 3.5) | `app/services/gwan_judgment.py` | docstring `"This module is not a deep learning model."` 명시 ✅ |
| Safety Gate + Reason Codes + Human Review Flag (3.6) | `gwan_judgment.py` | `blocked_by_safety_gate`, `reason_codes`, `requires_human_review` 구현 |
| synthetic/simulated 한정, 실센서 없음 (3.4) | 전체 | 합성 시나리오만 사용, 실제 센서 연동 없음 ✅ |
| JSONL → PostgreSQL 메모리 흐름 (3.14) | `gwan_memory*`, `routes_gwan.py` | **맥락이 "다음 단계"로 둔 것보다 더 많이 구현됨** (영속화·DB·sync 엔드포인트 다수) |

> 참고: 메모리/영속화/DB/sync는 맥락(CONTEXT 4.10)이 "초기에는 DB 없이 → JSONL → PostgreSQL 순서로 확장"이라며 **미래 작업**으로 둔 항목인데, 실제로는 이미 완성되어 있다. 구현이 맥락보다 **앞서 있는** 영역이다.

---

## 2. ⚠️ 불일치 (맥락 ≠ 코드)

### 2.1 예방 레이어가 "문서만 존재" (DECISIONS 2.16, CONTEXT 4.9)
- 맥락이 요구한 예방 필드 `trend_score`, `imbalance_score`, `early_warning_score`, `preventive_action_priority`, `prevention_status` 가 **코드에 없다**.
- 정렬 테스트 `tests/test_gwan_prevention_layer_alignment.py` 는 이 단어들이 **docs/README/AGENTS 마크다운에 적혀 있는지만** 검사한다 (구현 검사 아님).
- 판단 모델은 대신 `severity` (`normal/watch/adjust/restrict/abort`)를 사용 → 맥락의 `prevention_status`와 이름이 다르고, `shelter_or_abort`가 `abort`로 축약됨.
- **결론**: 예방형 문명 운영체제(PHILOSOPHY 1.5)의 핵심인 예방 점수들이 실제 계산 로직으로 존재하지 않는다.

### 2.2 판단 모델 입출력 계약 불일치 (CONTEXT 4.8)
| 구분 | 맥락(문서) | 실제 코드(`GWANJudgmentInput/Result`) |
|------|-----------|----------------------------------------|
| 입력 | `distance_au, energy_signal, resource_signal, risk_signal, exploration_value_signal, spectral_signal_quality, catalog_match_confidence, data_classification, mission_phase` | `distance_risk, velocity_risk, radiation_risk, resource_signal, spectral_confidence, trajectory_uncertainty, energy_level, recovery_capacity` |
| 출력 | `recommended_action, prevention_status, human_review_required, reason_codes` | `recommended_action, severity, requires_human_review, reason_codes, ...` |
- 입력 스키마가 거의 다르며, `data_classification`이 판단 입력에 없다.
- 출력 필드명이 다름(`prevention_status`→`severity`, `human_review_required`→`requires_human_review`).

### 2.3 결정 엔진이 두 갈래로 분기
- `app/services/gwan_scoring.py` → `recommend_action(case)` : **6개 점수(이미 계산된 값)** 를 입력으로 받음.
- `app/services/gwan_judgment.py` → `calculate_gwan_judgment(data)` : **8개 원신호(raw signal)** 를 입력으로 받아 점수를 직접 계산.
- 두 엔진이 책임(행동 추천)이 겹치는데 입력 스키마가 서로 다르고, 맥락의 단일 계약과도 둘 다 어긋난다. → 유지보수/테스트 혼선 위험.

### 2.4 fixtures 불일치 (CONTEXT 4.11)
- 맥락은 `fixtures/sim_001_*.json ~ sim_006_*.json` 6개 시나리오 파일을 요구.
- 실제는 `tests/fixtures/`에 `sample_gwan_simulation_request.json`, `gwan_scoring_cases.json` 둘뿐. 6개 명명 시나리오 없음.

### 2.5 엔드포인트 일부 미구현 (CONTEXT 4.10)
- `/gwan/schema`, `/gwan/reports/{report_id}` 없음.
- health는 `/gwan/health`가 아니라 앱 루트 `/health`에 존재.
- (반대로 `/gwan/memory/*`, `/gwan/sync/*` 등 맥락에 없던 엔드포인트는 다수 존재)

---

## 3. ⚠️🔴 가장 큰 충돌 — 명문화된 "보류 원칙"과 정반대 구현

- 맥락([CONTEXT.md](CONTEXT.md) 3.5 · 3.13 · 4.14)은 다음을 **명시적으로 보류/금지**로 적어둠:
  - "Kubernetes 과도한 고도화" (보류)
  - "실제 StatefulSet 운영 전환" (보류)
  - "처음부터 Kubernetes 중심으로 구현하기" (하면 안 되는 작업)
- 그러나 실제 레포는:
  - GWAN 단계 23~74의 **대부분이 Kubernetes**.
  - **StatefulSet 마이그레이션에 승인 게이트·cutover·preflight·readiness 등 ~30단계 절차**를 축적 ([DESIGN_HISTORY.md](DESIGN_HISTORY.md) Phase 8 / ⚠️-4와 동일 지점).
- **결론**: 써놓은 원칙과 **정반대 방향**으로 가장 크게 어긋난 부분. 단일 로컬 DB 마이그레이션에 엔터프라이즈급 변경관리 절차를 입혔다.

---

## 4. ❌ 미반영 (맥락의 비전이 코드에 없음)

1. **HYEAN 8개 시스템 (DECISIONS 2.4)** — Position / Observation / **Spectral Intelligence** / Resource&Energy / Risk / Exploration Decision / **Micro-Probe Mission** / Memory&Map 중, 코드는 GWAN 엔진(scoring/judgment/simulation/memory) 중심일 뿐 8시스템 모듈 구조가 없다. 특히 분광·마이크로탐사·위치 시스템은 코드 모듈 부재(`spectrum_summary`는 단순 옵션 문자열 필드).
2. **GWAN 5레이어 중 Data Intake / Interpretation Layer (2.5)** — 별도 모듈 없이 시뮬레이션/암묵 처리. Scoring/Decision/Memory만 모듈로 존재.
3. **Onboard/Ground/Cloud 분리 + Sync Layer (2.9)** — 메모리 JSONL↔DB 동기화는 있으나, 온보드 오프라인 생존지도·긴급 로컬 감지 같은 아키텍처 분리는 없다. (현재 sync는 DB 동기화이지, 맥락이 의도한 onboard/ground sync가 아님)
4. **예방 판단 흐름** (관측→기미감지→균형분석→예방조정→위험판단→탐사결정→기억) — 미구현.
5. **Space Data Source Map (4.3)**, **Spectroscopy Learning Path (4.4)** — 문서 미작성.
6. **Operator Interface mockup / UI (4.12)** — UI 코드 없음 (보류 원칙과는 부합하나, 계획된 다음 단계로서는 미반영).

---

## 5. 영역별 정렬도 요약

| 영역 | 정렬도 | 비고 |
|------|--------|------|
| Data Contract (enum·패키지·검증) | 🟢 높음 | 거의 완벽 일치 |
| GWAN 점수/행동 체계 | 🟢 높음 | 6점수·8행동 일치 (단, 엔진 이중화) |
| GWAN v0.1 rule-based 범위 | 🟢 높음 | 원칙 준수 |
| 메모리/영속화/DB | 🟢 (초과) | 맥락보다 앞서 구현 |
| 판단 모델 입출력 계약 | 🟡 중간 | 개념은 맞으나 필드/이름 불일치 |
| 예방 레이어 | 🔴 낮음 | 문서만, 코드 미구현 |
| HYEAN 8시스템 / 분광 지능 | 🔴 낮음 | 모듈 부재 |
| Onboard/Ground 분리 | 🔴 낮음 | 아키텍처 미반영 |
| Kubernetes/StatefulSet 절제 | 🔴 역행 | 보류 원칙과 정반대 |
