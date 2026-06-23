from pathlib import Path

ROOT_WORKFLOW = Path(".github/workflows/gwan-ci.yml")
DOC = Path("docs/26_GWAN_Kubernetes_CI_With_Kind.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_workflow_contains_kind_cluster_steps() -> None:
    text = read(ROOT_WORKFLOW)

    assert "Install kind" in text
    assert "kind create cluster" in text
    assert "kind load docker-image" in text
    assert "kubectl apply -k k8s/overlays/local" in text
    assert "rollout status deployment/postgres" in text
    assert "rollout status deployment/gwan-api" in text
    assert "Delete kind cluster" in text


def test_workflow_loads_expected_gwan_image_into_kind() -> None:
    text = read(ROOT_WORKFLOW)

    assert "GWAN_KIND_IMAGE" in text
    assert "ghcr.io/onetwotwreeone" not in text
    assert "ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest" in text
    assert "kind load docker-image \"${GWAN_KIND_IMAGE}\"" in text


def test_workflow_checks_kubernetes_api_through_port_forward() -> None:
    text = read(ROOT_WORKFLOW)

    assert "port-forward svc/gwan-api 8000:8000" in text
    assert "curl -f http://127.0.0.1:8000/health" in text
    assert "curl -f http://127.0.0.1:8000/gwan/memory/db-status" in text


def test_step_26_documentation_exists_and_explains_kind_ci() -> None:
    text = read(DOC)

    assert "26_GWAN_Kubernetes_CI_With_Kind" in text
    assert "temporary kind Kubernetes cluster" in text
    assert "Build and load image into kind" in text
    assert "k8s/overlays/local" in text
    assert "Current limitation" in text
