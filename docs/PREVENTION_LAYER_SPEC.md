# 예방 레이어 사양 v0.1 (Prevention Layer Spec) — 초안

> 상태: **초안(검토 대기)** · 코드 미작성 · [REALIGNMENT_BACKLOG.md](REALIGNMENT_BACKLOG.md) H2 대응.
> 근거: [DECISIONS.md](DECISIONS.md) 2.16·2.10·4.9, [PHILOSOPHY.md](PHILOSOPHY.md) 1.5·1.6, [CONTEXT_VS_CODE.md](CONTEXT_VS_CODE.md) 2.1.
> 상위 동기: [MOTIVATION.md](MOTIVATION.md). 관측 축 확장 구상(씨앗): [EIGHT_PRINCIPLES_AXES.md](EIGHT_PRINCIPLES_AXES.md).
> 원칙: **rule-based만. ML 금지([DECISIONS.md](DECISIONS.md) 3.5).** 기존 핵심 판단 로직(`gwan_judgment.py`)을 갈아엎지 않고 **순수 추가(additive)** 로 구현.

---

## 0. 설계 철학 (모듈화 + 상호작용 + 진화 가능성)

사용자 확정 철학. 본 사양 전체가 이 셋을 동시에 만족하도록 설계된다.

1. **모듈화 (서양의학적 강점 — 역할 분담)**: 각 파트는 선택과 집중을 하고, 문제 발생 시 빠르게 유지보수한다. → 물리적 파일 분리.
2. **상호작용 (동양의학적 강점 — 통합 네트워크)**: 파트들은 단절되지 않고 서로 참조하며 전체의 흐름·위험·에너지 균형을 향해 예방한다. → 약한 상호 참조 + 전체 상태(holistic) 동시 관찰.
3. **통합이 더 견고하다**: 모듈화와 상호작용은 대립이 아니라 같은 대상을 다른 각도로 본 것. 합치면 더 견고하다.

추가 핵심 — **진화 가능성**: 흐름·균형 판단의 *규칙·임계값·가중치*를 코드에 하드코딩하지 않는다. 새 발견이 쌓이면 **코드를 갈아엎지 않고 규칙만 갱신**할 수 있어야 한다. 단, v0.1에서 과한 추상화는 금지([DECISIONS.md](DECISIONS.md) 2.10) — **최소 분리, 확장 여지만**.

---

## 1. 범위 (v0.1)

- **하는 것**: 예방 5필드 + `prevention_status` + 전체 상태(holistic) 동시 관찰을 **rule-based로 실제 계산**하는 신규 모듈과 동작 검증 테스트.
- **안 하는 것 (다음 단계로 분리)**:
  - 기존 `severity`(순간 위험 분류기) 변경 → **건드리지 않음**.
  - `severity`와 `prevention_status`를 **하나의 강제 행동 게이트로 합치기** → **H4**. (v0.1은 *약한 상호 참조*까지만)
  - 예방 필드를 `GWANInterfacePayload`/Data Contract에 편입 → **H4**.
  - 규칙을 YAML/DB/외부파일에서 로딩하는 로더·DSL·플러그인 → **금지(과한 추상화)**. v0.1은 코드 내 타입드 데이터로만.
  - MemorySnapshot 히스토리 자동 배선 → 다음 단계. v0.1은 **호출자가 입력 명시 공급**(stateless).

---

## 2. 모듈 구조 + 규칙 정의/실행 엔진 분리 (D1·진화 가능성)

**물리 분리(모듈화) + 규칙 데이터와 엔진 코드의 분리(진화 가능성)** 를 한 번에 만족하는 최소 패키지:

```text
app/services/prevention/
├─ __init__.py     # 공개 API 한 개:  assess_prevention(input, ruleset=DEFAULT_RULESET) -> PreventionAssessment
├─ models.py       # 데이터 형태: PreventionReading, PreventionInput, PreventionAssessment, PreventionStatus, HolisticState
├─ rules.py        # ★ 규칙 '정의' (데이터):  PreventionRuleSet + DEFAULT_RULESET  ← 새 발견 시 여기만 수정
└─ engine.py       # ★ 규칙 '실행' (엔진):  순수 함수. 숫자를 하드코딩하지 않고 ruleset에서 읽음
```

**핵심 패턴 — 정의/엔진 분리 (의존성 주입)**:

```text
engine.calc_trend(readings, ruleset.trend)        # 엔진은 '어떻게 계산하는지'만 안다
rules.DEFAULT_RULESET.trend.gain = 1.5            # 규칙은 '얼마로 계산하는지'만 안다 (데이터)
assess_prevention(input)                          # 기본 규칙으로 평가
assess_prevention(input, ruleset=my_ruleset)     # 새 발견을 반영한 규칙으로 평가 (엔진 코드 무수정)
```

- **엔진(`engine.py`)은 상수를 모른다.** 모든 가중치·임계값·오버라이드 조건을 `ruleset` 인자로 받는다.
- **규칙(`rules.py`)은 계산 절차를 모른다.** 숫자/조건만 보유한 값 객체(dataclass 또는 frozen pydantic).
- 새 "인체 지식"이 생기면 `rules.py`의 값 또는 `DEFAULT_RULESET`만 갱신 → 엔진·테스트 구조 불변.
- **v0.1 한계선(과추상화 금지)**: 로더/DSL/레지스트리 없음. 규칙은 코드 안의 `DEFAULT_RULESET` 하나. "파일에서 로딩"은 확장 여지로만 남기고 구현하지 않는다.

> 결합도: `prevention/`는 `app/schemas`의 `ContractBaseModel`과 공용 `clamp_score`만 재사용하고 **`gwan_judgment`를 import하지 않는다.** 유일한 공유 정리 = `_clamp_score`를 공용 위치로 승격(H2가 H4와 얽히는 최소 지점). 그 외 계약 통합은 H4.

| 비교 | 채택안: `prevention/` 패키지 (정의/엔진 분리) | 반려: 단일 `prevention.py`에 상수 하드코딩 |
|------|---------------------------------------------|--------------------------------------------|
| 모듈화 | ✅ | △ |
| 진화 가능성(규칙만 갱신) | ✅ rules.py 한 곳 | ❌ 코드 수정 필요 |
| v0.1 복잡도 | △ 파일 3~4개 (수용 가능) | ✅ 가장 단순 |
| 과추상화 위험 | 로더 없이 멈추면 낮음 | — |

---

## 3. `prevention_status`와 `severity`의 관계 — 분리하되 약한 상호 참조 (D2 확정)

D2 확정: **완전 직교(서로 모름)가 아니라, 서로 참조하되 침범하지 않는 약한 상호작용.**

```text
   gwan_judgment.py (기존, 무수정)
        severity  ──────────────┐  (값으로만 전달, import 아님)
   "지금 위험한가? (순간)"          │
                                 ▼
        ┌───────────────────────────────────────────────┐
        │  holistic 관찰 (engine):  severity ↔ prevention │  ← '함께 본다', 강제 행동 X
        │  → holistic_state (서술적 동시 관찰)              │
        └───────────────────────────────────────────────┘
                                 ▲
   prevention/ (신규)            │
        prevention_status ───────┘
   "흐름이 나빠지는가? 지금 조정할까? (흐름)"
```

규칙:
1. **물리 분리**: `severity`는 `gwan_judgment.py`, `prevention_status`는 `prevention/`. 코드 의존 없음.
2. **약한 참조(데이터)**: `severity`를 import하지 않고, 호출자가 그 **결과 값**을 `PreventionInput.severity_context`로 넘긴다. 예방 엔진은 이를 **읽기 전용 참조**로만 쓴다.
3. **침범 금지**: 예방은 `severity`를 바꾸지 않고, `severity`는 예방 5필드를 바꾸지 않는다. 예방 5필드·`prevention_status`는 흐름 입력만으로 산출(아래 5·6절).
4. **함께 보기(holistic)**: 둘을 합쳐 하나의 행동으로 강제하지 않되, **전체 상태 라벨**(`holistic_state`)로 동시에 본다. 이는 *서술적 관찰*이지 행동 결정이 아니다. (행동 게이트 = H4)

> **관측 축 확장과의 연결**: 이 2축(severity 급성 × prevention 누적 흐름)은 팔강변증의 **표-리(表裏, 급변↔누적)** 에 부분 대응한다([EIGHT_PRINCIPLES_AXES.md](EIGHT_PRINCIPLES_AXES.md) 3절). 나머지 축(허-실/한-열/음-양)은 v0.1에 **넣지 않으며**, 측정 데이터 정의는 H4 이후로 미룬다.

---

## 4. `prevention_status` 값 통일 — `shelter_or_abort` 채택 (severity는 `abort` 유지)

| 개념 | 값 집합 | 최상위 값 |
|------|---------|-----------|
| `prevention_status` (예방/흐름) | normal · watch · adjust · restrict · **shelter_or_abort** | `shelter_or_abort` |
| `severity` (현재 위험/순간, 기존) | normal · watch · adjust · restrict · **abort** | `abort` (변경 없음) |

**`prevention_status`=`shelter_or_abort` 채택**, `severity`=`abort` 유지. 이유: ① `shelter_or_abort`는 [DECISIONS.md](DECISIONS.md) 2.16·4.9 확정 표현, ② 의미가 다름("대피/경로 중단" vs "동작 즉시 중단"), ③ 억지 통일 대신 책임 분리로 [REALIGNMENT_BACKLOG.md](REALIGNMENT_BACKLOG.md) L1 해소 — 3절(약한 상호 참조)과 정합.

---

## 5. 입력 모델 (v0.1, stateless)

```text
PreventionReading  (한 시점, 값 0.0~1.0, anomaly_flags만 정수)
  composite_risk            # 그 시점 종합 위험 프록시 (judgment.risk_score를 넣어도 됨)
  uncertainty
  energy_level
  energy_consumption_rate   # 0=낮음, 1=높음
  recovery_capacity         # ★ 기존 입력 재사용 — 회복/완충 여력 (재계산 안 함)
  resource_pursuit          # 자원/탐사 추구 정도
  risk_exposure             # 현재 위험 노출 정도
  anomaly_flags: int >= 0   # 그 시점 소규모 이상신호 수(방사선 상승·통신잡음·센서오차·weak_signal)
  # ↓ 씨앗(v0.1 계산 미사용): 자리만 마련
  energy_signal: float | None = None  # 환경 빛/에너지 신호 강도(0~1). energy_level(잔량)과 의미 다름

PreventionInput
  readings: list[PreventionReading]    # 오래된→최신, 최소 1개 (추세/조기신호는 2개 이상일 때 의미)
  severity_context: str | None = None  # ★ 약한 참조: 현재 severity 값(normal..abort). import 아님, 데이터로 주입
  flow_axis: FlowAxis = temporal       # ↓ 씨앗(v0.1 계산 미사용): 흐름의 성격 표시

FlowAxis = temporal | spatial | mixed  # "흐름은 시간만이 아니라 공간 이동 경로일 수도 있다"는 일반화의 자리
```

`recovery_capacity`는 새 필드를 만들지 않고 `gwan_judgment` 입력의 동일 의미 값을 같은 출처에서 최신 reading에 공급, **재계산 없이 통과**시켜 "낮을수록 위험 증폭" 지표로만 쓴다.

### 5.1 씨앗 필드 — `energy_signal` · `flow_axis` (v0.1 계산 미반영)

복리식 과설계([DESIGN_HISTORY.md](DESIGN_HISTORY.md) H1 패턴) 방지를 위해, **자리(필드)는 지금 만들되 v0.1 engine 계산에는 넣지 않는다.**

| 씨앗 필드 | 위치 | 의미 | v0.1 | 다음 단계 |
|-----------|------|------|------|-----------|
| `energy_signal: float\|None` | `PreventionReading` | **환경 빛/에너지 신호 강도**(외부에서 들어오는 에너지). `energy_level`(내가 가진 잔량)과 **다른 축** | **미사용**(None 허용) | `ruleset`을 통해 허-실 축 계산에 도입 |
| `flow_axis: temporal\|spatial\|mixed` | `PreventionInput` | 흐름의 성격. v0.1은 시간(temporal) 흐름만 계산 | **temporal만 실제 계산** | spatial(공간 이동 경로)·mixed를 `ruleset`/engine 확장으로 도입 |

- 두 필드 모두 **engine은 읽지 않는다.** 주든 안 주든 결과가 동일해야 한다(테스트로 고정).
- **[EIGHT_PRINCIPLES_AXES.md](EIGHT_PRINCIPLES_AXES.md) 연결**: 그 노트의 *허-실 = energy_signal* 매핑이, 이제 추상 개념이 아니라 **실제 필드(`PreventionReading.energy_signal`)로 존재**한다. 측정 데이터 정의·계산 도입은 Space Data Source Map(H4 이후) 단계.
- 도입 시에도 [PREVENTION_LAYER_SPEC.md](PREVENTION_LAYER_SPEC.md) 2절의 정의/엔진 분리 원칙을 따라 **`rules.py`에 규칙으로** 들어가고 engine 절차는 최소 변경한다.

---

## 6. 예방 5필드 계산 규칙 (engine + ruleset)

`clamp01(x)=max(0,min(1,x))`. `R=readings`, `last=R[-1]`, `first=R[0]`. **모든 상수는 `engine`이 아니라 `ruleset`에 있음** → 새 발견 시 ruleset만 갱신.

| 필드 | 입력 | 규칙(공식) | 참조 ruleset 키 (정의=데이터) |
|------|------|-----------|-------------------------------|
| **trend_score** | 창의 `composite_risk`,`uncertainty` | `stress_i = w_r*risk_i + w_u*unc_i`; `delta = stress(last)−stress(first)` (창>2면 후반평균−전반평균); `clamp01(delta * gain)`. 단일 reading→0.0 | `trend.risk_weight(0.6)`, `trend.unc_weight(0.4)`, `trend.gain(1.5)` |
| **imbalance_score** | `last` | `consumption_gap = max(0, consumption − (a*energy + b*recovery))`; `exposure = resource_pursuit * risk_exposure`; `clamp01(w_c*consumption_gap + w_e*exposure)` | `imbalance.energy_w(0.5)`, `imbalance.recovery_w(0.5)`, `imbalance.consumption_w(0.5)`, `imbalance.exposure_w(0.5)` |
| **early_warning_score** | 창의 `anomaly_flags` | `magnitude = Σflags / (len*max_flags)`; `persistence = (flags≥1인 reading 수)/len`; `clamp01(w_m*magnitude + w_p*persistence)` | `early.magnitude_w(0.5)`, `early.persistence_w(0.5)`, `early.max_flags(3)` |
| **recovery_capacity** | `last.recovery_capacity` | **passthrough**. 재계산 없음 | — |
| **preventive_action_priority** | 위 4개 | `clamp01(w_t*trend + w_i*imbalance + w_e*early + w_r*(1−recovery))` | `priority.trend_w(0.40)`, `imbalance_w(0.30)`, `early_w(0.20)`, `low_recovery_w(0.10)` |

---

## 7. `prevention_status` + holistic 도출 규칙 (engine + ruleset)

`p=preventive_action_priority`, `rc=recovery_capacity`, `ew=early_warning_score`, `t=trend_score`.

**7.1 기본 임계값** (`ruleset.status_thresholds`, 튜닝 대상):

| `p` 구간 | prevention_status |
|----------|-------------------|
| `< 0.20` | `normal` |
| `0.20 ~ 0.40` | `watch` |
| `0.40 ~ 0.60` | `adjust` |
| `0.60 ~ 0.80` | `restrict` |
| `≥ 0.80` | `shelter_or_abort` |

**7.2 오버라이드** (`ruleset.overrides`, 기본값보다 우선):
- **급변 대피**: `ew ≥ 0.80` ∧ `rc ≤ 0.20` ∧ `t ≥ 0.70` → `shelter_or_abort`
- **회복 바닥 플로어**: `rc ≤ 0.30` ∧ `p ≥ 0.40` → 최소 `restrict`

**7.3 약한 상호 참조 → holistic_state** (`severity_context` 있을 때만, *서술적 관찰*, 행동 강제 아님):

| severity_context (순간) | prevention_status (흐름) | holistic_state | 의미 |
|-------------------------|--------------------------|----------------|------|
| 낮음(normal/watch) | 낮음(normal/watch) | `stable` | 안정 |
| 낮음 | 높음(adjust↑) | `early_drift` | 흐름이 먼저 경고 (동양의학적 조기 발견) |
| 높음(restrict/abort) | 낮음 | `acute_buffered_recoverable` | 순간 위험은 높으나 완충 여력이 있어 회복 가능한 급성 |
| 높음 | 높음 | `compound_escalation` | 순간+흐름 동시 악화, 여력 소진 |
| `None` | — | `prevention_only` | severity 미제공 |

- holistic은 두 모듈을 **함께 보되 어느 쪽도 바꾸지 않는다.** divergence 시 `reason_code: SEVERITY_PREVENTION_DIVERGENCE` 부여.
- **처방 차이를 `reason_summary`에 서술** (행동 강제 아님, 운영자 판단용 설명):
  - `acute_buffered_recoverable`: 완충 여력(높은 `recovery_capacity`)이 남아 있으므로 **관측·조정**으로 대응 가능 — "급성이나 회복 여지 있음".
  - `compound_escalation`: 여력이 소진되며 순간·흐름이 함께 악화 — **대피(shelter)** 쪽으로 무게. "급성+추세 악화, 여력 소진".
  - 두 라벨의 차이는 곧 **여력 있음(관측·조정) ↔ 여력 소진(대피)** 이며, 이는 7.2 '급변 대피' 오버라이드와 정합한다.
- `holistic_state`→단일 행동 매핑(강제 게이트)은 **H4**(여기서 안 함).

---

## 8. 검증 시나리오 (→ 3단계 테스트 근거, [DECISIONS.md](DECISIONS.md) 4.9 매핑)

| # | 상황 | 기대값 | 핵심 규칙 |
|---|------|--------|-----------|
| S1 | 위험 낮지만 불확실↑ & 추세 악화 | `prevention_status ≥ watch` | trend↑ |
| S2 | 자원 가치 높아도 `recovery_capacity` 낮음 | `restrict` | 회복 바닥 플로어 |
| S3 | 방사선·통신잡음·센서오차 **반복** 증가 | `adjust` 또는 `restrict` | early↑ + trend↑ |
| S4 | SEP 급변 + 회복 여력 낮음 | `shelter_or_abort` | 급변 대피 오버라이드 |
| S5 | 안정·균형·이상신호 없음 | `normal` | p 낮음 |
| S6 | 단일 reading(추세 정보 없음) | `trend_score=0.0`, 안전 동작 | 단일 reading 가드 |
| S7 | severity=restrict, prevention=normal | `holistic_state=acute_buffered_recoverable` + divergence 코드 | 약한 상호 참조 |
| S8 | severity=normal, prevention=adjust | `holistic_state=early_drift` | 흐름 선감지 |
| S9 | **동일 입력 + 다른 ruleset → 다른 결과** | ruleset 교체로 임계 통과 변화 | 진화 가능성(엔진 무수정) |

---

## 9. 출력 모델 (제안)

```text
PreventionAssessment
  trend_score: float
  imbalance_score: float
  early_warning_score: float
  recovery_capacity: float              # passthrough
  preventive_action_priority: float
  prevention_status: PreventionStatus   # normal|watch|adjust|restrict|shelter_or_abort
  severity_context: str | None          # 읽기 전용 에코
  holistic_state: HolisticState         # stable|early_drift|acute_buffered_recoverable|compound_escalation|prevention_only
  reason_codes: list[str]               # TREND_WORSENING, IMBALANCE_HIGH, REPEATED_ANOMALY,
                                        # LOW_RECOVERY_FLOOR, ACUTE_SHELTER, SEVERITY_PREVENTION_DIVERGENCE ...
  reason_summary: str
```

`PreventionStatus`·`HolisticState`는 예방 모듈 소유 enum. v0.1은 `GWANInterfacePayload`에 편입하지 않고 독립 응답. API 엔드포인트 노출은 4단계에서 협의(기본: 서비스+테스트만).

---

## 10. 범위 밖 / 다음 단계

- **H4**: 예방 필드를 Data Contract·`GWANInterfacePayload`에 편입, `severity × prevention_status → 단일 행동 게이트`, 판단 입출력 계약 단일화.
- 규칙을 외부 파일/DB에서 로딩(진화 구조의 다음 진화) — v0.1은 `DEFAULT_RULESET`까지만.
- MemorySnapshot 히스토리 → `PreventionInput` 자동 구성.
- [PHILOSOPHY.md](PHILOSOPHY.md) 1.6 균형 축 7개 전체를 imbalance에 반영(현재 2개 축).

---

## 11. 확정 필요 (사용자 결정 요청)

- [x] **D2** 관계: 분리하되 약한 상호 참조(holistic 함께 보기), 강제 게이트는 H4 — **확정됨**.
- [ ] **D1′** 구조: `prevention/` 패키지로 **규칙 정의(rules.py)와 실행 엔진(engine.py) 분리** — 동의? (단일 파일 선호 시 알려주세요)
- [ ] **D3** 값: `prevention_status`=`shelter_or_abort`, `severity`=`abort` 유지 — 동의?
- [ ] **D4** 입력: 시간창 `readings` + `severity_context` 약한 참조 + `recovery_capacity` passthrough — 동의?
- [ ] **D5** 규칙: 6·7절 공식/임계값을 **`DEFAULT_RULESET` 초기값**으로 두고 3단계 테스트(4.9 예시) 충족하도록 4단계에서 미세조정 — 동의?
- [ ] **D6** holistic: 7.3 `holistic_state` 5라벨(서술적 동시 관찰, 행동 강제 아님) — 동의? *(라벨명 `acute_buffered_recoverable`는 확정됨)*
- [ ] **D7** API: v0.1 엔드포인트 노출 여부 (기본: 보류) — 선택.
