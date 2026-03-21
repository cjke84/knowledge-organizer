# obsidian-knowledge-organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fobsidian--knowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

一个面向 Obsidian 知识库工作流的整理工具，用于把文章、链接和草稿整理成结构化、可直接落盘的笔记。

## 文档入口

- [English README](README_EN.md)
- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)

## 能力概览

- 提取文章内容并生成 Obsidian 原生 Markdown 笔记
- 在写入前执行重复检测，支持结构化决策结果（decision）
- 生成标签、摘要、元数据和相关文章建议
- 自动下载图片到 `assets/` 并保留可读引用
- 支持多来源输入，包括公众号文章和普通网页
- 按仓库标签契约校验标签（tags）

## 快速使用

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```

## 使用方法

1. 把文章链接或草稿交给 OpenClaw。
2. 让它执行去重、标签生成和摘要整理。
3. 输出可直接写入 Obsidian 的 Markdown 笔记。
4. 将笔记落入知识库。

## 适用场景

- 定期整理微信收藏的文章
- 建立个人知识库体系
- 团队知识沉淀
- 学术资料归档

## Skill

OpenClaw-compatible skill. Codex-compatible skill.
