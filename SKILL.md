---
name: obsidian-knowledge-organizer
description: OpenClaw 和 Codex 可用的 Obsidian 知识整理 skill。用于存入知识库、整理文章、打标签、归档、生成摘要和推荐相关文章。
---

# Knowledge Organizer

Obsidian 原生知识整理能力，面向 vault 工作流，将文章、链接和草稿整理成结构化、标签化且可直接落盘、Obsidian 原生可发布的 Markdown 笔记。

## 适用场景

- 存入知识库
- 整理文章
- 打标签
- 归档
- 生成摘要
- 推荐相关文章

## 能力概览

- 生成可直接写入 Obsidian 的笔记，包含 YAML frontmatter、wikilinks、embeds 和 block IDs
- 如果 draft 提供 `images`，自动下载图片到 `assets/` 并在正文里用相对路径引用，避免图片信息丢失
- 在写入前执行重复检测，覆盖 URL、hash、alias 和相似度层
- 去重命中是正常控制流结果，不应被当作工具错误；CLI 以结构化决策结果（decision）返回
- 推荐可直接链接的相关文章
- 按知识库标签契约校验标签（tags）

## 工作流

1. 获取内容：公众号链接用浏览器，其它网页链接用 web_fetch，用户直给内容直接处理
2. 去重检测：发现重复时提示用户，等待覆盖、合并或跳过
3. 渲染笔记：`scripts/obsidian_note.py` 生成内容和目标路径
4. 写入 vault：runtime 按 `destination_path` 直接落盘，不再二次处理 Markdown

## 合同

- 输入：结构化 draft、标题别名、来源元数据、摘要、要点、摘录、图片、相关文章、vault root
- 输出：`RenderedNote(content, destination_path)`
- frontmatter 必须包含：`title`、`aliases`、`tags`、`source_type`、`source_url`、`published`、`created`、`updated`、`importance`、`status`、`canonical_hash`
- 标签写入前必须满足：至少 1 个领域标签 + 1 个类型标签，总数 5-10 个
- vault root 必须是 non-empty absolute path
- vault root 优先来自 `OPENCLAW_KB_ROOT`
- 覆盖 frontmatter / wikilink / embed / block id 规则

## 兼容性

- OpenClaw 兼容
- Codex 兼容
- Obsidian vault 工作流

## 输出模板

```text
✅ 已存入知识库

📁 位置：知识库/xxx.md
🏷️ 标签：tag1, tag2, tag3
📋 摘要：一句话总结
⭐ 重要性：core
🔗 相关文章：xxx, yyy
```
