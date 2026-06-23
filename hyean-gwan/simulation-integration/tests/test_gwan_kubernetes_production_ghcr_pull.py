from pathlib import Path

ROOT_WORKFLOW = Path("../../.github/workflows/gwan-ci.yml")
LOCAL_WORKFLOW = Path(".github/workflows/gwan-ci.yml")
PRODUCTION_KUSTOMIZATION = Path("k8s/overlays/production/kustomization.yaml")
PULL_SECRET_PATCH = Path("k8s/overlays/production/gwan-api-image-pull-secret-patch.yaml")
STEP_DOC = Path("docs/27_GWAN_Kubernetes_Production_GHCR_Pull.md")


def test_production_overlay_includes_image_pull_secret_patch() -> None:
    kustomization = PRODUCTION_KUSTOMIZATION.read_text(encoding="utf-8")
    patch = PULL_SECRET_PATCH.read_text(encoding="utf-8")

    assert "gwan-api-image-pull-secret-patch.yaml" in kustomization
    assert "imagePullSecrets" in patch
    assert "ghcr-pull-secret" in patch
    assert "name: gwan-api" in patch


def test_workflow_creates_ghcr_pull_secret_and_applies_production_overlay() -> None:
    text = ROOT_WORKFLOW.read_text(encoding="utf-8")

    assert "Create production kind cluster for GHCR pull" in text
    assert "Create GHCR image pull secret in production kind" in text
    assert "ghcr-pull-secret" in text
    assert "kubectl apply -k k8s/overlays/production" in text
    assert "Production overlay health check through port-forward" in text
    assert "KIND_PRODUCTION_CLUSTER_NAME" in text


def test_local_workflow_copy_stays_in_sync_for_documentation() -> None:
    root = ROOT_WORKFLOW.read_text(encoding="utf-8")
    local = LOCAL_WORKFLOW.read_text(encoding="utf-8")

    assert "Apply Kubernetes production overlay from GHCR" in root
    assert "Apply Kubernetes production overlay from GHCR" in local
    assert "ghcr-pull-secret" in local


def test_step_27_documentation_exists() -> None:
    text = STEP_DOC.read_text(encoding="utf-8")

    assert "27_GWAN_Kubernetes_Production_GHCR_Pull" in text
    assert "Build and push image to GHCR" in text
    assert "imagePullSecrets" in text
    assert "ghcr-pull-secret" in text
    assert "/gwan/memory/db-status" in text
