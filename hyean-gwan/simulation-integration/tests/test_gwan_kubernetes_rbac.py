from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gwan_api_rbac_manifest_exists() -> None:
    path = ROOT / "k8s/base/gwan-api-rbac.yaml"
    text = path.read_text(encoding="utf-8")

    assert "kind: ServiceAccount" in text
    assert "name: gwan-api-sa" in text
    assert "automountServiceAccountToken: false" in text
    assert "kind: Role" in text
    assert "name: gwan-api-minimal-role" in text
    assert "rules: []" in text
    assert "kind: RoleBinding" in text
    assert "name: gwan-api-minimal-rolebinding" in text


def test_postgres_rbac_manifest_exists() -> None:
    path = ROOT / "k8s/base/postgres-rbac.yaml"
    text = path.read_text(encoding="utf-8")

    assert "kind: ServiceAccount" in text
    assert "name: gwan-postgres-sa" in text
    assert "automountServiceAccountToken: false" in text
    assert "kind: Role" in text
    assert "name: gwan-postgres-minimal-role" in text
    assert "rules: []" in text
    assert "kind: RoleBinding" in text
    assert "name: gwan-postgres-minimal-rolebinding" in text


def test_rbac_manifests_are_registered_in_kustomization() -> None:
    path = ROOT / "k8s/base/kustomization.yaml"
    text = path.read_text(encoding="utf-8")

    assert "gwan-api-rbac.yaml" in text
    assert "postgres-rbac.yaml" in text


def test_gwan_api_deployment_uses_dedicated_service_account() -> None:
    path = ROOT / "k8s/base/gwan-api-deployment.yaml"
    text = path.read_text(encoding="utf-8")

    assert "serviceAccountName: gwan-api-sa" in text
    assert "automountServiceAccountToken: false" in text


def test_postgres_deployment_uses_dedicated_service_account() -> None:
    path = ROOT / "k8s/base/postgres-deployment.yaml"
    text = path.read_text(encoding="utf-8")

    assert "serviceAccountName: gwan-postgres-sa" in text
    assert "automountServiceAccountToken: false" in text


def test_rbac_check_script_exists() -> None:
    path = ROOT / "scripts/k8s/rbac_check.sh"
    text = path.read_text(encoding="utf-8")

    assert "kubectl" in text
    assert "get serviceaccount gwan-api-sa" in text
    assert "get serviceaccount gwan-postgres-sa" in text
    assert "auth can-i" in text


def test_rbac_documentation_exists() -> None:
    path = ROOT / "docs/37_GWAN_Kubernetes_ServiceAccount_RBAC_Baseline.md"
    text = path.read_text(encoding="utf-8")

    assert "37_GWAN_Kubernetes_ServiceAccount_RBAC_Baseline" in text
    assert "least-privilege" in text
    assert "preventive identity control" in text
    assert "gwan-api-sa" in text
    assert "gwan-postgres-sa" in text
