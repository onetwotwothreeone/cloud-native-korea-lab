from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gwan_api_pdb_manifest_exists() -> None:
    path = ROOT / "k8s/base/gwan-api-pdb.yaml"
    text = path.read_text(encoding="utf-8")

    assert "apiVersion: policy/v1" in text
    assert "kind: PodDisruptionBudget" in text
    assert "name: gwan-api-pdb" in text
    assert "namespace: hyean-gwan" in text
    assert "minAvailable: 1" in text
    assert "app.kubernetes.io/name: gwan-api" in text


def test_gwan_api_pdb_is_registered_in_kustomization() -> None:
    path = ROOT / "k8s/base/kustomization.yaml"
    text = path.read_text(encoding="utf-8")

    assert "gwan-api-pdb.yaml" in text


def test_pdb_check_script_exists() -> None:
    path = ROOT / "scripts/k8s/pdb_check.sh"
    text = path.read_text(encoding="utf-8")

    assert "kubectl" in text
    assert "get pdb" in text
    assert "describe pdb" in text
    assert "minAvailable" in text


def test_pdb_documentation_exists() -> None:
    path = ROOT / "docs/35_GWAN_Kubernetes_PodDisruptionBudget.md"
    text = path.read_text(encoding="utf-8")

    assert "35_GWAN_Kubernetes_PodDisruptionBudget" in text
    assert "PodDisruptionBudget" in text
    assert "minAvailable: 1" in text
    assert "GWAN" in text
