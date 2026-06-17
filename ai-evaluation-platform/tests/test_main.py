from fastapi.testclient import TestClient

from app.main import app, tasks


client = TestClient(app)


def setup_function():
    tasks.clear()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()

    assert data["version"] == "0.1.0"
    assert data["project"] == "ai-evaluation-platform"
    assert data["framework"] == "FastAPI"


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Evaluate Korean AI Tutor response",
            "task_type": "text",
            "language": "ko",
            "description": "Check clarity, accuracy, and naturalness.",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Evaluate Korean AI Tutor response"
    assert data["task_type"] == "text"
    assert data["language"] == "ko"
    assert data["status"] == "open"
    assert "id" in data
    assert "created_at" in data


def test_list_tasks():
    client.post(
        "/tasks",
        json={
            "title": "Evaluate Korean speech transcript",
            "task_type": "audio",
            "language": "ko",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Evaluate Korean speech transcript"
    assert data[0]["task_type"] == "audio"
