from pathlib import Path


def test_step_18_documentation_exists_and_explains_reverse_sync():
    text = Path("docs/18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation.md").read_text(encoding="utf-8")

    assert "18_GWAN_LongTermMemory_To_Onboard_Pull_And_Recommendation" in text
    assert "PostgreSQL long-term memory" in text
    assert "Onboard GWAN Core" in text
    assert "Manual Pull" in text
    assert "Proactive Recommendation" in text


def test_api_reference_lists_step_18_routes():
    text = Path("docs/API_REFERENCE.md").read_text(encoding="utf-8")

    assert "/gwan/sync/pull/manual" in text
    assert "/gwan/sync/recommend" in text
    assert "/gwan/sync/recommendation-settings" in text
    assert "manual_only" in text
    assert "critical_only" in text


def test_readme_and_runbook_include_step_18_flow():
    readme = Path("README.md").read_text(encoding="utf-8")
    runbook = Path("docs/LOCAL_RUNBOOK.md").read_text(encoding="utf-8")
    checklist = Path("docs/README_REVIEW_CHECKLIST.md").read_text(encoding="utf-8")

    assert "Long-term memory to onboard pull" in readme
    assert "/gwan/sync/pull/manual" in readme
    assert "/gwan/sync/recommend" in runbook
    assert "Step 18 checklist" in checklist
