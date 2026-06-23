from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_resourcequota_manifest_exists_and_sets_namespace_budget() -> None:
    text = read("k8s/base/resourcequota.yaml")

    assert "kind: ResourceQuota" in text
    assert "name: hyean-gwan-resource-quota" in text
    assert "namespace: hyean-gwan" in text
    assert "requests.cpu" in text
    assert "requests.memory" in text
    assert "limits.cpu" in text
    assert "limits.memory" in text
    assert "pods:" in text
    assert "services:" in text
    assert "secrets:" in text
    assert "configmaps:" in text


def test_limitrange_manifest_exists_and_sets_container_defaults() -> None:
    text = read("k8s/base/limitrange.yaml")

    assert "kind: LimitRange" in text
    assert "name: hyean-gwan-default-container-limits" in text
    assert "namespace: hyean-gwan" in text
    assert "defaultRequest" in text
    assert "default:" in text
    assert "min:" in text
    assert "max:" in text
    assert "cpu: 500m" in text
    assert "memory: 512Mi" in text


def test_base_kustomization_includes_namespace_policies() -> None:
    text = read("k8s/base/kustomization.yaml")

    assert "resourcequota.yaml" in text
    assert "limitrange.yaml" in text


def test_namespace_policy_check_script_exists() -> None:
    path = ROOT / "scripts/k8s/namespace_policy_check.sh"
    text = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "set -euo pipefail" in text
    assert "kubectl -n" in text
    assert "get resourcequota hyean-gwan-resource-quota" in text
    assert "get limitrange hyean-gwan-default-container-limits" in text


def test_workflow_checks_step_31_docs_and_namespace_policy() -> None:
    workflow_paths = [
        REPO_ROOT / ".github/workflows/gwan-ci.yml",
        ROOT / ".github/workflows/gwan-ci.yml",
    ]

    for path in workflow_paths:
        text = path.read_text(encoding="utf-8")
        assert "31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange.md" in text
        assert "Kubernetes namespace policy check" in text
        assert "Production namespace policy check" in text
        assert "scripts/k8s/namespace_policy_check.sh" in text
