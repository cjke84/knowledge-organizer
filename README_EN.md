# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

Send an article link to OpenClaw and say: `store it in the knowledge base`.

This skill will:
- extract the article
- check duplicates
- generate tags and summary
- render an Obsidian-ready note

## What it is

- OpenClaw- and Codex-compatible skill for Obsidian-native knowledge organization
- Obsidian-ready note generator for vault workflows

## Use

```bash
pytest -q
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```
