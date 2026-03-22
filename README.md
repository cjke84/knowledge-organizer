# Knowledge Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fknowledge--organizer-blue?logo=github)](https://github.com/cjke84/obsidian-knowledge-organizer)

一个面向知识库工作流的整理工具，用于把文章、链接和草稿整理成结构化、可直接落盘的笔记，也可以同步到飞书知识库和腾讯 IMA。

## 文档入口

- [English README](README_EN.md)
- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)
- [GitHub 仓库](https://github.com/cjke84/obsidian-knowledge-organizer)

## 能力概览

- 提取文章内容并生成 Obsidian 原生 Markdown 笔记
- 在写入前执行重复检测，支持结构化决策结果（decision）
- 生成标签、摘要、元数据和相关文章建议
- 自动下载图片到 `assets/` 并保留可读引用，支持 `src` / `data_src` / `data-original` / `data-lazy-src` / `srcset` / `url` / `image_url` / `original` 等常见字段
- 支持多来源输入，包括公众号文章、小红书链接和普通网页
- 按仓库标签契约校验标签（tags）
- 统一编排 `destination=obsidian|feishu|ima` 和 `mode=once|sync`
- Feishu 通过 OpenClaw 官方 `openclaw-lark` 插件接入
- IMA 通过 `import_doc` OpenAPI 直连

## 快速使用

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```

## 使用方法

1. 把文章链接或草稿交给 OpenClaw。
2. 让它执行去重、标签生成和摘要整理。
3. 选择目标：`obsidian`、`feishu` 或 `ima`。
4. 选择模式：`once` 一次导入，或 `sync` 增量同步。
5. 输出可直接写入 Obsidian 的 Markdown 笔记，或同步到飞书 / IMA。

## 适用场景

- 定期整理微信收藏的文章
- 建立个人知识库体系
- 团队知识沉淀
- 学术资料归档
- 需要把同一份内容同步到 Obsidian、飞书和 IMA

## `draft.images` 示例

```yaml
images:
  - path: /absolute/path/to/local.png
    alt: Local image
  - src: https://example.com/cover.png
    alt: Remote image
  - srcset: https://example.com/cover-1x.png 1x, https://example.com/cover-2x.png 2x
    alt: Responsive image
```

`path` 用于本地文件，`src` / `data_src` / `data-original` / `data-lazy-src` / `original` 等用于远程图片；`srcset` 会优先选数值更高的候选。

## Skill

OpenClaw-compatible skill. Codex-compatible skill.
