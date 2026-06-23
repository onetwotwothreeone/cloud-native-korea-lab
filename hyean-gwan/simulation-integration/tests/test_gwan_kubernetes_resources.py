from pathlib import Path


ROOT_WORKFLOW = Path("../../.github/workflows/gwan-ci.yml")
LOCAL_WORKFLOW = Path(".github/workflows/gwan-ci.yml")
GWAN_API_DEPLOYMENT = Path("k8s/base/gwan-api-deployment.yaml")
POSTGRES_DEPLOYMENT = Path("k8s/base/postgres-deployment.yaml")
DOC = Path("docs/30_GWAN_Kubernetes_Resource_Requests_And_Limits.md")
SCRIPT = Path("scripts/k8s/resource_check.sh")


def test_gwan_api_has_resource_requests_and_limits() -> None:
    text = GWAN_API_DEPLOYMENT.read_text(encoding="utf-8")

    assert "name: gwan-api" in text
    assert "resources:" in text
    assert "requests:" in text
    assert "limits:" in text
    assert "cpu: 100m" in text
    assert "memory: 128Mi" in text
    assert "cpu: 500m" in text
    assert "memory: 512Mi" in text
    assert "startupProbe" in text
    assert "readinessProbe" in text
    assert "livenessProbe" in text


def test_postgres_has_resource_requests_and_limits() -> None:
    text = POSTGRES_DEPLOYMENT.read_text(encoding="utf-8")

    assert "name: postgres" in text
    assert "resources:" in text
    assert "requests:" in text
    assert "limits:" in text
    assert "cpu: 100m" in text
    assert "memory: 256Mi" in text
    assert "cpu: 500m" in text
    assert "memory: 512Mi" in text
    assert "pg_isready" in text


def test_resource_documentation_exists() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "30_GWAN_Kubernetes_Resource_Requests_And_Limits" in text
    assert "requests" in text
    assert "limits" in text
    assert "gwan-api" in text
    assert "postgres" in text
    assert "kubectl top pods" in text


def test_resource_check_script_exists() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "resource_check" in str(SCRIPT)
    assert "kubectl" in text
    assert "gwan-api" in text
    assert "postgres" in text
    assert "requests.cpu" in text
    assert "limits.memory" in text


def test_workflows_check_step_30_documentation() -> None:
    for workflow in [ROOT_WORKFLOW, LOCAL_WORKFLOW]:
        text = workflow.read_text(encoding="utf-8")
        assert "docs/29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline.md" in text
        assert "docs/30_GWAN_Kubernetes_Resource_Requests_And_Limits.md" in text
        assert "KIND_CLUSTER_NAME" in text
        assert "KIND_PRODUCTION_CLUSTER_NAME" in text
        assert "GWAN_KIND_IMAGE" in text
        assert "GHCR_IMAGE_NAME" in text
