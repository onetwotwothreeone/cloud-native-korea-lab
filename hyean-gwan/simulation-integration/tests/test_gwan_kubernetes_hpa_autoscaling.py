from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPA = ROOT / "k8s/base/gwan-api-hpa.yaml"
KUSTOMIZATION = ROOT / "k8s/base/kustomization.yaml"
WORKFLOW = ROOT / ".github/workflows/gwan-ci.yml"
DOC = ROOT / "docs/32_GWAN_Kubernetes_HPA_Autoscaling_Baseline.md"
SCRIPT = ROOT / "scripts/k8s/hpa_check.sh"


def test_hpa_manifest_exists_and_targets_gwan_api() -> None:
    text = HPA.read_text(encoding="utf-8")
    assert "apiVersion: autoscaling/v2" in text
    assert "kind: HorizontalPodAutoscaler" in text
    assert "name: gwan-api-hpa" in text
    assert "scaleTargetRef:" in text
    assert "kind: Deployment" in text
    assert "name: gwan-api" in text


def test_hpa_has_safe_baseline_scaling_bounds_and_cpu_target() -> None:
    text = HPA.read_text(encoding="utf-8")
    assert "minReplicas: 1" in text
    assert "maxReplicas: 3" in text
    assert "type: Resource" in text
    assert "name: cpu" in text
    assert "averageUtilization: 70" in text


def test_base_kustomization_includes_hpa() -> None:
    text = KUSTOMIZATION.read_text(encoding="utf-8")
    assert "gwan-api-hpa.yaml" in text
    assert "resourcequota.yaml" in text
    assert "limitrange.yaml" in text


def test_workflow_uses_fixed_variable_names_and_checks_hpa() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "KIND_CLUSTER_NAME" in text
    assert "KIND_PRODUCTION_CLUSTER_NAME" in text
    assert "GWAN_KIND_IMAGE" in text
    assert "GHCR_IMAGE_NAME" in text
    assert "docs/32_GWAN_Kubernetes_HPA_Autoscaling_Baseline.md" in text
    assert "scripts/k8s/hpa_check.sh" in text


def test_hpa_check_script_documents_metrics_server_caveat() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert "kubectl" in text
    assert "get hpa" in text
    assert "describe hpa" in text
    assert "metrics-server" in text


def test_step_32_documentation_exists() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "32_GWAN_Kubernetes_HPA_Autoscaling_Baseline" in text
    assert "HorizontalPodAutoscaler" in text
    assert "metrics-server" in text
    assert "minReplicas" in text
    assert "maxReplicas" in text
