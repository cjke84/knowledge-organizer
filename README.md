# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

OpenClaw / Codex skill for Obsidian-native knowledge organization.

## When to use

- Store an article into an Obsidian vault
- Deduplicate a draft before saving
- Generate tags, summary, and related-note suggestions

## What it does

- Generates Obsidian-ready notes with frontmatter, wikilinks, embeds, and block IDs
- Detects duplicates with URL, hash, alias, and similarity checks
- Recommends related notes with wikilink-friendly references
- Validates tags against the vault contract before writing

## Compatibility

- OpenClaw-compatible skill
- Codex-compatible skill
- Obsidian vault workflows

## Structure

- `SKILL.md`: skill contract and workflow
- `scripts/`: runtime helpers
- `tests/`: regression tests
- `references/`: tag system and supporting docs

## Test

```bash
pytest -q
```

## Usage

```bash
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```

```bash
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```
