# 제품화 후보 (Productization Candidates) — 기록 (착수 아님)

> 상태: **기록만.** 지금 착수하지 않는다. 착수 시점은 모두 **예방 레이어 v0.1 완성·머지 이후**.
> 목적 정합: 제품 자체가 목적이 아니다. **수익으로 여유·풍요를 얻어 연구에 더 몰두하기 위함**이다 — 본업(연구)을 따라 흐른 결과로 생기는 **부산물**([MOTIVATION.md](MOTIVATION.md), 上善若水). 제품이 본업을 밀어내면 그 순간 [MOTIVATION.md](MOTIVATION.md) 4절 점검 질문으로 되돌아온다.

---

## 왜 기록만 하는가

제품화는 매력적이지만, 지금 벌리면 [DESIGN_HISTORY.md](DESIGN_HISTORY.md)의 H1 패턴(과설계·곁가지 확장)을 반복한다. 그래서 **선택과 집중**: 예방 레이어 v0.1을 먼저 진실하게 세우고, 그 자산이 자연히 제품 씨앗이 되도록 둔다. 이 문서는 그 씨앗들을 **잊지 않기 위한 목록**일 뿐이다.

---

## 후보 비교

| # | 후보 | 예상 수요 / 적용처 | 지금 자산과의 연결점 | 착수 권장 시점 |
|---|------|---------------------|------------------------|----------------|
| 1 | **Cloud Native Korea Lab 교육 콘텐츠·커뮤니티** | 한국어 클라우드 네이티브 입문자, 비전공·주니어, 사내 교육. **가장 현실적·저위험** | [PHILOSOPHY.md](PHILOSOPHY.md) 1.8(원래 교육 비전), 이미 쌓인 `labs/`·에러로그·실습 기록·네이버 카페 운영안 | 예방 레이어 v0.1 머지 이후, 운영 루틴 안정화 단계 |
| 2 | **Prevention Layer 범용화 — rule-based 예방 판단 엔진 라이브러리** | 우주 밖 일반 도메인: **서버/인프라 모니터링, IoT 디바이스 헬스, 알림 피로 저감, SRE 조기경보**. "추세·균형·조기신호·회복여력으로 *사고 전* 조정" 수요 | **지금 만드는 `app/services/prevention/` 패키지가 그 씨앗.** rules/engine 분리 구조(진화 가능성)·severity×prevention 2축·holistic이 그대로 범용 엔진의 골격 | 예방 레이어 v0.1 머지 후, 도메인 비종속 추출(우주 용어 → 일반 용어) 리팩터 단계 |
| 3 | **GWAN 평가·점수화 엔진** | 불확실성을 다루는 **설명가능 판단/스코어링**: 데이터 품질 평가, AI 출력 검수, 사람-검토 워크플로, 리스크 스코어링 | `gwan_judgment`·`gwan_scoring`·Data Contract(enum·검증)·reason_codes·human_review 플래그, [CONTEXT.md](CONTEXT.md) 3.2의 AI Eval 자산 | 예방 레이어 v0.1 머지 후, H4(판단 계약 단일화) 정리 이후 |

---

## 공통 원칙

- **연결점이 약하면 보류**: 위 셋 모두 *이미 만든 자산*에서 자라난다. 새 자산을 처음부터 만들어야 하는 후보는 지금 목록에 올리지 않는다.
- **추출(extract)이지 신규(new)가 아니다**: 특히 후보 2는 예방 레이어가 충분히 자리잡은 뒤 **도메인 비종속 부분만 떼어내는** 방식. 우주 프로젝트를 멈추고 라이브러리를 새로 시작하는 게 아니다.
- **수익은 수단**: 수익 → 여유 → 연구 몰두. 이 순서가 뒤집히면([MOTIVATION.md](MOTIVATION.md) 4절) 멈춘다.

---

> 관련: [MOTIVATION.md](MOTIVATION.md) · [PHILOSOPHY.md](PHILOSOPHY.md) 1.8 · [PREVENTION_LAYER_SPEC.md](PREVENTION_LAYER_SPEC.md) · [REALIGNMENT_BACKLOG.md](REALIGNMENT_BACKLOG.md)
