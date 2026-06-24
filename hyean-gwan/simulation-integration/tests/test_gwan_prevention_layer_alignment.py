from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]


def test_prevention_layer_alignment_doc_exists() -> None:
    path = ROOT / "docs/35_2_HYEAN_GWAN_Prevention_Layer_Alignment.md"
    text = path.read_text(encoding="utf-8")

    assert "35.2 HYEAN/GWAN Prevention Layer Alignment" in text
    assert "Prevention Layer" in text
    assert "prevention-oriented survival intelligence" in text
    assert "Early Signal Detection" in text
    assert "Balance Analysis" in text
    assert "Preventive Adjustment" in text
    assert "NetworkPolicy" in text


def test_prevention_fields_are_documented() -> None:
    path = ROOT / "docs/35_2_HYEAN_GWAN_Prevention_Layer_Alignment.md"
    text = path.read_text(encoding="utf-8")

    assert "risk_score" in text
    assert "trend_score" in text
    assert "imbalance_score" in text
    assert "early_warning_score" in text
    assert "recovery_capacity" in text
    assert "preventive_action_priority" in text


def test_prevention_alignment_is_added_to_readmes() -> None:
    paths = [
        REPO_ROOT / "README.md",
        ROOT / "README.md",
    ]

    for path in paths:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert "HYEAN/GWAN Prevention Layer Alignment" in text
            assert "NetworkPolicy" in text


def test_prevention_alignment_is_added_to_agents() -> None:
    path = REPO_ROOT / "AGENTS.md"
    text = path.read_text(encoding="utf-8")

    assert "HYEAN/GWAN Prevention Layer Alignment" in text
    assert "trend_score" in text
    assert "early_warning_score" in text
    assert "preventive_action_priority" in text


def test_codex_prompt_exists_for_prevention_alignment() -> None:
    path = ROOT / "codex/35_2_hyean_gwan_prevention_layer_alignment_prompt.md"
    text = path.read_text(encoding="utf-8")

    assert "Codex Prompt" in text
    assert "Prevention Layer" in text
    assert "36_GWAN_Kubernetes_NetworkPolicy_Baseline" in text
