from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable
from urllib import error, request

from .import_models import ImportDraft
from .sync_state import SyncStateRecord


@dataclass(frozen=True)
class FeishuImportConfig:
    import_endpoint: str
    app_id: str | None = None
    app_secret: str | None = None
    access_token: str | None = None
    knowledge_base_id: str | None = None
    folder_id: str | None = None
    timeout: float = 30.0


@dataclass(frozen=True)
class FeishuImportResult:
    payload: dict[str, Any]
    response: dict[str, Any]
    remote_id: str | None
    remote_url: str | None
    sync_record: SyncStateRecord


def resolve_feishu_config(
    *,
    import_endpoint: str | None = None,
    timeout: float = 30.0,
) -> FeishuImportConfig:
    return FeishuImportConfig(
        import_endpoint=import_endpoint
        or os.environ.get("FEISHU_IMPORT_ENDPOINT", "").strip(),
        app_id=os.environ.get("FEISHU_APP_ID", "").strip() or None,
        app_secret=os.environ.get("FEISHU_APP_SECRET", "").strip() or None,
        access_token=os.environ.get("FEISHU_ACCESS_TOKEN", "").strip() or None,
        knowledge_base_id=os.environ.get("FEISHU_KB_ID", "").strip() or None,
        folder_id=os.environ.get("FEISHU_FOLDER_ID", "").strip() or None,
        timeout=timeout,
    )


def _markdown_body(draft: ImportDraft) -> str:
    lines = [
        f"# {draft.title}",
        "",
        f"- Source type: {draft.source_type}",
    ]
    if draft.source_url:
        lines.append(f"- Source URL: {draft.source_url}")
    lines.append(f"- Source ID: {draft.source_id}")
    lines.append(f"- Content hash: {draft.content_hash}")
    if draft.tags:
        lines.append(f"- Tags: {', '.join(draft.tags)}")
    lines.extend(["", draft.content.strip(), ""])
    return "\n".join(line for line in lines if line is not None).strip() + "\n"


def build_feishu_payload(
    draft: ImportDraft,
    *,
    knowledge_base_id: str | None = None,
    folder_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": draft.title,
        "source_type": draft.source_type,
        "source_url": draft.source_url,
        "source_id": draft.source_id,
        "content_hash": draft.content_hash,
        "tags": list(draft.tags),
        "content": _markdown_body(draft),
    }
    if knowledge_base_id:
        payload["knowledge_base_id"] = knowledge_base_id
    if folder_id:
        payload["folder_id"] = folder_id
    return payload


def _default_transport(payload: dict[str, Any], config: FeishuImportConfig) -> dict[str, Any]:
    if not config.import_endpoint:
        raise ValueError("Feishu import_endpoint is required")

    headers = {"Content-Type": "application/json"}
    if config.access_token:
        headers["Authorization"] = f"Bearer {config.access_token}"

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(config.import_endpoint, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=config.timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        raise RuntimeError(f"Feishu import failed with HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Feishu import failed: {exc.reason}") from exc

    if not raw.strip():
        return {}
    return json.loads(raw)


def _extract_remote_fields(response: dict[str, Any], config: FeishuImportConfig) -> tuple[str | None, str | None]:
    data = response.get("data") if isinstance(response, dict) else None
    if not isinstance(data, dict):
        data = response if isinstance(response, dict) else {}

    remote_id = (
        data.get("document_id")
        or data.get("doc_id")
        or data.get("id")
        or data.get("file_id")
    )
    remote_url = data.get("url") or data.get("document_url") or config.import_endpoint
    return (str(remote_id) if remote_id is not None else None, str(remote_url) if remote_url else None)


def import_to_feishu(
    draft: ImportDraft,
    config: FeishuImportConfig,
    *,
    transport: Callable[[dict[str, Any], FeishuImportConfig], dict[str, Any]] | None = None,
) -> FeishuImportResult:
    payload = build_feishu_payload(
        draft,
        knowledge_base_id=config.knowledge_base_id,
        folder_id=config.folder_id,
    )
    response = (transport or _default_transport)(payload, config)
    remote_id, remote_url = _extract_remote_fields(response, config)
    now = datetime.now(timezone.utc).isoformat()
    sync_record = SyncStateRecord(
        source_id=draft.source_id,
        content_hash=draft.content_hash,
        destination="feishu",
        remote_id=remote_id,
        remote_url=remote_url,
        last_synced_at=now,
        status="ok",
        error_message=None,
    )
    return FeishuImportResult(
        payload=payload,
        response=response,
        remote_id=remote_id,
        remote_url=remote_url,
        sync_record=sync_record,
    )
