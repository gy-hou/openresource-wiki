---
date: 2026-04-07
authors:
  - gy-hou
categories:
  - AI 工具
tags:
  - 知识库
  - Claude Code
  - Obsidian
  - 效率
  - 教程
slug: karpathy-knowledge-base
---

# 一个 Prompt + 工具清单，搭建 Karpathy 本地知识库

> 把工具清单和 Prompt 直接复制发给你的 Claude Code / Codex 就能开搭

<!-- more -->

{{ card_row(xhs_note("一个命令和工具清单实现Karpathy本地知识库", "https://www.xiaohongshu.com/discovery/item/69d27fe6000000002103823e", 294, 650, "把工具清单和 Prompt 直接复制发给你的 Claude Code / Codex 就能开搭")) }}

---

## 📐 架构：就三层

**① 原始资料层**（只读，LLM 不改）

你的论文、文章、笔记、截图、网页剪藏。

**② Wiki 层**（LLM 写和维护，你只看）

结构化的 Markdown 文件：摘要、卡片、索引、综述，全部自动生成。

**③ Schema 层**（告诉 LLM 怎么干活）

一个 `CLAUDE.md` 或 `AGENTS.md`，写清楚目录结构、命名规范、工作流程。

---

## 🔧 工具清单：按层拆解

### 资料采集

| 工具 | 干嘛的 | 门槛 |
|------|--------|------|
| Obsidian Web Clipper | 浏览器一键把网页变成 Markdown | 装插件就行 |
| Jina Reader（`r.jina.ai`） | 任意 URL → 干净 Markdown，LLM 直接能读 | 免费 API |
| Zotero | 学术党必备，论文管理 + 一键导出 BibTeX | 免费 |
| Readwise | 把 Kindle / 微信读书 / Pocket 的标注自动同步到本地 | 付费 |
| MarkDownload | 另一个网页转 Markdown 的浏览器扩展 | 免费 |
| 微信输入法语音转文字 | 随手录想法，复制到笔记里 | 自带 |

### 知识库 IDE（你看 wiki 用的）

| 工具 | 干嘛的 | 门槛 |
|------|--------|------|
| **Obsidian** | 本地 Markdown 编辑器，图谱视图能看知识连接 | 免费，核心推荐 |
| obsidian-cli | 让 Agent 通过命令行操作 Obsidian | `brew install obsidian-cli` |
| Obsidian Dataview 插件 | 在笔记上跑查询，比如按标签列出所有论文 | 装插件 |
| Obsidian Marp 插件 | Markdown 直接生成幻灯片 | 装插件 |
| Logseq | Obsidian 的替代品，大纲式组织，也是本地 Markdown | 免费 |

### LLM Agent（帮你写和维护 wiki 的）

| 工具 | 特点 | 适合谁 |
|------|------|--------|
| **Claude Code** | 最稳，读写本地文件无障碍，适合单人 wiki | 有 API key 就行 |
| **Codex (OpenAI)** | 适合顺序执行，配合 AGENTS.md | 类似 |
| **OpenClaw** | 开源本地 Agent，支持多 Agent 编排 + 浏览器自动化 | 折腾党 |
| Cursor / Windsurf | 代码编辑器但也能操作 Markdown 文件 | 已经在用的 |
| Aider | 开源命令行 AI 编程助手，也能管 Markdown 仓库 | 极客 |

### 搜索和索引

| 工具 | 干嘛的 | 门槛 |
|------|--------|------|
| **qmd** | 本地 Markdown 语义搜索，BM25 + 向量混合 | `npm install -g @tobilu/qmd` |
| Ollama + Embedding 模型 | 本地跑向量化，配合 qmd 使用 | 需要 8G+ 内存 |
| ripgrep (`rg`) | 极速全文搜索，Agent 的 grep 神器 | `brew install ripgrep` |
| fzf | 模糊搜索，快速定位文件 | `brew install fzf` |

---

## 📋 复制这段给你的 Agent

把上面的工具清单和下面的 Prompt 直接发给你的 Claude Code 或 Codex：

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
一个资料可能涉及 10-15 个页面的更新。

### 查询（Query）
当我问问题时：
1. 先读 index.md 找到相关页面
2. 深入阅读这些页面
3. 综合回答，引用具体页面
4. 如果回答有价值，存为 outputs/ 下的新页面，更新 index.md

### 健康检查（Lint）
定期检查：
- 页面之间有没有矛盾
- 有没有孤立页面（没有任何链接指向它）
- 有没有提到但还没建页面的概念
- 有没有过时信息可以用新资料更新

## 规范
- 所有文件用 Markdown
- 页面之间用 [[wiki-links]] 互相引用
- 每个页面开头有 YAML frontmatter（tags, date, sources）
- index.md 按类别组织，每次摄入都更新
- log.md 每条格式：## [YYYY-MM-DD] ingest/query/lint | 标题

先帮我创建这个目录结构和一个空的 index.md + log.md。
然后阅读工具清单并根据我的本地电脑信息，选择适配的工具。
最后告诉我怎么开始，采取问答式协同工作。
```

---

## 💡 进阶玩法

- **个人日记编译**：把日记、Apple Notes、聊天记录扔进 `raw/`，LLM 自动提取你的偏好、习惯、目标，生成"关于我"的 wiki（Farza 做的 Farzapedia 就是这个思路）
- **读书笔记**：每读一章扔进去，LLM 自动维护角色页、主题页、时间线，读完你就有了一个私人 fan wiki
- **Finetuning**：当 wiki 大到一定程度，可以用它微调一个开源模型，让 AI 把你的知识"记在权重里"而不只是"读你的文件"

---

## 🎯 核心原则

- **你的数据在你本地**，不在任何 AI 公司的服务器上
- **纯 Markdown + 文件**，任何工具都能读，任何 AI 都能用
- **换 AI 不丢数据**——今天用 Claude，明天用 GPT，后天用开源模型，wiki 还是你的
- **人负责方向，机器负责跑腿**

---

## 必装 4 个工具

| 工具 | 作用 |
|------|------|
| **Obsidian** | 知识库本体，没它看不了 wiki |
| **Claude Code** | 写入和维护（其他 agent 也可） |
| **ripgrep** | CC 搜索和 lint 的底层命令 |
| **Git** | wiki 版本控制 |

**按需安装：**

- `Obsidian Web Clipper`：网页转 Markdown
- `marker-pdf`：有 PDF 需求时安装
- `Pandoc`：对外导出多格式
- `qmd`：wiki 内容积累到几百篇后再安，现在 `rg` 够用
