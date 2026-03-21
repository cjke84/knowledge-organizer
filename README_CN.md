# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

面向 Obsidian vault 工作流的知识整理 skill。

## 是什么

- 面向 vault 的 Obsidian 成品笔记生成器
- 支持去重检测与相关文章建议
- 支持标签校验、摘要整理和元数据输出

## 做什么

- 生成 frontmatter、wikilinks、embeds 和 block IDs
- 通过 URL、hash、alias 和相似度做分层去重
- 推荐可直接链接的相关文章
- 在写入前校验标签是否符合知识库契约

## 用法

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```
