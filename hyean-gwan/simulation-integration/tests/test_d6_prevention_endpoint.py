"""D6 예방 포함 시뮬레이션 엔드포인트 검증 테스트 (TDD: 구현 전 red).

대상: POST /gwan/simulate-with-prevention (아직 없음 → 404 가 red).
검사:
  1. 정상 요청 -> 200 + payload.prevention 이 HTTP 경유로도 실제 채워짐
  2. 채워진 값이 assess_prevention 결과와 100% 일치 (품질 가드, JSON 직렬화 경유 후에도)
  3. 오타/미지 필드 -> 422 반려 (엄격 경계 — 조용한 무시 차단)
     a) 최상위  b) prevention_input 내부  c) readings 항목 내부
  4. prevention_input 누락 -> 422 (필수 필드)
  5. 기존 /simulate, /simulate-integrated 는 여전히 prevention=None (기존 문 무변경 가드 — red 단계에서도 green 이 정상)
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.prevention import assess_prevention
from app.services.prevention.contract_adapter import to_prevention_report
from app.services.prevention.models import PreventionInput

client = TestClient(app)

ENDPOINT = "/gwan/simulate-with-prevention"

_READING_1 = {
    "composite_risk": 0.35, "uncertainty": 0.50, "energy_level": 0.40,
    "energy_consumption_rate": 0.60, "recovery_capacity": 0.40,
    "resource_pursuit": 0.70, "risk_exposure": 0.60, "anomaly_flags": 1,
}
_READING_2 = {
    "composite_risk": 0.60, "uncertainty": 0.70, "energy_level": 0.35,
    "energy_consumption_rate": 0.65, "recovery_capacity": 0.40,
    "resource_pursuit": 0.75, "risk_exposure": 0.65, "anomaly_flags": 2,
}

SAMPLE_PREVENTION_INPUT = {
    "readings": [_READING_1, _READING_2],
    "severity_context": "restrict",
}


# --------------------------------------------------------------------------- #
# 1. 정상 요청 -> 200 + prevention 이 HTTP 경유로도 채워짐
# --------------------------------------------------------------------------- #
def test_endpoint_populates_prevention_via_http():
    response = client.post(ENDPOINT, json={"prevention_input": SAMPLE_PREVENTION_INPUT})

    assert response.status_code == 200
    body = response.json()
    assert body["payload"]["prevention"] is not None
    assert body["payload"]["prevention"]["prevention_status"] in {
        "normal", "watch", "adjust", "restrict", "shelter_or_abort"
    }
    assert body["payload"]["schema_version"] == "hyean.gwan.interface.v0.1"


# --------------------------------------------------------------------------- #
# 2. 품질 가드: HTTP/JSON 직렬화를 거쳐도 assess_prevention 결과와 100% 일치
# --------------------------------------------------------------------------- #
def test_endpoint_prevention_matches_assessment_exactly():
    response = client.post(ENDPOINT, json={"prevention_input": SAMPLE_PREVENTION_INPUT})
    assert response.status_code == 200

    expected = to_prevention_report(
        assess_prevention(PreventionInput(**SAMPLE_PREVENTION_INPUT))
    ).model_dump(mode="json")
    got = response.json()["payload"]["prevention"]

    assert got == expected  # 10필드 전부(점수 소수점·reason_codes 순서 포함) 동일


# --------------------------------------------------------------------------- #
# 3. 엄격 경계: 오타/미지 필드는 조용히 무시되지 않고 422 로 반려
# --------------------------------------------------------------------------- #
def test_unknown_top_level_field_rejected_422():
    response = client.post(
        ENDPOINT,
        json={"prevention_input": SAMPLE_PREVENTION_INPUT, "preventoin_input": {}},  # 오타 필드
    )
    assert response.status_code == 422


def test_unknown_field_inside_prevention_input_rejected_422():
    bad_input = {**SAMPLE_PREVENTION_INPUT, "severity_contxt": "restrict"}  # 내부 오타
    response = client.post(ENDPOINT, json={"prevention_input": bad_input})
    assert response.status_code == 422


def test_unknown_field_inside_reading_rejected_422():
    bad_reading = {**_READING_1, "composite_rsik": 0.9}  # reading 항목 내부 오타
    bad_input = {"readings": [bad_reading, _READING_2], "severity_context": "restrict"}
    response = client.post(ENDPOINT, json={"prevention_input": bad_input})
    assert response.status_code == 422


# --------------------------------------------------------------------------- #
# 4. prevention_input 누락 -> 422 (필수 필드)
# --------------------------------------------------------------------------- #
def test_missing_prevention_input_rejected_422():
    response = client.post(ENDPOINT, json={})
    assert response.status_code == 422


# --------------------------------------------------------------------------- #
# 5. 기존 문 무변경 가드: /simulate, /simulate-integrated 는 여전히 prevention=None
#    (red 단계에서도 green 이 정상 — 회귀 가드)
# --------------------------------------------------------------------------- #
def test_existing_doors_unchanged_prevention_none():
    simulate = client.post("/gwan/simulate", json={})
    assert simulate.status_code == 200
    assert simulate.json().get("prevention") is None

    integrated = client.post("/gwan/simulate-integrated", json={})
    assert integrated.status_code == 200
    assert integrated.json()["payload"].get("prevention") is None
