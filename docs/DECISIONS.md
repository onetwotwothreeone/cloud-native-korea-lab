# 결정사항 (Confirmed Decisions)

> HYEAN/GWAN(= 이동형 지구 우주 항법 시스템, Mobile Earth Navigation System) 프로젝트에서 지금까지 확정된 설계 결정과 그 이유.
> 배경 철학은 [PHILOSOPHY.md](PHILOSOPHY.md), 미확정·보류·다음 단계는 [CONTEXT.md](CONTEXT.md), 작업 규칙은 루트 [CLAUDE.md](../CLAUDE.md) 참조.

---

## 2.1 프로젝트 정체성

```text
HYEAN = top-level service vision
GWAN  = core observation, interpretation, scoring, decision, and memory engine
Cloud Native Korea Lab = infrastructure / learning / documentation lab for HYEAN and GWAN
AI Evaluation Platform = evaluation and scoring workflow training asset for GWAN
```

**이유**: 프로젝트를 단순한 클라우드 학습·취업 포트폴리오·작은 웹 앱으로 축소하지 않기 위해서. 중심은 HYEAN/GWAN이며, Cloud Native Korea Lab은 이를 구현하기 위한 기술 실험실로 재배치되었다.

## 2.2 HYEAN의 최종 정의

> HYEAN은 생존형 이동식 우주 문명이 주변 우주 환경을 읽고, 에너지·자원·위험·탐사 가치를 판단하며, 다음 행동을 결정하도록 돕는 우주 생존 지능 서비스다.

HYEAN이 답해야 하는 질문:

```text
Where am I?
What is nearby?
What energy sources are available?
What planets, asteroids, comets, gases, or resource candidates are nearby?
What is dangerous?
What deserves more observation?
What deserves micro-probe exploration?
Where should the habitat move next?
```

**이유**: 우주 생존에는 단순한 위치 정보보다 자원·위험·탐사 가치·다음 행동 판단이 더 중요하기 때문.

## 2.3 HYEAN의 핵심 사용자

- 이동식 인간 거주체
- 거주체 내부 또는 연결된 인간 운영자
- 온보드 의사결정 지원 시스템
- 마이크로 탐사선 임무 계획 시스템
- 지상 연구 및 시뮬레이션 팀

**이유**: HYEAN은 사람에게만 보여주는 앱이 아니라, 인간 운영자·우주선 내부 시스템·탐사선 계획·지상 시뮬레이션이 함께 사용하는 복합 생존 판단 시스템이기 때문.

## 2.4 HYEAN의 8개 시스템

```text
HYEAN
├─ Position System
├─ Observation System
├─ Spectral Intelligence System
├─ Resource & Energy System
├─ Risk System
├─ Exploration Decision System
├─ Micro-Probe Mission System
└─ Memory & Map System
```

| 시스템 | 역할 |
|--------|------|
| Position System | 현재 위치, 이동 상태, 위치 불확실성 판단 |
| Observation System | 광학·분광·열·방사선·입자·환경 관측 수집 |
| Spectral Intelligence System | 빛의 단서로 물질·가스·자원 후보·불확실성 해석 |
| Resource & Energy System | 에너지와 자원 가능성 평가 |
| Risk System | 방사선·충돌·중력·먼지·에너지·임무 위험 평가 |
| Exploration Decision System | 관측·회피·접근·마이크로 탐사선 파견·장기 후보 등록 추천 |
| Micro-Probe Mission System | 소형 탐사선 계획과 결과 기록 |
| Memory & Map System | 관측·점수·판단·불확실성·생존 지도 업데이트 저장 |

**이유**: HYEAN을 하나의 거대한 앱이 아니라, 책임이 나뉜 생존 판단 아키텍처로 만들기 위해서.

## 2.5 GWAN의 5개 엔진 레이어

```text
GWAN
├─ Data Intake Layer
├─ Interpretation Layer
├─ Scoring Layer
├─ Decision Layer
└─ Memory Layer
```

| 레이어 | 역할 |
|--------|------|
| Data Intake Layer | 위치·거리·시간·객체 ID·좌표계·출처 메타데이터 정규화 |
| Interpretation Layer | 관측값과 known/estimated/simulated/hypothesis 데이터를 비교 |
| Scoring Layer | energy, resource, risk, exploration, uncertainty, survival priority 계산 |
| Decision Layer | avoid, wait, observe_more, approach, send_micro_probe 등 행동 추천 |
| Memory Layer | 관측·추론·점수·추천 행동·실제 행동·사후 확인 결과·생존 지도 업데이트 저장 |

**이유**: GWAN이 단순 점수 계산기가 아니라, 관측부터 기억까지 이어지는 판단 엔진이 되어야 하기 때문.

## 2.6 GWAN의 점수 체계

- `energy_score`: 에너지 관련 후보로서의 유용성
- `resource_score`: 물·얼음·금속·광물·가스 등 자원 가능성
- `risk_score`: 방사선·충돌·궤도·환경 위험
- `exploration_value_score`: 추가 관측 또는 마이크로 탐사선 파견 가치
- `uncertainty_score`: 시스템이 모르는 정도, 확정하지 못하는 정도
- `survival_priority_score`: 생존 가치·위험·거리·임무 맥락을 종합한 우선순위

이 점수들은 HYEAN Operator Interface에서 시각 마커·사이드바·경고·행동 추천에 연결된다.

## 2.7 GWAN의 추천 행동

```text
avoid
wait
observe_more
approach
send_micro_probe
mark_as_long_term_candidate
update_survival_map
request_additional_spectral_observation
```

**이유**: HYEAN은 "좋다/나쁘다"를 말하는 시스템이 아니라, 운영자가 선택할 수 있는 실제 행동 후보를 제안해야 하기 때문.

## 2.8 Cloud Native는 정체성이 아니라 수단이다 ★

가장 중요한 설계 결정 중 하나.

> Cloud-native technology is not the identity of HYEAN.

클라우드 네이티브는 HYEAN/GWAN을 만들고·테스트하고·시뮬레이션하고·배포하고·모니터링하고·개선하기 위한 구현·운영 전략이다.

**유용한 곳**: 지상 기반 데이터 처리 / 공개 우주 데이터 수집 / 시뮬레이션 워크플로 / API 서비스 / 점수화 및 판단 실험 / 장기 메모리와 지도 저장 / 모니터링과 관측 가능성 / 협업과 반복 가능한 배포.

**비효율적인 곳**: 생존-critical 온보드 긴급 판단 / 실시간 충돌 회피 / 저전력 임베디드 로직 / 안전 인증이 필요한 우주선 제어 루프 / 너무 이른 단일 파일 프로토타입.

## 2.9 Onboard / Ground / Cloud 분리

```text
Onboard GWAN Core
- local position reasoning
- local observation intake
- emergency risk detection
- local decision logic
- offline survival map

HYEAN Ground / Cloud Platform
- public space data ingestion
- spectroscopy data processing
- simulation environment
- scoring model evaluation
- mission report API
- memory and map database
- monitoring and experiment tracking

Sync Layer
- observation upload
- map update download
- model/rule update
- conflict and uncertainty handling
```

**이유**: 우주선 내부의 생존 판단은 클라우드 연결이 끊겨도 작동해야 한다. 생존-critical 판단을 클라우드에 의존하면 지연·단절·통신 오류가 곧 위험이 된다.

## 2.10 기술 도입 사다리

기술은 멋있어서 쓰는 것이 아니라 필요할 때만 쓴다.

```text
1. Python 함수, 샘플 데이터, 테스트, 문서
2. FastAPI로 GWAN 점수화/판단 엔드포인트 제공
3. Docker로 재현 가능한 실행 환경 구성
4. Docker Compose로 API + DB + worker 시뮬레이션 구성
5. GitHub Actions로 테스트와 문서 검증 자동화
6. Prometheus/Grafana는 모니터링할 가치가 있을 때 도입
7. Kubernetes는 서비스 수·배포 빈도·워크로드·self-healing 필요성이 생길 때 도입
8. Terraform은 클라우드 인프라를 안정적으로 재생성해야 할 때 도입
```

> 기술은 HYEAN/GWAN의 명확성·신뢰성·테스트·시뮬레이션·배포·모니터링·협업을 복잡도보다 더 크게 개선할 때만 사용한다.

## 2.11 Operator Interface 방향

GWAN은 긴 보고서만 출력하지 않고, HYEAN Operator Interface가 바로 사용할 수 있는 **구조화된 패키지**를 출력한다.

```text
spatial_visualization_package
sidebar_intelligence_package
alert_feed_package
uncertainty_package
decision_report_package
```

> GWAN calculates and explains. HYEAN Operator Interface displays and helps humans decide quickly.

## 2.12 Operator Interface 레이아웃

- **Main Spatial Awareness View**: 3D 또는 semi-3D 공간 인식 화면, 우주선 중심 좌표, 객체·위험·자원·불확실 후보 표시
- **Context & Reason Sidebar**: 선택 객체의 거리·위치·상대 이동·점수·분광 해석·출처·불확실성 이유·추천 행동
- **Alert & Uncertainty Feed**: 긴급 위험, 높은 불확실성, 추가 관측 필요, 마이크로 탐사선 추천, 지도 업데이트 필요 알림
- **Full Decision Report**: 관측 이력·점수 설명·데이터 출처·불확실성·판단 근거·지도 업데이트 기록

**비목표 (확정)**:
- 불확실한 데이터를 확정된 것처럼 보여주지 않는다.
- 장식적 3D 효과로 가독성을 떨어뜨리지 않는다.
- 색상 의미를 애매하게 만들지 않는다.
- GWAN의 판단을 사람이 시각적으로 추측하는 구조로 대체하지 않는다.
- 모든 판단을 긴 보고서로만 확인하게 하지 않는다.

## 2.13 Data Contract

`05_HYEAN_GWAN_Data_Contract.docx`로 GWAN ↔ HYEAN Operator Interface 데이터 계약을 정의. 핵심 구성:

- Global payload envelope
- Coordinate and unit rules
- Shared enumerations
- 5개 package schema (spatial_visualization / sidebar_intelligence / alert_feed / uncertainty / decision_report)
- Full example JSON payload
- Validation rules
- Pydantic / FastAPI implementation direction
- Testing requirements

**이유**: "GWAN이 뭔가 판단한다"에서 멈추지 않고, 실제 구현 가능한 JSON 구조와 Pydantic 모델로 내려가기 위해서.

## 2.14 Data Contract 주요 enum

```text
data_classification:
  known, estimated, simulated, hypothesis, fictional_future_scenario

confidence_label:
  confirmed, likely, uncertain, low_confidence, unknown

display_category:
  energy_candidate, resource_candidate, risk_zone, observation_target,
  uncertain_detection, navigation_reference, micro_probe, long_term_candidate

visual_marker_type:
  pin, region, trajectory, sphere, probe, warning_zone, unknown_point

recommended_action:
  avoid, wait, observe_more, approach, send_micro_probe,
  mark_as_long_term_candidate, update_survival_map,
  request_additional_spectral_observation

alert_severity:
  info, low, medium, high, critical

uncertainty_type:
  weak_signal, missing_data, conflicting_observation, high_distance,
  low_resolution, stale_catalog_data, simulated_only, unknown_source
```

**이유**: 엔진·인터페이스·테스트·문서가 같은 언어를 쓰게 만들기 위해서.

## 2.15 Data Contract 검증 규칙

- sidebar/alert/uncertainty/report의 모든 `object_id`는 spatial_visualization_package에 있거나 non-spatial로 명확히 표시해야 한다.
- 모든 추천에는 `reason_summary` 또는 `reasoning_steps`가 있어야 한다.
- 불확실한 탐지는 `uncertainty_type`, `uncertainty_reason`, `suggested_resolution`을 가져야 한다.
- 모든 출력은 `data_classification`을 직접 가지거나 관련 객체에서 상속해야 한다.
- 인터페이스는 uncertain/hypothetical 데이터를 confirmed처럼 보여주면 안 된다.
- 점수는 별도 버전이 정해지기 전까지 **0~1 숫자**여야 한다.
- 모든 타임스탬프는 **ISO-8601**이어야 한다.
- 좌표 단위는 명확해야 하며, **AU와 km를 라벨 없이 섞으면 안 된다.**

## 2.16 Prevention Layer

HYEAN/GWAN은 위험 발생 후 대응이 아니라 **예방을 우선**하는 시스템으로 확장. Prevention Layer는 기존 시스템 위에 놓이는 상위 해석 계층으로, "아직 위험은 아니지만 조정이 필요한 상태"를 판단한다.

보는 항목: Trend / Pattern / Balance / Early Signal / Recovery Capacity / Preventive Action Priority.

GWAN에 추가할 예방 판단 필드:

```text
risk_score
trend_score
imbalance_score
early_warning_score
recovery_capacity
preventive_action_priority
```

보완된 판단 흐름:

```text
관측 → 기미 감지 → 균형 분석 → 예방 조정 → 위험 판단 → 탐사 결정 → 기억
```

**이유**: HYEAN을 단순 우주 탐사 AI가 아니라, 이동식 지구의 건강을 관리하는 예방형 문명 운영체제로 만들기 위해서.

## 2.17 Cloud Native Korea Lab 운영 결정 (초기)

ChatGPT Project / Project Instructions / 00_Setup_History / 00_Control Center / Google Drive 폴더 구조 / 기준 문서 5개 / ChatGPT Tasks 4개 / Google Calendar 반복 일정 4개 / GitHub Repository / Connector Write Permission / Template Files — 모두 완료.

저장소: `onetwotwothreeone/cloud-native-korea-lab`. 기본 파일: `README.md`, `labs/lab-template.md`, `error-logs/error-log-template.md`, `content/community-post-template.md`.

이 프로젝트는 단순 공부방이 아니라 학습 본부·실습 기록 저장소·에러 해결 아카이브·콘텐츠 제작소·커뮤니티 운영 본부·포트폴리오 제작 시스템으로 정의되었다.

## 2.18 학습 로드맵 (초기 3개월)

```text
Month 1 Foundation:  W1 Linux/Shell/Git · W2 Network/HTTP/DNS/Port · W3 Docker · W4 Docker Compose
Month 2 Kubernetes:  W5 Overview/Pod/Node/Cluster · W6 Deployment/Service/Ingress · W7 ConfigMap/Secret/Volume · W8 Helm
Month 3 Operations:  W9 CI/CD/GitHub Actions · W10 Argo CD/GitOps · W11 Prometheus/Grafana · W12 Terraform/Cloud/Portfolio
```

단, HYEAN/GWAN 전환 이후에는 이 로드맵이 독립 목표가 아니라 **HYEAN/GWAN 구현에 필요한 만큼 단계적으로** 사용된다.

## 2.19 매일 운영 루틴

```text
하루에 하나의 개념을 배우고,
하나의 실습을 진행하고,
하나의 기록을 남기고,
하나의 커뮤니티 글로 공유한다.
(+ 하나의 포트폴리오 노트 저장)
```

**이유**: 완벽하게 알고 시작하는 것이 아니라, 배우는 과정을 공개하면서 한국어 클라우드 네이티브 학습 자료를 쌓기 위해서.

## 2.20 ChatGPT Tasks 정리

유지 Tasks 4개:
- 매일 07:00 — 오늘의 학습 주제·실습·커뮤니티 글감 안내
- 매일 22:00 — 오늘 배운 내용 복습 질문 5개 생성
- 매주 일 20:00 — 주간 요약 + 다음 주 계획 제안
- 매주 월 08:00 — Docker/Kubernetes/CNCF/AWS/GCP/Azure 공식 업데이트 요약

중복 Tasks는 비활성화. **이유**: 중복 알림 없이 하나의 운영 루틴만 유지하기 위해서.

## 2.21 채팅방 역할

- `00_Control Center` — 전체 운영 본부(상태 점검, 다음 액션 결정, Tasks/Calendar/GitHub/Drive 흐름 관리)
- `02_Lab Coach` — 실습 진행(MacBook 기준 안내, 단계별 진행, 결과 정리)
- `03_Error Doctor` — 에러 분석(쉬운 뜻·원인·해결·확인 명령어·재발 방지·공유글)
- `04_Content Factory` — 콘텐츠 변환(카페 업로드용 글, 제목 후보, 초보자 설명)
- `05_Community Manager` — 커뮤니티 운영(공지, 참여 질문, 인증 미션, 온보딩)
- `06_Portfolio Builder` — 포트폴리오 변환(README, 프로젝트 설명, 트러블슈팅, 이력서/면접)

**이유**: 프로젝트가 커질수록 판단·실습·에러·콘텐츠·커뮤니티·포트폴리오가 섞이지 않도록.

## 2.22 콘텐츠 채널

당분간 외부 콘텐츠 업로드 채널은 **네이버 카페로 단일화**.

```text
실습 완료 → GitHub 실습 기록 → 네이버 카페 글 → 댓글 질문 수집
→ 에러와 배운 점 축적 → 추후 블로그/쇼츠/강의/포트폴리오로 재가공
```

**이유**: 초기에는 여러 채널 확장보다 하나의 커뮤니티 거점을 안정적으로 키우는 것이 중요.

## 2.23 네이버 카페 글 형식

```text
제목 / 오늘 한 실습 / 왜 배웠는지 / 초보자용 쉬운 설명 / 실행 명령어 /
성공 확인 방법 / 헷갈렸던 부분 / 오늘 배운 점 3개 / 다음 실습 예고 / 댓글 유도 질문
```

제목 형식: `[오늘의 클라우드 네이티브] 주제명` (예: `[오늘의 클라우드 네이티브] Docker로 Nginx 컨테이너 실행하기`)

## 2.24 첫 실습 완료

Docker 설치 확인 → 버전 확인 → Nginx 컨테이너 실행 → localhost:8080 접속 확인 → 실행 상태 확인 → 정리. Cloud Native Korea Lab의 첫 번째 실습 기록.

## 2.25 Mini Platform 방향 결정과 이후 전환

처음에는 Mini Platform을 작은 웹 서비스로 만들고 Docker/Compose/K8s/Helm/Actions/Argo CD/Prometheus/Terraform/Cloud까지 단계적으로 발전시키기로 함.

2026-06-11 기준 **Cloud Native AI Docs Agent**(공식 문서를 참고해 12살도 이해할 수 있게 답하는 AI 에이전트)로 방향 수정.

이후 HYEAN/GWAN이 최상위 프로젝트가 되면서, Mini Platform과 AI Docs Agent는 **HYEAN/GWAN 구현을 위한 훈련 자산/하위 실험으로 재배치**됨.
