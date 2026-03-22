# Knowledge Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fknowledge--organizer-blue?logo=github)](https://github.com/cjke84/knowledge-organizer)

A knowledge-base workflow skill that turns article links, drafts, and notes into structured Markdown. You can write directly into Obsidian or sync to Feishu Knowledge Base and Tencent IMA.

## What it does

- process articles, links, and drafts into structured notes
- check duplicates and return a structured decision
- generate tags, summaries, and metadata
- download images into `assets/` and keep readable references, including common fields like `src`, `data_src`, `data-original`, `data-lazy-src`, `srcset`, `url`, `image_url`, and `original`
- write directly to Obsidian vault files
- orchestrate `destination=obsidian|feishu|ima` and `mode=once|sync`
- sync to Feishu through the official OpenClaw `openclaw-lark` plugin
- sync to Tencent IMA through the direct `import_doc` OpenAPI flow

## Capabilities

- OpenClaw- and Codex-compatible skill for knowledge organization
- Supports public-account posts, Xiaohongshu links, and ordinary web pages
- Works for Obsidian vault writes, Feishu sync, and IMA sync
- validates tags against the repository tag contract
- recommends directly linkable related notes
- supports one-shot import and incremental sync into Obsidian, Feishu, or IMA

## Use cases

- store in the knowledge base
- organize articles
- apply tags
- archive notes
- generate summaries
- suggest related notes

## How to use

1. Give OpenClaw an article link, a markdown draft, or a folder of drafts.
2. Choose a destination: `obsidian`, `feishu`, or `ima`.
3. Choose a mode: `once` for a single run or `sync` for incremental updates.
4. For Obsidian, provide a vault root. For Feishu and IMA, make sure the plugin or API credentials are ready.
5. The tool will dedupe first, then render the note or sync payload, then write or upload it.
6. You can call the sync orchestrator directly:

```bash
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination feishu --mode once --state .sync-state.json --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination ima --mode sync --state .sync-state.json --folder-path drafts/
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md --disable feishu,ima
```

## `draft.images` example

```yaml
images:
  - path: /absolute/path/to/local.png
    alt: Local image
  - src: https://example.com/cover.png
    alt: Remote image
  - srcset: https://example.com/cover-1x.png 1x, https://example.com/cover-2x.png 2x
    alt: Responsive image
```

`path` is for local files. `src` / `data_src` / `data-original` / `data-lazy-src` / `original` etc. are used for remote images; `srcset` prefers the highest-value candidate.

## Quick start

```bash
pytest -q
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```

## Related

- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)
- [GitHub Repository](https://github.com/cjke84/knowledge-organizer)
