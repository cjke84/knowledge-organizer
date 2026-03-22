# Knowledge Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fknowledge--organizer-blue?logo=github)](https://github.com/cjke84/knowledge-organizer)

一个面向知识库工作流的整理工具，用于把文章、链接和草稿整理成结构化笔记。你可以直接写入 Obsidian，也可以同步到飞书知识库和腾讯 IMA。

## 它会做什么

- 处理文章、链接和草稿，输出可直接落盘的结构化笔记
- 检查是否重复并返回结构化决策结果（decision）
- 生成标签、摘要和元数据
- 自动下载图片到 `assets/` 并保留可读引用，支持 `src` / `data_src` / `data-original` / `data-lazy-src` / `srcset` / `url` / `image_url` / `original` 等常见字段
- 支持公众号文章、小红书链接和普通网页
- 统一编排 `destination=obsidian|feishu|ima` 和 `mode=once|sync`
- 直接写入 Obsidian 本地 vault
- 飞书通过 OpenClaw 官方 `openclaw-lark` 插件接入
- IMA 通过 `import_doc` OpenAPI 直连

## 能力概览

- OpenClaw 和 Codex 可用的知识库整理工具
- 支持 Obsidian 写入、飞书同步和 IMA 同步
- 面向 vault 工作流的成品笔记生成器
- 按标签契约校验标签（tags）
- 推荐可直接链接的相关文章

## 使用方式

1. 把文章链接、markdown 草稿或草稿文件夹交给 OpenClaw。
2. 选择目标：`obsidian`、`feishu` 或 `ima`。
3. 选择模式：`once` 一次导入，或 `sync` 增量同步。
4. Obsidian 需要提供 vault 路径；飞书和 IMA 需要准备好对应插件或 API 凭据。
5. 工具会先去重，再生成摘要、标签和元数据，最后写入本地笔记或同步到飞书 / IMA。
6. 你也可以直接调用同步编排器：

```bash
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination feishu --mode once --state .sync-state.json --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination ima --mode sync --state .sync-state.json --folder-path drafts/
```

## 适用场景

- 存入知识库
- 整理文章
- 打标签
- 归档
- 生成摘要
- 推荐相关文章
- 需要把同一份内容同步到 Obsidian、飞书和 IMA

## `draft.images` 示例

```yaml
images:
  - path: /absolute/path/to/local.png
    alt: 本地图片
  - src: https://example.com/cover.png
    alt: 远程图片
  - srcset: https://example.com/cover-1x.png 1x, https://example.com/cover-2x.png 2x
    alt: 响应式图片
```

`path` 用于本地文件，`src` / `data_src` / `data-original` / `data-lazy-src` / `original` 等用于远程图片；`srcset` 会优先选数值更高的候选。

## 快速使用

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```

## 相关入口

- [English README](README_EN.md)
- [安装说明](INSTALL.md)
- [GitHub 仓库](https://github.com/cjke84/knowledge-organizer)
