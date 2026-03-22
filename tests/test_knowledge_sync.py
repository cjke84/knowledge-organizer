from __future__ import annotations

from pathlib import Path

import pytest

from scripts import ImportDraft, SyncStateRecord, SyncStateStore


def _draft(*, title: str = "T", url: str = "https://example.com/x", content: str = "Body") -> ImportDraft:
    return ImportDraft.from_mapping(
        {
            "title": title,
            "source_type": "web",
            "source_url": url,
            "content": content,
            "tags": ["a"],
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf", "name": "a.pdf"}],
        }
    )


def test_run_sync_routes_to_ima_destination(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    draft = _draft()
    seen = {"calls": 0}

    def fake_ima_transport(payload, config):
        seen["calls"] += 1
        return {"doc_id": "doc_123"}

    result = run_sync(
        destination="ima",
        mode="once",
        drafts=[draft],
        state_path=tmp_path / "state.json",
        ima_config_overrides={"client_id": "c", "api_key": "k"},
        ima_transport=fake_ima_transport,
    )

    assert result.destination == "ima"
    assert result.mode == "once"
    assert result.processed == 1
    assert seen["calls"] == 1


def test_incremental_sync_skips_unchanged_items(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    draft = _draft()
    store = SyncStateStore(tmp_path / "state.json")
    store.write(
        SyncStateRecord(
            source_id=draft.source_id,
            content_hash=draft.content_hash,
            destination="ima",
            remote_id="doc_123",
            remote_url=None,
            last_synced_at="2026-03-22T00:00:00+00:00",
            status="ok",
            error_message=None,
        )
    )

    seen = {"calls": 0}

    def fake_ima_transport(payload, config):
        seen["calls"] += 1
        return {"doc_id": "doc_999"}

    result = run_sync(
        destination="ima",
        mode="sync",
        drafts=[draft],
        state_path=tmp_path / "state.json",
        ima_config_overrides={"client_id": "c", "api_key": "k"},
        ima_transport=fake_ima_transport,
    )

    assert result.skipped == 1
    assert result.processed == 0
    assert seen["calls"] == 0


def test_dry_run_does_not_write_obsidian_files(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    vault_root = tmp_path / "vault"
    vault_root.mkdir()

    draft = _draft(title="Obsidian Note")

    result = run_sync(
        destination="obsidian",
        mode="once",
        drafts=[draft],
        vault_root=vault_root,
        state_path=tmp_path / "state.json",
        dry_run=True,
    )

    assert result.processed == 1
    assert list(vault_root.glob("*.md")) == []
    assert list((vault_root / "assets").rglob("*")) == []


def test_once_mode_dedupes_duplicate_sources(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    draft = _draft(title="Duplicate Note")

    result = run_sync(
        destination="ima",
        mode="once",
        drafts=[draft, draft],
        state_path=tmp_path / "state.json",
        ima_config_overrides={"client_id": "c", "api_key": "k"},
        ima_transport=lambda payload, config: {"doc_id": "doc_123"},
    )

    assert result.processed == 1
    assert result.skipped == 1


def test_feishu_dispatch_can_be_faked_via_transport(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    draft = _draft(title="Feishu Note")
    seen = {}

    def fake_feishu_transport(payload, config):
        seen["payload"] = payload
        return {"doc_id": "doc_123", "doc_url": "https://www.feishu.cn/docx/doc_123"}

    result = run_sync(
        destination="feishu",
        mode="once",
        drafts=[draft],
        state_path=tmp_path / "state.json",
        feishu_config_overrides={"wiki_space": "my_library"},
        feishu_transport=fake_feishu_transport,
    )

    assert result.processed == 1
    assert seen["payload"]["title"] == "Feishu Note"
    assert seen["payload"]["wiki_space"] == "my_library"
    assert "<image url=" in seen["payload"]["markdown"]


def test_unknown_destination_raises(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    with pytest.raises(ValueError):
        run_sync(
            destination="unknown",
            mode="once",
            drafts=[_draft()],
            state_path=tmp_path / "state.json",
        )


def test_disabled_destination_raises(tmp_path: Path) -> None:
    from scripts.knowledge_sync import run_sync

    with pytest.raises(ValueError, match="disabled"):
        run_sync(
            destination="ima",
            mode="once",
            drafts=[_draft()],
            state_path=tmp_path / "state.json",
            ima_config_overrides={"client_id": "c", "api_key": "k"},
            ima_transport=lambda payload, config: {"doc_id": "doc_123"},
            disabled_destinations=["ima"],
        )


def test_main_supports_disable_switch(tmp_path: Path) -> None:
    from scripts.knowledge_sync import main

    exit_code = main(
        [
            "--destination",
            "feishu",
            "--mode",
            "once",
            "--state",
            str(tmp_path / "state.json"),
            "--disable",
            "feishu,ima",
        ]
    )

    assert exit_code == 1
