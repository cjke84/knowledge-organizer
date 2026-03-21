# Direct Agent Prompt

## Chinese

把下面这段直接发给 OpenClaw 或 Codex：

```text
请使用 obsidian-knowledge-organizer skill 处理这篇文章/这个链接，目标是“存入知识库”。

要求：
- 提取文章内容
- 检查是否重复，并返回结构化 decision
- 生成标签、摘要和元数据
- 保留输入中的图片引用
- 输出可直接写入 Obsidian 的笔记

如果发现重复，请不要直接覆盖，先说明 decision 和处理建议。
```

## English

Copy this to OpenClaw or Codex:

```text
Use the obsidian-knowledge-organizer skill to process this article/link. The goal is to store it in the knowledge base.

Requirements:
- extract the article
- check duplicates and return a structured decision
- generate tags, summary, and metadata
- preserve provided images in the rendered note
- render an Obsidian-ready note

If a duplicate is found, do not overwrite automatically. Return the decision and the recommended action.
```
