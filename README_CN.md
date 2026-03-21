# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

把文章链接发给 OpenClaw，并说：`存入知识库`。

这个 skill 会自动：
- 提取文章内容
- 检查是否重复
- 生成标签和摘要
- 输出可直接写入 Obsidian 的笔记

## 是什么

- OpenClaw 和 Codex 可用的 Obsidian 原生知识整理 skill
- 面向 vault 工作流的成品笔记生成器

## 用法

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```
