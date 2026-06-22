from pathlib import Path


def test_sync_docs_exist_and_list_sync_routes() -> None:
    step_doc = Path("docs/17_GWAN_Local_Log_To_PostgreSQL_Sync.md").read_text(encoding="utf-8")
    api_ref = Path("docs/API_REFERENCE.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "17_GWAN_Local_Log_To_PostgreSQL_Sync" in step_doc
    assert "/gwan/memory/sync-status" in api_ref
    assert "/gwan/memory/sync-jsonl-to-db" in api_ref
    assert "JSONL local log to PostgreSQL sync" in readme
    assert "dry_run" in step_doc
