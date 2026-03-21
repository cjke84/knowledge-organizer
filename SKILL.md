---
name: knowledge-organizer
description: OpenClaw 可用的知识库文章整理与归档助手。自动为文章生成标签、摘要、元数据，检测重复内容，推荐关联文章。触发词：存入知识库、整理文章、打标签、归档、知识库、保存文章、整理公众号。
---

# Knowledge Organizer

知识库文章自动化整理工具，将任意来源的文章整理成结构化、标签化且 **Obsidian 原生可发布** 的 Markdown 笔记（无需额外插件、无需二次处理）。

## 触发场景

- 用户发送文章链接，要求存入知识库
- 用户要求整理、归档文章
- 用户要求为文章打标签、生成摘要

## 工作流程

### 1. 获取内容

- 微信公众号链接 → 使用浏览器打开并提取内容
- 其他网页链接 → 使用 web_fetch 提取
- 用户直接提供内容 → 直接处理

### 2. 去重检测

在写入前，搜索知识库已有文章：
- 检查标题相似度
- 检查核心内容是否重复
- 如果发现重复，提示用户并询问是否覆盖/合并/跳过

### 3. Obsidian 原生笔记整形（Contract）

本技能将“整形渲染”和“文件写入”明确分离：

- `scripts/obsidian_note.py` 负责：根据结构化 draft 生成 Obsidian Markdown（包含 YAML frontmatter + 正文结构）并 **解析出目标写入路径**
- Skill runtime 负责：按 helper 返回的 `destination_path` **执行实际写入**（不再对内容做后处理）
- 写入前必须确认 frontmatter、wikilink、embed、tags 都符合本技能约束；不符合则先修正 draft，再写入 vault
- helper 返回的 vault root 必须是 non-empty absolute path

Helper 的运行时合同：

- input: 结构化文章 draft（title、aliases、source metadata、summary、bullets、excerpts、related links/notes、以及目标 vault root）
- output: `RenderedNote(content, destination_path)`，其中 `content` 可直接放入 vault 发布，`destination_path` 为最终落盘路径

frontmatter 必须包含（允许额外字段，但以下字段必须存在）：

```yaml
---
title: 标题
aliases:
  - 别名1
  - 别名2
tags:
  - 自动生成标签（5-10个）
source_type: web | wechat | paper | book | ...
source_url: 原文链接
published: 发布日期（YYYY-MM-DD，未知可为空字符串）
created: 归档日期（YYYY-MM-DD）
updated: 更新日期（YYYY-MM-DD）
importance: core | reference | to-read
status: draft | processed | archived | ...
canonical_hash: 用于去重/溯源的稳定哈希（sha256 hex）
---
```

### 4. 标签生成规则

根据文章内容自动匹配标签，参考 [references/tag-system.md](references/tag-system.md)。

标签在写入前必须做校验：
- 至少 1 个领域标签 + 1 个类型标签
- 总数 5-10 个
- 优先复用已有标签，避免同义词扩散
- 不符合标签体系的候选标签必须丢弃或改写，不允许直接落盘

标签分类：
- **领域标签**：AI-Agent、投资、编程、产品、运营、设计...
- **类型标签**：技术文档、教程、案例、观点、工具、方法论...
- **技术标签**：Python、React、向量数据库、LLM...
- **来源标签**：公众号、知乎、博客、论文、书籍...

### 5. 摘要生成

生成两级摘要：
- **一句话总结**：15-30字，放在正文开头
- **核心要点**：3-5条 bullet points

### 6. 重要程度判断

根据内容质量、实用性、时效性判断：
- `core` — 核心资料，长期有价值的知识
- `reference` — 参考资料，偶尔查阅
- `to-read` — 待读，尚未深入理解

### 7. 关联推荐

搜索知识库已有文章，推荐相关内容：
- 相同标签的文章
- 相似主题的文章
- 引用/被引用关系

### 8. 分类建议

根据内容推荐存放位置：
- 已有子目录 → 推荐最匹配的
- 无匹配目录 → 建议创建新目录

### 9. 写入文件

保存到知识库目录：`~/Documents/Obsidian/KKKK/知识库/`

文件命名规范：
- 使用原标题生成文件名，清理特殊字符并压缩空白
- helper 只负责生成目标路径；runtime 负责冲突处理、重命名或追加日期

## 输出格式

完成整理后，汇报：

```
✅ 已存入知识库

📁 位置：知识库/xxx.md
🏷️ 标签：tag1, tag2, tag3
📋 摘要：一句话总结
⭐ 重要性：core
🔗 相关文章：xxx, yyy
```

## 配置

知识库根目录默认来源优先级：
1. `OPENCLAW_KB_ROOT`
2. skill/runtime 显式配置
3. `~/Documents/Obsidian/KKKK/知识库/`

- helper 期望 runtime 传入非空且绝对路径的 vault root
- runtime 负责把 helper 生成的内容直接写入 vault，不再做二次 Markdown 处理

## Obsidian 语法要求

- 内部引用必须使用 Obsidian wikilink：`[[Note Title]]`
- 仅在明确要求嵌入时才使用 embed：`![[Note Title]]`
- 正文必须直接可发布到 vault：不依赖后处理、不要求额外插件
- 所有输出都应兼容 Obsidian 的 frontmatter / wikilink / embed / block id 语法
