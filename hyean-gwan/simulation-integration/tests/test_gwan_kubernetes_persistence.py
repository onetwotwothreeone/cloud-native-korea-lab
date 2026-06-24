from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "k8s" / "base"


def test_postgres_pvc_manifest_exists():
    path = BASE / "postgres-pvc.yaml"
    assert path.exists()

    text = path.read_text(encoding="utf-8")

    assert "kind: PersistentVolumeClaim" in text
    assert "name: postgres-data" in text
    assert "namespace: hyean-gwan" in text
    assert "ReadWriteOnce" in text
    assert "storage: 1Gi" in text


def test_kustomization_includes_postgres_pvc():
    path = BASE / "kustomization.yaml"
    text = path.read_text(encoding="utf-8")

    assert "postgres-pvc.yaml" in text


def test_postgres_deployment_uses_persistent_volume_claim():
    path = BASE / "postgres-deployment.yaml"
    text = path.read_text(encoding="utf-8")

    assert "persistentVolumeClaim:" in text
    assert "claimName: postgres-data" in text
    assert "mountPath: /var/lib/postgresql/data" in text
    assert "emptyDir: {}" not in text


def test_persistence_check_script_exists():
    path = ROOT / "scripts" / "k8s" / "persistence_check.sh"
    assert path.exists()

    text = path.read_text(encoding="utf-8")

    assert "kubectl -n" in text
    assert "get pvc postgres-data" in text
    assert "describe pvc postgres-data" in text
    assert "persistentVolumeClaim" in text


def test_docs_and_codex_prompt_exist():
    doc = ROOT / "docs" / "40_GWAN_Kubernetes_Persistence_Baseline.md"
    prompt = ROOT / "codex" / "40_gwan_kubernetes_persistence_baseline_prompt.md"

    assert doc.exists()
    assert prompt.exists()

    assert "PersistentVolumeClaim" in doc.read_text(encoding="utf-8")
    assert "41_GWAN_Kubernetes_StatefulSet_Design_Review" in prompt.read_text(encoding="utf-8")
