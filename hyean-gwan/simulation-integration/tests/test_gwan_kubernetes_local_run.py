from pathlib import Path

SCRIPT_DIR = Path("scripts/k8s")
DOC = Path("docs/24_GWAN_Kubernetes_Local_Run.md")


def test_step_24_scripts_exist() -> None:
    expected = [
        SCRIPT_DIR / "apply_local.sh",
        SCRIPT_DIR / "port_forward_health_check.sh",
        SCRIPT_DIR / "status.sh",
        SCRIPT_DIR / "cleanup_local.sh",
    ]

    for path in expected:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")


def test_apply_local_script_uses_local_overlay_and_waits_for_both_deployments() -> None:
    text = (SCRIPT_DIR / "apply_local.sh").read_text(encoding="utf-8")

    assert 'KUSTOMIZE_PATH="k8s/overlays/local"' in text
    assert "docker build -t" in text
    assert "kubectl apply -k \"$KUSTOMIZE_PATH\"" in text
    assert "rollout status deployment/postgres" in text
    assert "rollout status deployment/gwan-api" in text
    assert "kubectl -n \"$NAMESPACE\" get pods" in text
    assert "kubectl -n \"$NAMESPACE\" get svc" in text


def test_port_forward_script_checks_health_and_db_status() -> None:
    text = (SCRIPT_DIR / "port_forward_health_check.sh").read_text(encoding="utf-8")

    assert "kubectl -n \"$NAMESPACE\" port-forward" in text
    assert "svc/gwan-api" in text
    assert "curl -f \"http://127.0.0.1:${LOCAL_PORT}/health\"" in text
    assert "curl -f \"http://127.0.0.1:${LOCAL_PORT}/gwan/memory/db-status\"" in text
    assert "trap cleanup EXIT" in text


def test_cleanup_script_deletes_local_overlay() -> None:
    text = (SCRIPT_DIR / "cleanup_local.sh").read_text(encoding="utf-8")

    assert 'KUSTOMIZE_PATH="k8s/overlays/local"' in text
    assert "kubectl delete -k \"$KUSTOMIZE_PATH\" --ignore-not-found=true" in text
    assert "hyean-gwan" in text


def test_step_24_documentation_explains_manual_and_scripted_local_overlay_run() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "24_GWAN_Kubernetes_Local_Run" in text
    assert "kubectl kustomize k8s/overlays/local" in text
    assert "kubectl apply -k k8s/overlays/local" in text
    assert "kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000" in text
    assert "scripts/k8s/apply_local.sh" in text
    assert "scripts/k8s/cleanup_local.sh" in text
    assert "/gwan/memory/db-status" in text
