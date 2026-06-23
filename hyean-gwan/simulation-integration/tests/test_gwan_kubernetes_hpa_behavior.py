from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hpa_behavior_policy_exists() -> None:
    hpa = ROOT / "k8s/base/gwan-api-hpa.yaml"
    text = hpa.read_text(encoding="utf-8")

    assert "kind: HorizontalPodAutoscaler" in text
    assert "behavior:" in text
    assert "scaleUp:" in text
    assert "scaleDown:" in text
    assert "stabilizationWindowSeconds: 60" in text
    assert "stabilizationWindowSeconds: 300" in text
    assert "periodSeconds: 60" in text
    assert "periodSeconds: 120" in text


def test_hpa_behavior_check_script_exists() -> None:
    script = ROOT / "scripts/k8s/hpa_behavior_check.sh"
    text = script.read_text(encoding="utf-8")

    assert "kubectl" in text
    assert "get hpa" in text
    assert "describe hpa" in text
    assert "behavior" in text


def test_hpa_behavior_documentation_exists() -> None:
    doc = ROOT / "docs/34_GWAN_Kubernetes_HPA_Behavior_Policy.md"
    text = doc.read_text(encoding="utf-8")

    assert "34_GWAN_Kubernetes_HPA_Behavior_Policy" in text
    assert "scaleUp" in text
    assert "scaleDown" in text
    assert "GWAN" in text
