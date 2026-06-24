from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gwan_api_networkpolicy_exists() -> None:
    path = ROOT / "k8s/base/gwan-api-networkpolicy.yaml"
    text = path.read_text(encoding="utf-8")

    assert "apiVersion: networking.k8s.io/v1" in text
    assert "kind: NetworkPolicy" in text
    assert "name: gwan-api-network-policy" in text
    assert "namespace: hyean-gwan" in text
    assert "app.kubernetes.io/name: gwan-api" in text
    assert "app.kubernetes.io/name: gwan-postgres" in text
    assert "port: 8000" in text
    assert "port: 5432" in text
    assert "port: 53" in text
    assert "Ingress" in text
    assert "Egress" in text


def test_postgres_networkpolicy_exists() -> None:
    path = ROOT / "k8s/base/postgres-networkpolicy.yaml"
    text = path.read_text(encoding="utf-8")

    assert "apiVersion: networking.k8s.io/v1" in text
    assert "kind: NetworkPolicy" in text
    assert "name: gwan-postgres-network-policy" in text
    assert "namespace: hyean-gwan" in text
    assert "app.kubernetes.io/name: gwan-postgres" in text
    assert "app.kubernetes.io/name: gwan-api" in text
    assert "port: 5432" in text
    assert "Ingress" in text


def test_networkpolicies_are_registered_in_kustomization() -> None:
    path = ROOT / "k8s/base/kustomization.yaml"
    text = path.read_text(encoding="utf-8")

    assert "gwan-api-networkpolicy.yaml" in text
    assert "postgres-networkpolicy.yaml" in text


def test_network_policy_check_script_exists() -> None:
    path = ROOT / "scripts/k8s/network_policy_check.sh"
    text = path.read_text(encoding="utf-8")

    assert "kubectl" in text
    assert "get networkpolicy" in text
    assert "describe networkpolicy gwan-api-network-policy" in text
    assert "describe networkpolicy gwan-postgres-network-policy" in text
    assert "CNI" in text


def test_networkpolicy_documentation_exists() -> None:
    path = ROOT / "docs/36_GWAN_Kubernetes_NetworkPolicy_Baseline.md"
    text = path.read_text(encoding="utf-8")

    assert "36_GWAN_Kubernetes_NetworkPolicy_Baseline" in text
    assert "NetworkPolicy" in text
    assert "preventive infrastructure" in text
    assert "gwan-api-network-policy" in text
    assert "gwan-postgres-network-policy" in text


def test_networkpolicy_codex_prompt_exists() -> None:
    path = ROOT / "codex/36_gwan_kubernetes_networkpolicy_baseline_prompt.md"
    text = path.read_text(encoding="utf-8")

    assert "GWAN Kubernetes NetworkPolicy Baseline" in text
    assert "preventive infrastructure" in text
    assert "gwan-api" in text
    assert "gwan-postgres" in text
