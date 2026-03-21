# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

OpenClaw / Codex skill for Obsidian-native knowledge organization.

## What it is

- Obsidian-ready note generator for vault workflows
- Duplicate detection and related-note suggestions
- Tag validation, summary shaping, and metadata output

## What it does

- Generates frontmatter, wikilinks, embeds, and block IDs
- Detects duplicates with URL, hash, alias, and similarity checks
- Recommends related notes with wikilink-friendly references
- Validates tags against the vault contract before writing

## Use

```bash
pytest -q
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```
