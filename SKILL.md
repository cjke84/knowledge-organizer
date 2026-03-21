---
name: obsidian-knowledge-organizer
description: OpenClaw 和 Codex 可用的 Obsidian 知识整理 skill。用于存入知识库、整理文章、打标签、归档、生成摘要和推荐相关文章。
---

# Knowledge Organizer

Obsidian 原生知识整理 skill，面向 vault 工作流，将文章整理成结构化、标签化且 **Obsidian 原生可发布** 的 Markdown 笔记。

## When to use

- 存入知识库
- 整理文章
- 打标签
- 归档
- 生成摘要
- 推荐相关文章

## What it does

- 生成 Obsidian-ready 笔记，包含 YAML frontmatter、wikilinks、embeds 和 block IDs
- 在写入前执行重复检测，覆盖 URL、hash、alias 和相似度层
- 推荐可直接链接的相关文章
- 按知识库标签契约校验标签

## Workflow

1. 获取内容：公众号链接用浏览器，其它网页链接用 web_fetch，用户直给内容直接处理
2. 去重检测：发现重复时提示用户，等待覆盖、合并或跳过
3. 渲染笔记：`scripts/obsidian_note.py` 生成内容和目标路径
4. 写入 vault：runtime 按 `destination_path` 直接落盘，不再二次处理 Markdown

## Contract

- helper 输入：结构化 draft、标题别名、来源元数据、摘要、要点、摘录、相关文章、vault root
- helper 输出：`RenderedNote(content, destination_path)`
- frontmatter 必须包含：`title`、`aliases`、`tags`、`source_type`、`source_url`、`published`、`created`、`updated`、`importance`、`status`、`canonical_hash`
- tags 写入前必须满足：至少 1 个领域标签 + 1 个类型标签，总数 5-10 个
- vault root 必须是 non-empty absolute path
- vault root 优先来自 `OPENCLAW_KB_ROOT`
- contract covers frontmatter / wikilink / embed / block id rules

## Compatibility

- OpenClaw-compatible skill
- Codex-compatible skill
- Obsidian vault workflows

## Output

```text
✅ 已存入知识库

📁 位置：知识库/xxx.md
🏷️ 标签：tag1, tag2, tag3
📋 摘要：一句话总结
⭐ 重要性：core
🔗 相关文章：xxx, yyy
```
