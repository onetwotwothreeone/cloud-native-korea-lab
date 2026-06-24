from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_configmap_contains_non_sensitive_runtime_settings() -> None:
    text = read("k8s/base/gwan-api-configmap.yaml")

    assert "kind: ConfigMap" in text
    assert "gwan-api-config" in text

    expected_keys = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_DIALECT",
        "HYEAN_MEMORY_JSONL_PATH",
    ]

    for key in expected_keys:
        assert key in text

    assert "POSTGRES_PASSWORD" not in text
    assert "hyean_password" not in text


def test_secret_contains_database_credentials() -> None:
    text = read("k8s/base/postgres-secret.yaml")

    assert "kind: Secret" in text
    assert "gwan-postgres-secret" in text
    assert "POSTGRES_USER" in text
    assert "POSTGRES_PASSWORD" in text
    assert "POSTGRES_DB" in text


def test_gwan_api_deployment_uses_configmap_and_secret() -> None:
    text = read("k8s/base/gwan-api-deployment.yaml")

    assert "gwan-api-config" in text
    assert "configMapKeyRef" in text
    assert "gwan-postgres-secret" in text
    assert "secretKeyRef" in text
    assert "POSTGRES_PASSWORD" in text

    expected_keys = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_DIALECT",
        "HYEAN_MEMORY_JSONL_PATH",
    ]

    for key in expected_keys:
        assert key in text

    assert "hyean_password" not in text


def test_postgres_deployment_uses_secret() -> None:
    text = read("k8s/base/postgres-deployment.yaml")

    assert "gwan-postgres-secret" in text
    assert "secretRef" in text or "secretKeyRef" in text


def test_config_secret_check_script_exists() -> None:
    text = read("scripts/k8s/config_secret_check.sh")

    assert "ConfigMap" in text
    assert "Secret" in text
    assert "gwan-api-config" in text
    assert "gwan-postgres-secret" in text
    assert "raw database password is not hardcoded" in text


def test_step_39_documentation_exists() -> None:
    text = read("docs/39_GWAN_Kubernetes_Config_And_Secret_Refinement.md")

    assert "39_GWAN_Kubernetes_Config_And_Secret_Refinement" in text
    assert "ConfigMap" in text
    assert "Secret" in text
    assert "HYEAN/GWAN" in text
