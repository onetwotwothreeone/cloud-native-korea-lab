from pathlib import Path


def test_gwan_api_deployment_has_startup_readiness_and_liveness_probes():
    text = Path("k8s/base/gwan-api-deployment.yaml").read_text(encoding="utf-8")

    assert "startupProbe:" in text
    assert "readinessProbe:" in text
    assert "livenessProbe:" in text
    assert "path: /health" in text
    assert "failureThreshold: 30" in text
    assert "DATABASE_HOST" in text
    assert "DATABASE_PORT" in text
    assert "$(DATABASE_HOST):$(DATABASE_PORT)" in text


def test_kubernetes_observability_scripts_exist_and_are_useful():
    rollout = Path("scripts/k8s/rollout_check.sh")
    health = Path("scripts/k8s/health_readiness_check.sh")
    diagnostics = Path("scripts/k8s/diagnostics.sh")

    for path in [rollout, health, diagnostics]:
        assert path.exists(), path
        assert path.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")

    assert "rollout status deployment/postgres" in rollout.read_text(encoding="utf-8")
    assert "rollout status deployment/gwan-api" in rollout.read_text(encoding="utf-8")

    health_text = health.read_text(encoding="utf-8")
    assert "/health" in health_text
    assert "/gwan/memory/db-status" in health_text
    assert "curl -fsS" in health_text

    diagnostics_text = diagnostics.read_text(encoding="utf-8")
    assert "get events --sort-by=.lastTimestamp" in diagnostics_text
    assert "describe deployment/gwan-api" in diagnostics_text
    assert "describe pods" in diagnostics_text
    assert "logs deployment/gwan-api" in diagnostics_text
    assert "logs deployment/postgres" in diagnostics_text


def test_step_29_documentation_exists_and_explains_observability():
    text = Path("docs/29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline.md").read_text(
        encoding="utf-8"
    )

    assert "29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline" in text
    assert "startupProbe" in text
    assert "readinessProbe" in text
    assert "livenessProbe" in text
    assert "events" in text
    assert "logs" in text
    assert "diagnostics.sh" in text
