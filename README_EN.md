# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

An Obsidian vault workflow skill that turns articles, links, and drafts into structured notes you can write directly to disk.

## What it does

- extract the article
- check duplicates and return a structured decision
- generate tags, summary, and metadata
- download images into `assets/` and keep readable references
- render an Obsidian-ready note

## Capabilities

- OpenClaw- and Codex-compatible skill for Obsidian-native knowledge organization
- Obsidian-ready note generator for vault workflows
- validates tags against the repository tag contract
- recommends directly linkable related notes

## Use cases

- store in the knowledge base
- organize articles
- apply tags
- archive notes
- generate summaries
- suggest related notes

## Quick start

```bash
pytest -q
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```

## Related

- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)
