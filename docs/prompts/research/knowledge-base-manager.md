---
tags:
  - prompt
  - 知识库
  - Claude Code
  - 研究
---

# LLM 本地知识库管理 Prompt

> 自研 Prompt：让 AI 管理你的本地 Markdown 知识库（Karpathy 风格）

## 适用场景

- 用 Claude Code / Codex 管理本地 Obsidian 知识库
- 自动摘要、交叉引用、健康检查
- 配合 `raw/ → wiki/ → CLAUDE.md` 三层架构

## Prompt

```
你是我的个人知识库管理员。请帮我在本地搭建一个 LLM Wiki 系统。

## 架构

三个目录：
- raw/        → 原始资料（你只读不改）
- wiki/       → 你生成并维护的 Markdown 知识库
- CLAUDE.md   → 工作规范（我们一起写）

## Wiki 结构

wiki/
├── index.md          ← 所有页面的目录（每页一行：链接 + 一句话摘要）
├── log.md            ← 操作日志（## [日期] 操作类型 | 标题）
├── concepts/         ← 概念页（每个重要概念一个 .md）
├── entities/         ← 实体页（人物、项目、公司、工具）
├── sources/          ← 每个原始资料的摘要页
└── outputs/          ← 查询产出（综述、对比表、分析）

## 核心工作流

### 摄入（Ingest）
当我把新文件放进 raw/ 并告诉你处理时：
1. 读原文，和我讨论要点
2. 在 sources/ 写一页摘要
3. 更新 index.md
4. 更新所有相关的 concepts/ 和 entities/ 页面
5. 在 log.md 追加记录

### 查询（Query）
当我问问题时：
1. 先读 index.md 找到相关页面
2. 深入阅读这些页面
3. 综合回答，引用具体页面
4. 如果回答有价值，存为 outputs/ 下的新页面

### 健康检查（Lint）
定期检查：
- 页面之间有没有矛盾
- 有没有孤立页面
- 有没有提到但还没建页面的概念
- 有没有过时信息

## 规范
- 所有文件用 Markdown
- 页面之间用 [[wiki-links]] 互相引用
- 每个页面开头有 YAML frontmatter（tags, date, sources）
- index.md 按类别组织，每次摄入都更新

先帮我创建目录结构和空的 index.md + log.md，然后告诉我怎么开始。
```

## 配套工具

| 工具 | 作用 |
|------|------|
| Obsidian | 知识库本体 |
| Claude Code | 写入和维护 |
| ripgrep | 搜索和 lint 底层 |
| Git | 版本控制 |

详细搭建教程：[一个 Prompt + 工具清单，搭建 Karpathy 本地知识库](../../blog/posts/2026-04-07-karpathy-knowledge-base.md)
