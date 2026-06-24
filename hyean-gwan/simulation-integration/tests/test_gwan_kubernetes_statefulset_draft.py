from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_statefulset_draft_files_exist() -> None:
    assert (ROOT / "k8s/drafts/postgres-headless-service-draft.yaml").exists()
    assert (ROOT / "k8s/drafts/postgres-statefulset-draft.yaml").exists()
    assert (ROOT / "k8s/drafts/kustomization.yaml").exists()


def test_statefulset_draft_has_expected_identity_and_storage() -> None:
    text = read("k8s/drafts/postgres-statefulset-draft.yaml")

    assert "kind: StatefulSet" in text
    assert "name: postgres" in text
    assert "serviceName: postgres-headless" in text
    assert "volumeClaimTemplates:" in text
    assert "name: postgres-data" in text
    assert "mountPath: /var/lib/postgresql/data" in text


def test_statefulset_draft_keeps_current_runtime_safety_settings() -> None:
    text = read("k8s/drafts/postgres-statefulset-draft.yaml")

    assert "serviceAccountName: gwan-postgres-sa" in text
    assert "automountServiceAccountToken: false" in text
    assert "seccompProfile:" in text
    assert "type: RuntimeDefault" in text
    assert "allowPrivilegeEscalation: false" in text
    assert "capabilities:" in text
    assert "drop:" in text
    assert "- ALL" in text


def test_statefulset_draft_keeps_postgres_health_and_resources() -> None:
    text = read("k8s/drafts/postgres-statefulset-draft.yaml")

    assert "livenessProbe:" in text
    assert "readinessProbe:" in text
    assert "pg_isready" in text
    assert "resources:" in text
    assert "requests:" in text
    assert "limits:" in text
    assert "cpu: 100m" in text
    assert "memory: 256Mi" in text
    assert "cpu: 500m" in text
    assert "memory: 512Mi" in text


def test_headless_service_draft_exists() -> None:
    text = read("k8s/drafts/postgres-headless-service-draft.yaml")

    assert "kind: Service" in text
    assert "name: postgres-headless" in text
    assert "clusterIP: None" in text
    assert "app.kubernetes.io/name: gwan-postgres" in text
    assert "port: 5432" in text


def test_draft_is_not_in_active_kustomizations_yet() -> None:
    base = read("k8s/base/kustomization.yaml")
    local = read("k8s/overlays/local/kustomization.yaml")

    assert "postgres-statefulset-draft.yaml" not in base
    assert "postgres-headless-service-draft.yaml" not in base
    assert "postgres-statefulset-draft.yaml" not in local
    assert "postgres-headless-service-draft.yaml" not in local


def test_docs_and_prompt_exist() -> None:
    doc = read("docs/44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md")
    prompt = read("codex/44_gwan_kubernetes_statefulset_draft_manifest_prompt.md")

    assert "StatefulSet Draft Manifest" in doc
    assert "Headless Service" in doc
    assert "volumeClaimTemplates" in doc
    assert "45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run" in doc

    assert "Codex Prompt" in prompt
    assert "serviceName: postgres-headless" in prompt
    assert "volumeClaimTemplates" in prompt
