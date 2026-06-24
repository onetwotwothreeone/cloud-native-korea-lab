from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_statefulset_design_review_doc_exists() -> None:
    doc = ROOT / "docs/41_GWAN_Kubernetes_StatefulSet_Design_Review.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "StatefulSet" in text
    assert "Deployment" in text
    assert "PersistentVolumeClaim" in text
    assert "42_GWAN_Kubernetes_StatefulSet_Migration_Plan" in text


def test_codex_prompt_exists_for_statefulset_review() -> None:
    prompt = ROOT / "codex/41_gwan_kubernetes_statefulset_design_review_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")
    assert "Do not convert PostgreSQL to StatefulSet yet" in text
    assert "Deployment + PVC" in text
    assert "42_GWAN_Kubernetes_StatefulSet_Migration_Plan" in text


def test_postgres_uses_persistent_volume_claim() -> None:
    text = read("k8s/base/postgres-deployment.yaml")

    assert "kind: Deployment" in text
    assert "name: postgres" in text
    assert "persistentVolumeClaim" in text
    assert "claimName: postgres-data" in text
    assert "mountPath: /var/lib/postgresql/data" in text


def test_postgres_pvc_exists() -> None:
    text = read("k8s/base/postgres-pvc.yaml")

    assert "kind: PersistentVolumeClaim" in text
    assert "name: postgres-data" in text
    assert "ReadWriteOnce" in text


def test_statefulset_review_script_exists() -> None:
    script = ROOT / "scripts/k8s/statefulset_design_review_check.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")
    assert "kubectl" in text
    assert "get pvc postgres-data" in text
    assert "get deployment postgres" in text
    assert "get statefulset" in text
