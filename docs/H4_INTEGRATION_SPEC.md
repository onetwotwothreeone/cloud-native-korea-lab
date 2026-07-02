# H4 통합 사양 (Prevention ↔ Data Contract) — 초안

> 상태: **초안(검토 대기) · 코드 미작성.** [REALIGNMENT_BACKLOG.md](REALIGNMENT_BACKLOG.md) H4 중 **(가)+(나)만, 얕게**.
> 근거 진단: 1단계 읽기 진단(이 대화). 연결: [PREVENTION_LAYER_SPEC.md](PREVENTION_LAYER_SPEC.md)(2축·약한 상호참조·정의/엔진 분리), [DESIGN_HISTORY.md](DESIGN_HISTORY.md)(H1 과설계 경계).
> 원칙: 기존 핵심·계약 코드를 **순수 추가(additive)** 로만 건드린다. 어제 `energy_signal` 씨앗처럼 **"자리만" 잇는다.**

---

## 0. 이번 H4 범위 (확정)

| 항목 | 이번 H4 | 비고 |
|------|---------|------|
| (가) PreventionAssessment를 Data Contract에 편입 | ✅ **얕게(자리만)** | 연결 가능한 구조 + 어댑터까지. 자동 배선은 안 함 |
| (나) severity ↔ prevention_status 약한 상호작용을 계약 레벨에서 표현 | ✅ **함께 보이게(holistic)** | 행동 게이트는 **안 만듦** |
| (다) 판단 모델 이중화(gwan_scoring vs gwan_judgment) 해소 | ❌ **범위 밖 → H3** | 이번엔 두 파일 모두 무수정 |
| severity × prevention → 단일 행동 게이트 | ❌ **범위 밖(다음 단계)** | 4절 참조 |
| 깊은 결합(자동 populate, 좌표 교차검증, severity 자동 동기화) | ❌ **범위 밖** | 4절 참조 |

---

## 1. (가) 계약 편입을 '얕게' 하는 구체안

### 1.1 새 계약 스키마 `PreventionReport(ContractBaseModel)`
- 위치: `app/schemas/gwan_interface.py` (또는 신규 `app/schemas/prevention_report.py`).
- `ContractBaseModel` 상속 → `extra="forbid"` 규약 준수. `PreventionAssessment`(순수 `BaseModel`)의 **계약용 거울(mirror)**.
- 필드(거울): `prevention_status`, `severity_context`(echo), `holistic_state`, `trend_score`, `imbalance_score`, `early_warning_score`, `recovery_capacity`, `preventive_action_priority`, `reason_codes`, `reason_summary`.
- **`recommended_action` 필드 없음** — 이것이 (나)의 행동 게이트 금지선(1.4·2절).

### 1.2 페이로드에 '자리'를 잇는 두 방안

```text
[방안 A] 6번째 옵션 package                     [방안 B] 최상위 옵션 필드(권장)
GWANInterfacePayload                            GWANInterfacePayload
└ packages: GWANOutputPackages                  ├ packages: GWANOutputPackages (5개 그대로)
   ├ spatial (필수)                              └ prevention: PreventionReport | None = None
   ├ sidebar | None                                 (display package가 아니라 '횡단 평가'라서 분리)
   ├ alert_feed | None
   ├ uncertainty | None
   ├ decision_report | None
   └ prevention_package: PreventionReport | None = None
```

| | 방안 A (6번째 package) | 방안 B (최상위 옵션 필드) — **권장** |
|---|---|---|
| 기존 5 package | 구조는 유지하나 묶음에 1개 추가 | **5개 그대로 무변경** |
| 의미 정합 | 예방은 'display package'가 아닌데 섞임(약간의 의미 왜곡) | 예방=흐름 횡단 평가 → 별도 자리가 정직 |
| 운영 UI | 기존 package 순회 루프에 자연 편입 | payload.prevention 별도 읽기 필요 |
| 비파괴성 | 옵션 default None → 비파괴 | 옵션 default None → 비파괴 |

→ 둘 다 **옵션·default None이라 기존 페이로드는 그대로 유효**(비파괴). 권장은 **B**(정직한 분리, 5 package 무변경). 최종은 D1.

### 1.3 enum 레이어링 충돌 (ContractBaseModel 규약과 충돌하는 지점)
- **현재 레이어 방향**: `services → schemas` (예: `gwan_judgment`가 `app.schemas`를 import). 정상.
- **충돌**: `PreventionReport`가 `prevention_status: PreventionStatus`를 쓰려면 schemas가 `app.services.prevention.models`의 enum을 import → **레이어 역전(schemas → services)**.
- 해소 방안:
  - **(i) enum을 schemas로 내림(권장)**: `PreventionStatus`·`HolisticState`를 `gwan_interface.py`로 옮기고, `prevention/models.py`는 거기서 **import·재노출**. (`RecommendedAction`이 이미 계약 enum인 것과 동일한 정합.) prevention 테스트는 `from ...models import PreventionStatus`를 그대로 쓰므로 재노출이면 무변경.
  - **(ii) 계약 쪽에서 값 복제**: schemas에 `Literal[...]`로 값만 복제(서비스 import 회피). 더 얕지만 **값 드리프트 위험**.
- 권장 (i). 최종은 D2.

### 1.4 어댑터(경계 번역기) — 자동 배선 안 함
- 신규 `app/services/prevention/contract_adapter.py`: `to_prevention_report(assessment: PreventionAssessment) -> PreventionReport`.
- 역할: 느슨한 `BaseModel`(extra ignore) → 엄격한 `ContractBaseModel`(extra forbid) 경계 번역. engine/rules/models의 **계산 로직은 무수정**.
- **얕음의 핵심**: 이 어댑터와 옵션 자리까지만 만든다. `/simulate` 등 기존 엔드포인트가 prevention을 **자동 채우지 않는다**(자동 populate = 깊은 결합 = 범위 밖).

---

## 2. (나) severity ↔ prevention 약한 상호작용을 계약 레벨에서

- **지금**: `severity_context`는 prevention 패키지 내부에서만 참조되고(holistic), 계약/페이로드에는 전혀 안 보임.
- **이번 변화**: `PreventionReport` 하나가 `prevention_status` + `severity_context`(echo) + `holistic_state`를 **한 객체에 함께** 담는다 → 계약 페이로드 수준에서 두 축이 **나란히 보인다**(함께 보기). `holistic_state`(stable/early_drift/acute_buffered_recoverable/compound_escalation/prevention_only)가 곧 둘의 서술적 동시 관찰.
- **침범 금지 유지**: 계약에 담긴 `severity_context`는 **에코일 뿐**, prevention이 severity를 바꾸지 않고 그 반대도 아니다([PREVENTION_LAYER_SPEC.md](PREVENTION_LAYER_SPEC.md) 3절 그대로).
- **행동 게이트 금지선(명확히)**:
  - `PreventionReport`에는 `recommended_action`이 **없다**.
  - 페이로드의 유일한 행동은 기존 `DecisionReportPackage.recommended_action`이며, 이번에 **무수정**(여전히 judgment/scoring 출처).
  - 즉 "severity와 prevention_status를 합쳐 하나의 행동을 강제"하는 코드·필드를 **만들지 않는다.** → 다음 단계.
- **얕음의 한계(명시)**: `severity_context`를 같은 페이로드의 judgment severity와 **자동 동기화/교차검증하지 않는다**(호출자가 넣은 값을 신뢰). 일관성 검증은 다음 단계.

---

## 3. 변경 범위 체크리스트 + 기존 342 테스트 충돌 위험

| # | 파일 | 변경 | 깊이 | 기존 테스트 충돌 위험 |
|---|------|------|------|------------------------|
| C1 | `app/schemas/gwan_interface.py` | `PreventionReport` 추가 + 옵션 자리(B: 최상위 필드 / A: 6번째 package) + (D2-i면) enum 2개 이동 | 얕음(추가) | **낮음.** 자리 옵션·default None → 기존 페이로드 유효. `schema_version`은 **v0.1 유지**(아래 R1) |
| C2 | `app/services/prevention/contract_adapter.py` (신규) | `to_prevention_report()` 어댑터 | 신규 | **없음**(새 파일) |
| C3 | `app/services/prevention/models.py` | (D2-i 채택 시만) enum을 schemas에서 import·재노출 | 얕음 | **낮음.** prevention 테스트는 재노출명 그대로 import → 무변경 |
| C4 | `app/api/routes_gwan.py` | (D6) 기본은 **무변경**. 엔드포인트 노출은 보류 | 없음/옵션 | 무변경이면 없음 |
| C5 | `tests/test_h4_prevention_contract.py` (신규) | 어댑터·자리·"행동필드 없음"·기존 페이로드 무프레벤션 유효 검증 | 신규 | 기존과 독립 |

**구체 위험 평가**
- **R1 (schema_version 테스트)**: `test_gwan_interface_schema.py`가 `schema_version == "hyean.gwan.interface.v0.1"`를 단언. → **버전 올리지 않고 추가-옵션만** 하면 green 유지. 버전 bump는 보류(D7).
- **R2 (extra="forbid")**: 계약은 미선언 필드를 거부하지만, 우리가 자리를 **선언**하므로 문제 없음. 기존 JSON fixture들은 prevention 필드를 보내지 않으므로 그대로 유효.
- **R3 (payload model_validator)**: `validate_cross_package_contract`는 object_id 교차참조 검사. prevention엔 좌표/object_id 교차참조가 없어 **무관**. (방안 A로 packages 안에 넣어도 검증 로직이 prevention을 건드리지 않게 둘 것.)
- **R4 (enum 이동, D2-i)**: 재노출만 지키면 prevention 11개 테스트 green 유지. 재노출 누락이 유일한 깨짐 경로 → 구현 시 점검.
- 종합: **추가-옵션 + default None + schema_version 동결**이면 기존 342개에 대한 위험 **낮음**. 3단계(테스트 먼저)에서 R1·R4를 우선 가드.

---

## 4. 무엇을 '안 하는지' (범위 밖, 명시)

- **(다) 판단 모델 이중화 해소** — `gwan_scoring`/`gwan_judgment` 두 파일 **무수정** → **H3**로 분리.
- **행동 게이트** — severity × prevention_status → 단일 `recommended_action` 매핑/필드 **안 만듦**.
- **깊은 결합** — `/simulate` 자동 populate, `severity_context` 자동 동기화, severity↔prevention 일관성 교차검증, 좌표 결합 **안 함**.
- **4축·energy_signal 계산** — 여전히 씨앗([EIGHT_PRINCIPLES_AXES.md](EIGHT_PRINCIPLES_AXES.md)) 단계, 계산 도입 **안 함**.
- **schema_version bump** — v0.1 유지(D7).

---

## 5. 확정 필요한 결정 (D1~D7)

- [ ] **D1 (가) 자리 위치**: 방안 B(최상위 옵션 필드, 권장) vs 방안 A(6번째 package).
- [ ] **D2 enum 레이어링**: (i) enum을 schemas로 내리고 재노출(권장) vs (ii) 계약에 값 복제.
- [ ] **D3 `PreventionReport` 필드 범위**: 전체 거울(5점수+status+severity_context+holistic+reasons, 권장) vs 최소(status+severity_context+holistic+reason_summary).
- [ ] **D4 행동 게이트 금지선**: `PreventionReport`에 `recommended_action` 없음 + `DecisionReportPackage` 무수정 — 동의?
- [ ] **D5 severity 일관성**: 이번엔 echo만, 자동 동기화·교차검증 안 함 — 동의?
- [ ] **D6 엔드포인트**: 이번엔 `routes_gwan.py` 무변경(자리+어댑터+테스트만) vs 작은 엔드포인트 추가.
- [ ] **D7 schema_version**: v0.1 유지(추가-옵션, 비파괴) vs v0.2 bump.

> 확정되면, 구현은 내일 **3단계(테스트 먼저: 어댑터·자리·'행동필드 없음'·비파괴 검증)** 부터. 코드는 오늘 건드리지 않는다.

---

# 부록: 중간 연결 (Mid-Connection) — 예방을 '한 곳 흐름'에서 populate

> 상태: **초안(검토 대기) · 코드 미작성.** (가)+(나)의 계약 자리(위 본문)가 커밋(`f3639e8`)된 뒤, 그 자리를 **실제로 채우는 첫 흐름**을 만드는 단계.
> 확정 전제: **길 A**(호출자가 명시적 `PreventionInput` 제공, 데이터 날조 0) + **엔드포인트 미노출**(서비스 함수+테스트만, D6 보류 유지).

## M0. 범위 / 경계
- ✅ 기존 빌더는 **무수정**, 그 위에 얇게 얹는 **새 래퍼 함수 하나**로 예방을 populate.
- ❌ 기존 빌더 내부 삽입(=`/simulate`·`/simulate-integrated` 자동 populate), `gwan_judgment`/`gwan_scoring` 수정, severity 자동 동기화·교차검증, 행동 게이트, `routes_gwan.py` 변경 — 모두 범위 밖.

## M1. 새 래퍼 함수 — 이름 · 시그니처 · 위치
- 위치: `app/services/gwan_simulation.py` (기존 빌더 옆).
- 시그니처(권장):

```python
def generate_simulation_with_prevention(
    prevention_input: PreventionInput,
    request: GWANSimulationRequest | None = None,
) -> IntegratedSimulationResult:
```

- `prevention_input`: **필수**(길 A). 거주체 흐름 readings를 호출자가 제공. `severity_context`는 그 안의 값(또는 None)을 그대로 사용(자동 동기화 없음).
- 동작(기존 빌더는 '호출'만):

```text
1. result   = generate_integrated_simulation_result(request)     # 기존 빌더 무수정, 호출만
2. assessment = assess_prevention(prevention_input)              # 예방 실제 작동
3. report   = to_prevention_report(assessment)                   # 계약 거울(위 본문 (가))
4. enriched = result.payload.model_copy(update={"prevention": report})
5. return result.model_copy(update={"payload": enriched})
```

## M2. 반환 타입 — `IntegratedSimulationResult` (기존 타입 재사용, 무변경)
- 반환: `IntegratedSimulationResult` — `payload.prevention`이 채워지고 `object_decisions`는 보존.
- 이유: 기존 타입 재사용(신규 타입·스키마 변경 0), 정보 손실 없음, enriched payload는 `.payload`로 접근.
- prevention은 이미 `payload.prevention`에 들어가므로 `IntegratedSimulationResult`에 prevention 필드를 **추가하지 않는다**(스키마 무변경).
- payload만 필요하면 `.payload` 접근으로 충분 — payload-only 헬퍼는 지금 불필요.

## M3. 새 의존성 (레이어 확인)
- `gwan_simulation` → `app.services.prevention`(`assess_prevention`) + `app.services.prevention.contract_adapter`(`to_prevention_report`).
- 동일 레이어(services→services), **순환 없음**(prevention은 `gwan_simulation`을 import 안 함).

## M4. 3단계에서 못박을 검사(미리 정리)
- 진짜 `PreventionInput` 주입 시 `payload.prevention`이 실제로 채워짐.
- 채워진 `prevention` 값이 `assess_prevention` 결과와 **100% 일치**(품질 가드).
- 채워진 뒤에도 기존 5 package **무변경**(비파괴).
- 채워진 페이로드가 `ContractBaseModel` 규약 **위반 없음**(새 품질 가드).
- `prevention_input` 미주입 기존 빌더 경로는 여전히 **`prevention=None`**(경계).

## M5. 확정 필요 (M-D)
- [ ] **M-D1 시그니처**: `generate_simulation_with_prevention(prevention_input, request=None)` — 이름·인자 순서 동의?
- [ ] **M-D2 반환 타입**: `IntegratedSimulationResult` 재사용(권장) vs `GWANInterfacePayload`(payload만).
