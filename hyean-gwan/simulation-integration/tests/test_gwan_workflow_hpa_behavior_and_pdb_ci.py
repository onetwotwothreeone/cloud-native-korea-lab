from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


def read_workflows() -> list[str]:
    paths = [
        REPO_ROOT / ".github/workflows/gwan-ci.yml",
        ROOT / ".github/workflows/gwan-ci.yml",
    ]
    return [path.read_text(encoding="utf-8") for path in paths if path.exists()]


def test_workflow_checks_step_34_and_35_docs() -> None:
    for text in read_workflows():
        assert "docs/34_GWAN_Kubernetes_HPA_Behavior_Policy.md" in text
        assert "docs/35_GWAN_Kubernetes_PodDisruptionBudget.md" in text


def test_workflow_runs_hpa_behavior_check() -> None:
    for text in read_workflows():
        assert "Kubernetes HPA behavior policy check" in text
        assert "scripts/k8s/hpa_behavior_check.sh" in text


def test_workflow_runs_pdb_check() -> None:
    for text in read_workflows():
        assert "Kubernetes PDB check" in text
        assert "scripts/k8s/pdb_check.sh" in text
