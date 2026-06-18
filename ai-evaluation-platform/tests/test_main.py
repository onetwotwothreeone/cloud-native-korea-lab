from fastapi.testclient import TestClient

from app.main import app, samples, tasks


client = TestClient(app)


def setup_function():
    tasks.clear()
    samples.clear()


def create_task_for_test() -> str:
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
    return response.json()["id"]


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


def test_create_sample():
    task_id = create_task_for_test()

    response = client.post(
        "/samples",
        json={
            "task_id": task_id,
            "sample_type": "text",
            "content": "Kubernetes Service는 Pod에 안정적으로 접근하게 해주는 네트워크 입구입니다.",
            "language": "ko",
            "metadata": {
                "source": "synthetic",
                "domain": "cloud-native",
            },
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["task_id"] == task_id
    assert data["sample_type"] == "text"
    assert data["language"] == "ko"
    assert data["metadata"]["source"] == "synthetic"
    assert "id" in data
    assert "created_at" in data


def test_list_samples():
    task_id = create_task_for_test()

    client.post(
        "/samples",
        json={
            "task_id": task_id,
            "sample_type": "text",
            "content": "FastAPI는 Python으로 API를 만들기 위한 웹 프레임워크입니다.",
            "language": "ko",
        },
    )

    response = client.get("/samples")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["task_id"] == task_id
    assert data[0]["sample_type"] == "text"


def test_get_sample_by_id():
    task_id = create_task_for_test()

    create_response = client.post(
        "/samples",
        json={
            "task_id": task_id,
            "sample_type": "audio",
            "transcript": "안녕하세요. 오늘은 Kubernetes에 대해 설명하겠습니다.",
            "language": "ko",
            "metadata": {
                "audio_quality": "clear",
                "speaker": "self-created",
            },
        },
    )

    sample_id = create_response.json()["id"]

    response = client.get(f"/samples/{sample_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == sample_id
    assert data["sample_type"] == "audio"
    assert data["transcript"] == "안녕하세요. 오늘은 Kubernetes에 대해 설명하겠습니다."
    assert data["metadata"]["audio_quality"] == "clear"


def test_create_sample_with_invalid_task_id_returns_404():
    response = client.post(
        "/samples",
        json={
            "task_id": "missing-task-id",
            "sample_type": "text",
            "content": "This sample should fail because the task does not exist.",
            "language": "en",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found: missing-task-id"


def test_get_missing_sample_returns_404():
    response = client.get("/samples/missing-sample-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sample not found: missing-sample-id"
