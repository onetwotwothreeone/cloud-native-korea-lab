from pathlib import Path

BASE = Path("k8s/base")
DOC = Path("docs/28_GWAN_Kubernetes_Production_Secrets_And_Config.md")


def test_gwan_api_configmap_exists_and_contains_non_sensitive_settings():
    text = (BASE / "gwan-api-configmap.yaml").read_text(encoding="utf-8")

    assert "kind: ConfigMap" in text
    assert "name: gwan-api-config" in text
    assert "DATABASE_HOST: postgres" in text
    assert 'DATABASE_PORT: "5432"' in text
    assert "DATABASE_NAME: hyean_gwan" in text
    assert "DATABASE_USER: hyean" in text
    assert "HYEAN_MEMORY_JSONL_PATH: /tmp/hyean-gwan-memory.jsonl" in text
    assert "POSTGRES_PASSWORD" not in text


def test_base_kustomization_includes_configmap():
    text = (BASE / "kustomization.yaml").read_text(encoding="utf-8")

    assert "gwan-api-configmap.yaml" in text
    assert text.index("postgres-secret.yaml") < text.index("gwan-api-configmap.yaml")


def test_gwan_api_deployment_uses_configmap_and_secret_refs():
    text = (BASE / "gwan-api-deployment.yaml").read_text(encoding="utf-8")

    assert "configMapKeyRef:" in text
    assert "name: gwan-api-config" in text
    assert "secretKeyRef:" in text
    assert "name: gwan-postgres-secret" in text
    assert "key: POSTGRES_PASSWORD" in text
    assert "$(DATABASE_USER):$(POSTGRES_PASSWORD)@$(DATABASE_HOST):$(DATABASE_PORT)/$(DATABASE_NAME)" in text
    assert "value: postgresql+psycopg://hyean:$(POSTGRES_PASSWORD)@postgres:5432/hyean_gwan" not in text


def test_overlays_still_exist_after_config_split():
    assert Path("k8s/overlays/local/kustomization.yaml").exists()
    assert Path("k8s/overlays/production/kustomization.yaml").exists()
    assert Path("k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml").exists()


def test_step_28_documentation_exists():
    text = DOC.read_text(encoding="utf-8")

    assert "28_GWAN_Kubernetes_Production_Secrets_And_Config" in text
    assert "ConfigMap" in text
    assert "Secret" in text
    assert "DATABASE_URL" in text
    assert "POSTGRES_PASSWORD" in text
