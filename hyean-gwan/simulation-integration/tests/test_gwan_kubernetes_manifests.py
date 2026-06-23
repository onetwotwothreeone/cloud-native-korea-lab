from pathlib import Path

BASE = Path("k8s/base")


def read(name: str) -> str:
    return (BASE / name).read_text(encoding="utf-8")


def test_kubernetes_manifest_files_exist() -> None:
    expected_files = [
        "namespace.yaml",
        "postgres-secret.yaml",
        "postgres-service.yaml",
        "postgres-deployment.yaml",
        "gwan-api-service.yaml",
        "gwan-api-deployment.yaml",
        "kustomization.yaml",
    ]

    for filename in expected_files:
        assert (BASE / filename).exists(), filename


def test_kustomization_includes_api_and_postgres_resources() -> None:
    text = read("kustomization.yaml")

    assert "namespace.yaml" in text
    assert "postgres-secret.yaml" in text
    assert "postgres-service.yaml" in text
    assert "postgres-deployment.yaml" in text
    assert "gwan-api-service.yaml" in text
    assert "gwan-api-deployment.yaml" in text


def test_gwan_api_deployment_uses_ghcr_image_and_database_url() -> None:
    text = read("gwan-api-deployment.yaml")

    assert "ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest" in text
    assert "DATABASE_URL" in text
    assert "postgres:5432" in text
    assert "HYEAN_MEMORY_JSONL_PATH" in text
    assert "/health" in text
    assert "readinessProbe" in text
    assert "livenessProbe" in text


def test_postgres_deployment_and_service_are_present() -> None:
    deployment = read("postgres-deployment.yaml")
    service = read("postgres-service.yaml")
    secret = read("postgres-secret.yaml")

    assert "postgres:16-alpine" in deployment
    assert "pg_isready" in deployment
    assert "containerPort: 5432" in deployment
    assert "name: postgres" in service
    assert "port: 5432" in service
    assert "POSTGRES_USER: hyean" in secret
    assert "POSTGRES_PASSWORD: hyean_password" in secret
    assert "POSTGRES_DB: hyean_gwan" in secret


def test_step_23_documentation_exists_and_explains_limitations() -> None:
    text = Path("docs/23_GWAN_Kubernetes_Manifests.md").read_text(encoding="utf-8")

    assert "23_GWAN_Kubernetes_Manifests" in text
    assert "Kubernetes Deployment" in text
    assert "Kubernetes Service" in text
    assert "kubectl apply -k k8s/base" in text
    assert "emptyDir" in text
    assert "PersistentVolumeClaim" in text
