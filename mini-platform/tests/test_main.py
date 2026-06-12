from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()

    assert data["version"] == "0.1.0"
    assert data["language"] == "Python"
    assert data["framework"] == "FastAPI"


def test_ask():
    response = client.post(
        "/ask",
        json={"question": "Kubernetes에서 Service는 왜 필요한가요?"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["question"] == "Kubernetes에서 Service는 왜 필요한가요?"
    assert "answer" in data
    assert data["source"] == "sample-response"
