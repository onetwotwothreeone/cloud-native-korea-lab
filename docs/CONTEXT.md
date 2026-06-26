# 세부 맥락 · 다음 단계 (Context & Next Steps)

> HYEAN/GWAN(= 이동형 지구 우주 항법 시스템, Mobile Earth Navigation System) 프로젝트에서 논의됐지만 **미확정/보류된 것**과 **앞으로 할 일 12개**.
> 확정 결정은 [DECISIONS.md](DECISIONS.md), 배경 철학은 [PHILOSOPHY.md](PHILOSOPHY.md), 작업 규칙은 루트 [CLAUDE.md](../CLAUDE.md) 참조.

---

# 3. 세부 맥락 — 미확정·보류·중요 배경

## 3.1 "프로젝트는 취업 포트폴리오가 아니다"
초기에는 xAI AI Tutor, AI Evaluation Platform, Korean Voice Data Evaluation Portfolio가 중요한 맥락이었으나, HYEAN/GWAN 전환 이후 현재 초점은 취업 지원이 아니다.

현재 초점:
```text
Define HYEAN completely.
Design GWAN clearly.
Reposition all existing projects under HYEAN.
Build the knowledge and infrastructure needed for long-term implementation.
```
포트폴리오 효과는 부수적으로 생길 수 있지만, 프로젝트 정체성은 **생존형 우주 지능 시스템**이다.

## 3.2 AI Evaluation Platform은 폐기가 아니라 재배치
훈련한 역량: structured evaluation, annotation workflows, scoring rubrics, review_required logic, uncertainty handling, human judgment modeling, data quality thinking, explainable decision records. → 이 경험은 GWAN의 점수화·불확실성 처리·human review·판단 기록·설명 가능한 의사결정에 그대로 연결된다.

## 3.3 Korean Voice Data Evaluation Portfolio도 재배치
단순 음성 평가가 아니라 구조화된 평가·루브릭 설계·모호한 데이터 판단·데이터 품질 판단·화자/발음/억양/대본 일치성 평가 역량의 예시로 재해석. → GWAN의 분광 해석·위험 검토·탐사 신뢰도 평가·decision audit trail에 연결 가능.

## 3.4 실제 우주 데이터 연동은 아직 보류
**사용 가능**: 공개 데이터, 자기 생성 시뮬레이션, 합성 예제, 적절히 인용된 자료, 비기밀 자료.
**범위 밖(보류)**: 실제 센서 연동, 실제 우주선 제어, 실제 생존-critical 제어 루프. → early implementation은 public data + simulation을 먼저 쓰고, real sensor integration은 나중으로.

## 3.5 ML/딥러닝은 GWAN v0.1에서 보류 ★
GWAN v0.1 진행 가능 범위:
```text
Rule-based Safety Gate + Weighted Scoring + Uncertainty Score + Reason Codes + Human Review Flag
```
**보류 항목**:
- ML/딥러닝 기반 판단
- 실제 우주 데이터 고도 연동
- 실제 3D UI 구현
- **Kubernetes 과도한 고도화**
- **실제 StatefulSet 운영 전환**
- 과학적으로 확정되지 않은 내용을 확정처럼 표현하는 것

**이유**: 지금 필요한 것은 "똑똑해 보이는 AI"가 아니라, **설명 가능하고 테스트 가능한 첫 판단 구조**다.

> ⚠️ 주의: 이 보류 목록은 실제 레포 현황과 충돌한다. 자세한 대조는 [DESIGN_HISTORY.md](DESIGN_HISTORY.md) 및 본 PR의 비교 분석 참조.

## 3.6 GWAN Judgment Model v0.1 — 진행 가능하나 범위는 좁게
구성 요소: 최종 입력 데이터 구조 / Safety Gate 최종 규칙 / Weighted Scoring 최종 공식 / Uncertainty Score 계산 규칙 / Reason Code 목록 / Human Review Flag 조건 / recommended_action 결정 규칙 / prevention_status 결정 규칙 / Pydantic 모델 필드 / pytest 케이스.

이것은 "완성된 우주 AI"가 아니라 **첫 번째 규칙 기반 판단 모델**이다. 비유: 우주선 자동조종 AI가 아니라 운영자가 읽을 수 있는 **첫 번째 안전 점검표 + 점수 계산기 + 판단 기록기**.

## 3.7 Operator Interface 최종 디자인은 미확정
확정: 인터페이스 철학 + 데이터 구조. **미확정**: 최종 UI 디자인, 색상 체계, 3D 그래픽 수준, cockpit aesthetics, 라이브러리/프론트엔드 프레임워크 선택, 모바일/데스크톱 우선순위, 렌더링 성능 기준. (Data Contract도 "최종 색상/콕핏 미학"은 정의하지 않는다고 명시)

## 3.8 1 AU 기준 시야는 고정값이 아니라 가변 스케일
```text
Local View:     km ~ thousands of km
Tactical View:  thousands ~ millions of km
Regional View:  0.01 AU ~ 1 AU
Strategic View: 1 AU 이상
```
**이유**: 즉각 위험과 장기 경로 계획은 전혀 다른 스케일을 요구하기 때문.

## 3.9 HYEAN의 목적 목록은 확정이지만 수정 가능
1. 인류 존속·탐색 지속을 위한 에너지원 탐색
2. 생존 가능한 행성/거주 가능 환경 탐색
3. 우주가 빅뱅 이전에는 어떤 상태였는지 탐구
4. 우주가 어떤 방향을 향해 가고 있는지 탐구

프로젝트가 성장하면서 추가·수정 가능.

## 3.10 철학적 가설과 시스템 출력은 분리
솔님 세계관에 포함된 맥락(인간은 지구에서, 지구는 우주에서 만들어졌다 / 인간의 욕망은 우주 흐름의 기본 설정일 수 있다 / 우주 진출은 지구의 물질·생명·기억·정보의 확장 / 지구를 고향이자 근원으로 보존 / 기술은 욕망의 실행 가속기 / AI·로봇과 인간의 자기 진화 / 쾌락·욕망을 존재·우주적 흐름 관점에서 탐구)은 **HYEAN의 철학적 배경**으로 중요하지만, GWAN의 실제 출력에서는 반드시 known/estimated/simulated/hypothesis/fictional_future_scenario로 분리한다.

## 3.11 커뮤니티 멀티채널 확장은 보류
블로그·유튜브 쇼츠·인스타그램·스레드·링크드인은 아이디어로만 논의. 초기에는 네이버 카페 하나에 집중. **이유**: 운영 부담 축소 / 하나의 거점 우선 / 실습→기록→질문→콘텐츠 루틴 안정화. 멀티채널은 "나중".

## 3.12 회원가입·로그인·게시판·결제는 아직 만들지 않는다
보류 기능: 회원가입, 로그인, 게시판, 댓글, 강의 결제, 관리자 페이지, DB 기반 커뮤니티 서비스, 알림, 완성형 AI 튜터. **이유**: 지금 필요한 것은 완성 서비스가 아니라 HYEAN/GWAN 구현과 학습을 위한 기준 실험 구조.

## 3.13 Kubernetes는 학습했지만 정체성은 아니다 ★
Deployment/Service/port-forward/probe/StatefulSet/PVC 등은 학습했으나 최신 원칙은:
- Kubernetes는 **필요할 때만** 쓴다.
- 서비스 수·반복 배포·self-healing·시뮬레이션 워크로드·관측 가능성이 필요할 때 도입.
- 단일 파일 프로토타입이나 초기 규칙 기반 모델에는 오히려 복잡도를 키울 수 있다.

→ Kubernetes는 HYEAN/GWAN의 "자랑 포인트"가 아니라 필요할 때 쓰는 운영 도구다.

## 3.14 PostgreSQL / JSONL / MemorySnapshot 흐름
```text
Synthetic space scenario → GWAN scoring rule → recommended action
→ Operator Interface payload → MemorySnapshot → JSONL or PostgreSQL storage → memory query API
```
JSONL은 초기 단순 저장, PostgreSQL은 구조화된 장기 저장 확장용. 학습 포인트: **Docker volume은 컨테이너를 지워도 남는다** (POSTGRES_USER=hyean 등 새 설정이 기존 volume 때문에 적용 안 되는 문제 경험).

## 3.15 용어 학습도 프로젝트의 일부
SQLAlchemy, query, HPA 객체, echo, StatefulSet, PostgreSQL, Deployment, PVC, CPU/RAM/Storage/Network, GPU 병렬 처리, Edge computing, Kubernetes object, Docker volume — HYEAN/GWAN을 실제 운영 가능한 시스템으로 만들기 위한 기초 체력.

---

# 4. 다음 단계 — 앞으로 할 일

## 4.1 지금 가장 중요한 방향
구현을 크게 벌리는 것이 아니라 순서를 지키는 것:
```text
HYEAN 최종 비전 유지 → GWAN 구조 명확화 → Data Contract 기준 구현 가능한 모델 생성
→ 첫 rule-based simulation 작성 → 테스트 검증 → FastAPI endpoint 노출 → 문서/커뮤니티 설명
```
Control Center 기준 다음 작업 단위: (1) Space Data Source Map 확장 (2) Spectroscopy Learning Path (3) 첫 GWAN simulation 정의 (4) scoring test cases 작성 (5) README를 HYEAN/GWAN 정체성에 맞게 업데이트.

## 4.2 작업 1 — README 정체성 업데이트
README가 전달할 메시지:
```text
I am building HYEAN, a survival-oriented space intelligence service for mobile human habitats.
Its core engine, GWAN, combines astronomical data, onboard observations, spectroscopy,
risk scoring, resource evaluation, uncertainty handling, and exploration decision logic
to help a spacecraft understand its environment and decide where to observe, avoid,
approach, or send micro-probes.
```
포함: HYEAN/GWAN 한 줄 정의, Cloud Native Korea Lab의 역할, AI Evaluation Platform 재배치, 현재 구현 범위, 현재 보류 범위, known/estimated/simulated/hypothesis/future-scenario 구분, 첫 simulation 목표, 설치·실행·테스트 방법, 다음 로드맵.

## 4.3 작업 2 — Space Data Source Map
작성 항목: (1) 사용 가능한 공개 우주 데이터 (2) 각 데이터가 설명하는 것 (3) HYEAN 어느 시스템에 연결 (4) GWAN 어느 레이어에서 사용 (5) known/estimated/simulated/hypothesis 분류 (6) 초기 simulation에서 가짜로 만들 것 vs 공개 데이터로 대체할 것.
예상 분류: 천체 카탈로그 / 소행성·혜성 / 행성·위성 / 항성 / 궤도 / 분광 / 우주 날씨 / 방사선 / 시뮬레이션 전용 synthetic dataset.

## 4.4 작업 3 — Spectroscopy Learning Path
Spectral Intelligence System이 핵심 감각기관이므로 분광법 학습 경로 필요. 포함: 분광법 정의, 흡수선/방출선, 빛으로 물질 추정 의미, 수소/헬륨/산소/물·얼음 단서, 분광 신호의 한계, weak signal → 불확실성, 분광 해석 → GWAN `spectrum_summary` 변환, overclaim 회피.
비유: 분광법은 멀리 있는 물체를 만지지 않고 그 물체가 빛에 남긴 "지문"을 읽는 방법.

## 4.5 작업 4 — 첫 GWAN simulation 정의
첫 simulation은 작게. 추천 시나리오:
```text
상황: 이동식 인간 거주체가 태양에서 멀어지는 중. 태양광 에너지 약화.
      얼음 소행성 후보 1개 감지. 분광 신호 약함. 위험도 낮음~중간.
      자원 가능성 중간 이상. 불확실성 높음.
GWAN 판단: 즉시 send_micro_probe 안 함. observe_more 또는
           request_additional_spectral_observation 추천.
           Memory & Map System에 uncertain_resource_candidate로 저장.
```
Data Contract 예시(candidate-ice-001: resource score 중간 이상, uncertainty 높음 → observe_more)와 일치.

## 4.6 작업 5 — Pydantic 모델 생성
우선 모델: `GWANInterfacePayload, MissionContext, CoordinateReference, GWANOutputPackages, SpatialVisualizationPackage, SpatialObject, SidebarIntelligencePackage, AlertFeedPackage, AlertItem, UncertaintyPackage, UncertaintyItem, DecisionReportPackage, MemoryUpdate`.
규칙: 모든 score 0~1 / generated_at datetime / data_classification·recommended_action·uncertainty_type enum / 좌표 단위 명시 / uncertain이면 uncertainty_reason 필수 / 추천에는 reasoning_steps 또는 reason_summary 필수.

## 4.7 작업 6 — pytest 테스트 케이스
1. sample decision에서 모든 package 생성
2. uncertain object가 uncertainty_reason 없이 통과 못 함
3. alert_feed가 severity·priority_score로 정렬
4. sidebar가 scores·provenance·uncertainty·recommended_action 포함
5. full report가 known/estimated/simulated/hypothesis/future-scenario 구분 보존
6. spatial object에 coordinate unit·range_scale 항상 존재
7. score가 0~1 벗어나면 실패
8. recommended_action이 허용 enum 밖이면 실패
9. send_micro_probe가 high uncertainty에서 바로 추천되지 않음
10. observe_more가 weak_signal 상황에서 추천됨

## 4.8 작업 7 — GWAN Judgment Model v0.1 구현
범위: `Rule-based Safety Gate + Weighted Scoring + Uncertainty Score + Reason Codes + Human Review Flag + recommended_action + prevention_status`.

입력 예시:
```json
{
  "mission_id": "sim-001", "object_id": "candidate-ice-001",
  "distance_au": 0.128, "energy_signal": 0.31, "resource_signal": 0.68,
  "risk_signal": 0.27, "exploration_value_signal": 0.74,
  "spectral_signal_quality": 0.38, "catalog_match_confidence": 0.42,
  "data_classification": "simulated", "mission_phase": "regional_resource_scan"
}
```
출력 예시:
```json
{
  "recommended_action": "observe_more", "prevention_status": "watch",
  "human_review_required": true,
  "reason_codes": ["RESOURCE_POTENTIAL_MODERATE","SPECTRAL_SIGNAL_WEAK","UNCERTAINTY_HIGH","MICRO_PROBE_NOT_YET_SAFE"]
}
```

## 4.9 작업 8 — Prevention Layer v0.1 반영
반영 필드: `trend_score, imbalance_score, early_warning_score, recovery_capacity, preventive_action_priority, prevention_status`.
`prevention_status` 후보: `normal, watch, adjust, restrict, shelter_or_abort`.
판단 예시:
- 위험 낮지만 uncertainty 높고 trend 악화 → `watch`
- resource_score 높아도 recovery_capacity 낮음 → `restrict`
- 방사선·통신 잡음·센서 오차 동반 증가 → `adjust` 또는 `restrict`
- SEP 같은 단기 급변 위험 높고 회복 여력 낮음 → `shelter_or_abort`

구현 방향: MemorySnapshot에 예방 필드 추가 / Risk System은 현재 위험과 미래 위험 가능성 분리 / Observation System은 단발성 이상값과 반복 신호 구분.

## 4.10 작업 9 — FastAPI endpoint 설계
첫 API 후보: `POST /gwan/simulate`, `POST /gwan/interface-payload`, `GET /gwan/health`, `GET /gwan/schema`.
추천 순서: (1) /gwan/health (2) /gwan/simulate (3) /gwan/interface-payload (4) /gwan/reports/{report_id} (5) /gwan/memory.
초기에는 DB 없이 JSON fixture → JSONL → PostgreSQL 순서로 확장.

## 4.11 작업 10 — 샘플 JSON fixtures
```text
fixtures/
├─ sim_001_uncertain_ice_candidate.json
├─ sim_002_high_risk_radiation_zone.json
├─ sim_003_low_risk_low_resource_candidate.json
├─ sim_004_high_resource_high_risk_candidate.json
├─ sim_005_missing_data_human_review.json
└─ sim_006_prevention_watch_status.json
```
각 fixture 검증: 자원 높아도 위험 높으면 바로 접근 안 함 / 불확실성 높으면 추가 관측 추천 / simulated를 confirmed처럼 표시 안 함 / missing data면 human_review_required=true / prevention_status가 단순 risk_score와 다르게 작동.

## 4.12 작업 11 — Operator Interface mockup
고급 3D는 아직 불필요. 우선순위: (1) 2D 좌표 평면 또는 간단한 3D placeholder (2) object pin (3) resource/risk/uncertain category 표시 (4) 선택 시 sidebar 정보 (5) uncertainty badge (6) alert feed (7) full decision report 버튼.
미래 경로: GWAN structured output schema 정의 → simulated objects 기반 2D/3D mockup → selectable pins/sidebar → uncertainty tags/alert feed → GWAN scoring 연결 → full report view → 실제 public space data 및 advanced visualization.

## 4.13 작업 12 — 커뮤니티 콘텐츠로 변환
추천 콘텐츠 순서:
1. HYEAN은 왜 지도 앱이 아닌가?
2. GWAN은 무엇을 판단하는 엔진인가?
3. 왜 우주선 판단에는 불확실성이 중요한가?
4. resource_score가 높아도 risk_score가 높으면 왜 조심해야 하는가?
5. 왜 cloud보다 edge/onboard 판단이 중요한가?
6. Docker/Kubernetes는 HYEAN에서 어디에 쓰이는가?
7. 분광법은 왜 우주의 지문을 읽는 기술인가?
8. Prevention Layer는 왜 "문명의 건강검진"인가?

## 4.14 지금 하면 안 되는 작업 ★
- HYEAN을 작은 데모 앱으로 소개하기
- HYEAN을 취업 포트폴리오라고만 설명하기
- Cloud Native를 프로젝트 정체성으로 만들기
- 처음부터 Kubernetes 중심으로 구현하기
- 실제 센서 연동부터 하려 하기
- ML/딥러닝 모델부터 붙이기
- 3D UI 디자인부터 깊게 들어가기
- 로그인/회원가입/게시판 같은 일반 서비스 기능 만들기
- 과학적 가설을 확정된 사실처럼 표현하기
- 불확실한 데이터를 confirmed로 표시하기

## 4.15 실습 예시 — 다음에 바로 진행할 수 있는 작업
```bash
cd ~/cloud-native-korea-lab
mkdir -p hyean-gwan/app hyean-gwan/tests hyean-gwan/fixtures hyean-gwan/docs
```
파일 구조:
```text
hyean-gwan/
├─ app/ (main.py, models.py, scoring.py, decision.py, interface_payload.py)
├─ fixtures/ (sim_001_uncertain_ice_candidate.json)
├─ tests/ (test_models.py, test_scoring.py, test_decision.py, test_interface_payload.py)
└─ docs/ (gwan-v0.1-simulation.md)
```
목표: simulated object 하나를 입력하면 GWAN이 점수화하고, recommended_action을 정하고, uncertainty_reason을 붙이고, HYEAN Operator Interface용 JSON payload를 생성한다.
