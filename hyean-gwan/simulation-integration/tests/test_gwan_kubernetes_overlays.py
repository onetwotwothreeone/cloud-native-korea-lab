from pathlib import Path

BASE_DEPLOYMENT = Path("k8s/base/gwan-api-deployment.yaml")
LOCAL = Path("k8s/overlays/local")
PRODUCTION = Path("k8s/overlays/production")
DOC = Path("docs/25_GWAN_Kubernetes_Overlays_Local_And_Production.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_base_deployment_is_production_safe_by_default() -> None:
    text = read(BASE_DEPLOYMENT)

    assert "ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest" in text
    assert "imagePullPolicy: IfNotPresent" in text
    assert "imagePullPolicy: Never" not in text


def test_local_overlay_sets_image_pull_policy_never() -> None:
    kustomization = read(LOCAL / "kustomization.yaml")
    patch = read(LOCAL / "gwan-api-image-pull-policy-patch.yaml")

    assert "../../base" in kustomization
    assert "gwan-api-image-pull-policy-patch.yaml" in kustomization
    assert "name: gwan-api" in patch
    assert "namespace: hyean-gwan" in patch
    assert "imagePullPolicy: Never" in patch


def test_production_overlay_sets_image_pull_policy_if_not_present() -> None:
    kustomization = read(PRODUCTION / "kustomization.yaml")
    patch = read(PRODUCTION / "gwan-api-image-pull-policy-patch.yaml")

    assert "../../base" in kustomization
    assert "gwan-api-image-pull-policy-patch.yaml" in kustomization
    assert "name: gwan-api" in patch
    assert "namespace: hyean-gwan" in patch
    assert "imagePullPolicy: IfNotPresent" in patch
    assert "imagePullPolicy: Never" not in patch


def test_local_scripts_use_local_overlay() -> None:
    apply_text = read(Path("scripts/k8s/apply_local.sh"))
    cleanup_text = read(Path("scripts/k8s/cleanup_local.sh"))

    assert 'KUSTOMIZE_PATH="k8s/overlays/local"' in apply_text
    assert "docker build -t" in apply_text
    assert "kubectl apply -k \"$KUSTOMIZE_PATH\"" in apply_text
    assert 'KUSTOMIZE_PATH="k8s/overlays/local"' in cleanup_text
    assert "kubectl delete -k \"$KUSTOMIZE_PATH\"" in cleanup_text


def test_step_25_documentation_explains_local_and_production_split() -> None:
    text = read(DOC)

    assert "25_GWAN_Kubernetes_Overlays_Local_And_Production" in text
    assert "k8s/overlays/local" in text
    assert "k8s/overlays/production" in text
    assert "imagePullPolicy: Never" in text
    assert "imagePullPolicy: IfNotPresent" in text
