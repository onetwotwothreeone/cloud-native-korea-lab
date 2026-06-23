from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_WORKFLOW = ROOT.parents[1] / ".github/workflows/gwan-ci.yml"
LOCAL_WORKFLOW = ROOT / ".github/workflows/gwan-ci.yml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_metrics_server_readiness_documentation_exists() -> None:
    text = read(ROOT / "docs/33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness.md")

    assert "Metrics Server" in text
    assert "metrics.k8s.io" in text
    assert "kubectl top" in text
    assert "gwan-api-hpa" in text
    assert "HPA" in text


def test_metrics_server_check_script_is_safe_for_local_and_ci() -> None:
    path = ROOT / "scripts/k8s/metrics_server_check.sh"
    text = read(path)

    assert "v1beta1.metrics.k8s.io" in text
    assert "kubectl top nodes" in text
    assert "kubectl top pods" in text
    assert "gwan-api-hpa" in text
    assert "exit 0" in text
    assert "Metrics APIService" in text


def test_optional_metrics_server_install_script_exists() -> None:
    text = read(ROOT / "scripts/k8s/install_metrics_server_local.sh")

    assert "metrics-server" in text
    assert "components.yaml" in text
    assert "--kubelet-insecure-tls" in text
    assert "rollout status deployment/metrics-server" in text


def test_workflow_checks_step_33_docs_and_metrics_readiness() -> None:
    for workflow in [ROOT_WORKFLOW, LOCAL_WORKFLOW]:
        text = read(workflow)

        assert "KIND_CLUSTER_NAME" in text
        assert "KIND_PRODUCTION_CLUSTER_NAME" in text
        assert "GWAN_KIND_IMAGE" in text
        assert "GHCR_IMAGE_NAME" in text
        assert "33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness.md" in text
        assert "Kubernetes metrics server readiness check" in text
        assert "scripts/k8s/metrics_server_check.sh" in text
        assert "Production metrics server readiness check" in text


def test_hpa_manifest_still_targets_gwan_api() -> None:
    text = read(ROOT / "k8s/base/gwan-api-hpa.yaml")

    assert "kind: HorizontalPodAutoscaler" in text
    assert "apiVersion: autoscaling/v2" in text
    assert "name: gwan-api-hpa" in text
    assert "name: gwan-api" in text
    assert "averageUtilization: 70" in text
