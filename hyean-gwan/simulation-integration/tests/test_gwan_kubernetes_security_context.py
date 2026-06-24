from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gwan_api_security_context_exists() -> None:
    path = ROOT / "k8s/base/gwan-api-deployment.yaml"
    text = path.read_text(encoding="utf-8")

    assert "securityContext:" in text
    assert "runAsNonRoot: true" in text
    assert "runAsUser: 1000" in text
    assert "runAsGroup: 1000" in text
    assert "fsGroup: 1000" in text
    assert "seccompProfile:" in text
    assert "type: RuntimeDefault" in text
    assert "allowPrivilegeEscalation: false" in text
    assert "privileged: false" in text
    assert "readOnlyRootFilesystem: true" in text
    assert "capabilities:" in text
    assert "- ALL" in text
    assert "gwan-api-tmp" in text
    assert "mountPath: /tmp" in text
    assert "PYTHONDONTWRITEBYTECODE" in text


def test_postgres_security_context_exists() -> None:
    path = ROOT / "k8s/base/postgres-deployment.yaml"
    text = path.read_text(encoding="utf-8")

    assert "securityContext:" in text
    assert "fsGroup: 999" in text
    assert "seccompProfile:" in text
    assert "type: RuntimeDefault" in text
    assert "allowPrivilegeEscalation: false" in text
    assert "privileged: false" in text
    assert "readOnlyRootFilesystem: false" in text
    assert "capabilities:" in text
    assert "- ALL" in text


def test_security_context_check_script_exists() -> None:
    path = ROOT / "scripts/k8s/security_context_check.sh"
    text = path.read_text(encoding="utf-8")

    assert "SecurityContext" in text
    assert "RuntimeDefault" in text
    assert "allowPrivilegeEscalation" in text
    assert "readOnlyRootFilesystem" in text
    assert "capabilities.drop" in text


def test_security_context_documentation_exists() -> None:
    path = ROOT / "docs/38_GWAN_Kubernetes_SecurityContext_Baseline.md"
    text = path.read_text(encoding="utf-8")

    assert "38_GWAN_Kubernetes_SecurityContext_Baseline" in text
    assert "preventive runtime control" in text
    assert "runAsNonRoot" in text
    assert "RuntimeDefault" in text
    assert "readOnlyRootFilesystem" in text


def test_security_context_codex_prompt_exists() -> None:
    path = ROOT / "codex/38_gwan_kubernetes_securitycontext_baseline_prompt.md"
    text = path.read_text(encoding="utf-8")

    assert "GWAN Kubernetes SecurityContext Baseline" in text
    assert "preventive runtime control" in text
    assert "runAsNonRoot" in text
    assert "RuntimeDefault" in text
