# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

Obsidian-native knowledge organizer for vault workflows. / 面向 Obsidian 知识库工作流的原生整理工具。

OpenClaw-compatible skill. / 可直接在 OpenClaw 中使用的 skill。

## Capabilities / 核心能力

- Generate Obsidian-ready notes with frontmatter, wikilinks, embeds, and block IDs
- Detect duplicates with layered URL, hash, alias, and similarity checks
- Surface related notes with wikilink-friendly references
- Validate tags against the vault contract before writing

## Structure / 仓库结构

- `SKILL.md`: skill contract and workflow
- `scripts/`: runtime helpers
- `tests/`: regression tests
- `references/`: tag system and supporting docs

## Test

Run the full suite:

```bash
pytest -q
```

## Usage / 使用示例

Check whether a draft duplicates an existing note:

```bash
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
```

Find related notes for a new article:

```bash
python scripts/find_related.py alpha beta --title "New Title" --json
```

检测草稿是否与现有笔记重复：

```bash
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
```

为新文章查找相关文章：

```bash
python scripts/find_related.py alpha beta --title "新标题" --json
```
