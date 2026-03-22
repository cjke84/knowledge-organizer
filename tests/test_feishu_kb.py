from scripts import ImportDraft


def test_build_feishu_payload_contains_required_fields():
    from scripts.feishu_kb import build_feishu_payload

    draft = ImportDraft.from_mapping(
        {
            "title": "Feishu Note",
            "source_type": "web",
            "source_url": "https://example.com/note",
            "content": "Body text",
            "tags": ["tag-a", "tag-b"],
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf"}],
        }
    )

    payload = build_feishu_payload(draft)

    assert payload["title"] == "Feishu Note"
    assert payload["source_type"] == "web"
    assert payload["source_url"] == "https://example.com/note"
    assert payload["source_id"] == draft.source_id
    assert payload["content_hash"] == draft.content_hash
    assert payload["images"] == [{"url": "https://img.example/a.png"}]
    assert payload["attachments"] == [{"url": "https://files.example/a.pdf"}]
    assert "Body text" in payload["content"]
    assert "tag-a" in payload["content"]


def test_import_to_feishu_returns_sync_record_from_transport():
    from scripts.feishu_kb import FeishuImportConfig, import_to_feishu

    draft = ImportDraft.from_mapping(
        {
            "title": "Feishu Note",
            "source_type": "markdown",
            "source_path": "/vault/note.md",
            "content": "Body text",
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf"}],
        }
    )

    seen = {}

    def fake_transport(payload, config):
        seen["payload"] = payload
        seen["config"] = config
        return {
            "data": {
                "document_id": "doc_123",
                "url": "https://example.com/doc/123",
            }
        }

    result = import_to_feishu(
        draft,
        FeishuImportConfig(import_endpoint="https://example.com/import"),
        transport=fake_transport,
    )

    assert seen["payload"]["title"] == "Feishu Note"
    assert seen["payload"]["images"] == [{"url": "https://img.example/a.png"}]
    assert seen["payload"]["attachments"] == [{"url": "https://files.example/a.pdf"}]
    assert result.remote_id == "doc_123"
    assert result.remote_url == "https://example.com/doc/123"
    assert result.sync_record.destination == "feishu"
    assert result.sync_record.remote_id == "doc_123"


def test_resolve_feishu_config_reads_environment(monkeypatch):
    from scripts.feishu_kb import resolve_feishu_config

    monkeypatch.setenv("FEISHU_IMPORT_ENDPOINT", "https://example.com/import")
    monkeypatch.setenv("FEISHU_APP_ID", "app_123")
    monkeypatch.setenv("FEISHU_APP_SECRET", "secret_456")
    monkeypatch.setenv("FEISHU_ACCESS_TOKEN", "token_789")
    monkeypatch.setenv("FEISHU_KB_ID", "kb_abc")
    monkeypatch.setenv("FEISHU_FOLDER_ID", "folder_def")

    config = resolve_feishu_config()

    assert config.import_endpoint == "https://example.com/import"
    assert config.app_id == "app_123"
    assert config.app_secret == "secret_456"
    assert config.access_token == "token_789"
    assert config.knowledge_base_id == "kb_abc"
    assert config.folder_id == "folder_def"
