from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_preexecution_safety_snapshot_doc_exists():
    doc = ROOT / "docs" / "62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot.md"
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")

    assert "Pre-Execution Safety Snapshot" in text
    assert "CURRENT_DECISION=NO_GO" in text
    assert "APPROVED_BY_OPERATOR=false" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "SNAPSHOT_REQUIRED=true" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "SECRET_METADATA_ONLY=true" in text
    assert "63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check" in text


def test_preexecution_safety_snapshot_script_exists_and_is_safe():
    script = ROOT / "scripts" / "k8s" / "statefulset_preexecution_safety_snapshot.sh"
    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert "get deployment postgres" in text
    assert "get pods -o wide" in text
    assert "get pvc postgres-data" in text
    assert "get service postgres" in text
    assert "get secret gwan-postgres-secret" in text
    assert "get configmap gwan-api-config" in text
    assert "get statefulset postgres" in text
    assert "SECRET_VALUES_EXPORTED=false" in text
    assert "SECRET_METADATA_ONLY=true" in text
    assert "PREEXECUTION_SNAPSHOT_CREATED=true" in text
    assert "63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check" in text

    forbidden = [
        "kubectl delete deployment postgres",
        "kubectl apply -f k8s/drafts",
        "kubectl apply -f k8s/drafts/postgres-statefulset-draft.yaml",
        "kubectl get secret gwan-postgres-secret -o yaml",
    ]

    for item in forbidden:
        assert item not in text


def test_codex_prompt_exists():
    prompt = ROOT / "codex" / "62_gwan_kubernetes_statefulset_preexecution_safety_snapshot_prompt.md"
    assert prompt.exists()

    text = prompt.read_text(encoding="utf-8")

    assert "Do not execute real migration" in text
    assert "Do not export secret values" in text
    assert "FINAL_DECISION=NO_GO" in text
    assert "REAL_MIGRATION_EXECUTED=false" in text
    assert "63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check" in text
