from fastapi.testclient import TestClient

from app.main import app
from app.services.gwan_simulation import generate_first_simulation_payload

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_validate_interface_payload_endpoint() -> None:
    payload = generate_first_simulation_payload()
    response = client.post("/gwan/interface-payload", json=payload.model_dump(mode="json"))

    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == "hyean.gwan.interface.v0.1"
    assert body["packages"]["spatial_visualization_package"]["objects"][0]["object_id"] == "candidate-resource-stable-001"
