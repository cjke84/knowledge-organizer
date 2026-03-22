# Feishu and IMA Knowledge Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add first-class import and incremental sync support for Feishu Knowledge Base and Tencent IMA while preserving the current Obsidian pipeline.

**Architecture:** Build a shared import model plus sync-state layer, then route normalized drafts into destination adapters for Obsidian, Feishu, and IMA. Keep source parsing, normalization, deduplication, and platform-specific rendering separate so the target integrations stay isolated and testable.

**Tech Stack:** Python 3.14, `pytest`, `PyYAML`, standard library `dataclasses`/`pathlib`/`json`/`urllib`, and the existing `scripts/` module layout.

---

### Task 1: Define the shared import model and sync-state storage

**Files:**
- Create: `scripts/import_models.py`
- Create: `scripts/sync_state.py`
- Modify: `scripts/__init__.py`
- Test: `tests/test_import_models.py`
- Test: `tests/test_sync_state.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_import_draft_normalizes_required_fields():
    draft = ImportDraft.from_mapping({...})
    assert draft.title == "..."
    assert draft.source_type == "..."
    assert draft.content_hash

def test_sync_state_round_trip(tmp_path):
    store = SyncStateStore(tmp_path / "state.json")
    store.write(...)
    assert store.read(...) == ...
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_import_models.py tests/test_sync_state.py -q
```
Expected: FAIL because the new model and state modules do not exist yet.

- [ ] **Step 3: Implement the minimal model and state layer**

Implement:
- `ImportDraft` as a small dataclass or frozen mapping wrapper
- stable `content_hash` / `source_id` helpers
- `SyncStateRecord` plus a JSON-backed `SyncStateStore`
- a simple `scripts/__init__.py` export path for shared helpers

- [ ] **Step 4: Run the tests and verify they pass**

Run:
```bash
pytest tests/test_import_models.py tests/test_sync_state.py -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/import_models.py scripts/sync_state.py scripts/__init__.py tests/test_import_models.py tests/test_sync_state.py
git commit -m "feat: add shared import model and sync state"
```

### Task 2: Add source normalization for links, Markdown, and folder scans

**Files:**
- Create: `scripts/import_sources.py`
- Create: `scripts/import_normalizer.py`
- Modify: `scripts/check_runtime.py`
- Test: `tests/test_import_sources.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_link_source_normalizes_wechat_and_xiaohongshu_inputs():
    draft = load_source(...)
    assert draft.source_type in {"wechat_article", "xiaohongshu_note", "web"}

def test_markdown_and_folder_sources_share_the_same_output_shape(tmp_path):
    assert normalize_source(md_path) == normalize_source(folder_path)
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_import_sources.py -q
```
Expected: FAIL because the source normalization module is not implemented yet.

- [ ] **Step 3: Implement the minimal source readers and normalizer**

Implement:
- link-based source detection
- Markdown file loading
- folder scan for `*.md`
- normalized output into `ImportDraft`
- reuse the existing WeChat / Xiaohongshu guidance from `references/wechat-import.md` and `references/xiaohongshu-import.md`

- [ ] **Step 4: Run the tests and verify they pass**

Run:
```bash
pytest tests/test_import_sources.py -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/import_sources.py scripts/import_normalizer.py scripts/check_runtime.py tests/test_import_sources.py
git commit -m "feat: normalize knowledge sync inputs"
```

### Task 3: Implement the Feishu knowledge adapter

**Files:**
- Create: `scripts/feishu_kb.py`
- Create: `references/feishu-import.md`
- Test: `tests/test_feishu_kb.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_feishu_payload_contains_required_fields():
    payload = build_feishu_payload(draft)
    assert payload["title"] == draft.title
    assert payload["content"]

def test_feishu_import_updates_sync_state(tmp_path):
    ...
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_feishu_kb.py -q
```
Expected: FAIL because the adapter does not exist yet.

- [ ] **Step 3: Implement the minimal Feishu adapter**

Implement:
- a Feishu-specific payload builder from `ImportDraft`
- credential resolution through environment/config
- a thin transport function for create/import calls
- remote-id and remote-url capture for sync state

Keep the transport layer isolated so the adapter can be swapped between API-style and official-plugin-style import paths if the platform requires it.

- [ ] **Step 4: Run the tests and verify they pass**

Run:
```bash
pytest tests/test_feishu_kb.py -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/feishu_kb.py references/feishu-import.md tests/test_feishu_kb.py
git commit -m "feat: add Feishu knowledge adapter"
```

### Task 4: Implement the Tencent IMA knowledge adapter

**Files:**
- Create: `scripts/ima_kb.py`
- Create: `references/ima-import.md`
- Test: `tests/test_ima_kb.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_ima_adapter_builds_a_valid_import_plan():
    plan = build_ima_import_plan(draft)
    assert plan.title == draft.title
    assert plan.payload

def test_ima_adapter_preserves_fallback_path_when_api_is_unclear():
    ...
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_ima_kb.py -q
```
Expected: FAIL because the adapter does not exist yet.

- [ ] **Step 3: Implement the minimal IMA adapter**

Implement:
- a normalized IMA import plan from `ImportDraft`
- a transport boundary for the official path
- a fallback path that emits a portable import package when the API shape is not stable enough to call directly
- remote-id / sync-state capture when available

Do not hard-code undocumented endpoints. Keep the public API surface small so the adapter can be adjusted after validation against the official plugin flow.

- [ ] **Step 4: Run the tests and verify they pass**

Run:
```bash
pytest tests/test_ima_kb.py -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/ima_kb.py references/ima-import.md tests/test_ima_kb.py
git commit -m "feat: add IMA knowledge adapter"
```

### Task 5: Add the orchestration CLI for one-shot import and incremental sync

**Files:**
- Create: `scripts/knowledge_sync.py`
- Modify: `scripts/__init__.py`
- Test: `tests/test_knowledge_sync.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_sync_cli_routes_to_selected_destination():
    result = run_sync(...)
    assert result.destination == "feishu"

def test_incremental_sync_skips_unchanged_items(tmp_path):
    ...
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_knowledge_sync.py -q
```
Expected: FAIL because the orchestration module does not exist yet.

- [ ] **Step 3: Implement the minimal sync orchestrator**

Implement:
- a CLI or callable entrypoint for `destination=obsidian|feishu|ima`
- `mode=once|sync`
- source loading
- dedupe check
- adapter dispatch
- sync-state read/write
- dry-run support if the payload is already easy to preview

- [ ] **Step 4: Run the tests and verify they pass**

Run:
```bash
pytest tests/test_knowledge_sync.py -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/knowledge_sync.py scripts/__init__.py tests/test_knowledge_sync.py
git commit -m "feat: add knowledge sync orchestration"
```

### Task 6: Update contracts, docs, and regression coverage

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `README_CN.md`
- Modify: `README_EN.md`
- Modify: `INSTALL.md`
- Modify: `tests/test_skill_contract.py`

- [ ] **Step 1: Write the failing contract/doc tests**

```python
def test_skill_contract_mentions_feishu_and_ima_support():
    assert "Feishu" in skill_text
    assert "IMA" in skill_text
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:
```bash
pytest tests/test_skill_contract.py -q
```
Expected: FAIL until the new integration language is added.

- [ ] **Step 3: Update the docs and contract text**

Update:
- the skill description to mention Feishu and IMA import support
- the README files to explain the new destinations and sync modes
- the install guide if any new env vars or setup steps are introduced
- the skill contract test so it checks the new platform coverage

- [ ] **Step 4: Run the full test suite and verify it passes**

Run:
```bash
pytest -q
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add SKILL.md README.md README_CN.md README_EN.md INSTALL.md tests/test_skill_contract.py
git commit -m "docs: document feishu and ima knowledge sync"
```

## Notes for implementation

- Keep the existing Obsidian behavior intact; this work is additive.
- Prefer small modules over one large multi-platform file.
- Keep Feishu and IMA adapters isolated so future platform changes stay local.
- If the IMA public API remains ambiguous after validation, preserve the fallback import-package path rather than guessing unsupported endpoints.
