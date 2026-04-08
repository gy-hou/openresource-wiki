# Phase 1: 视觉设计 + 首页 + 模板系统

> 本阶段完成 Wiki 的视觉体验、首页内容、和可复用的内容模板。
> 完成后 Wiki 应该有一个好看的首页和完整的模板库。

---

## Prompt 1.1 — 自定义 CSS 样式

```
编辑 `docs/assets/stylesheets/extra.css`，为 Wiki 添加完整的自定义样式。

## 设计原则
- 干净、现代、重视可读性
- 中文排版优化
- light/dark 两种模式都要好看
- 专为 Prompt 展示和代码分享优化

## 需要的样式

### 1. 中文排版基础
```css
/* 中文排版优化 */
body {
  /* 中文行高需要更大 */
}
.md-typeset {
  font-size: 0.82rem;  /* 适合中文阅读 */
  line-height: 1.8;     /* 中文行间距 */
}
.md-typeset p {
  /* 段落间距 */
}
```

### 2. Prompt 展示专用样式
创建 `.prompt-block` class，用于大段 prompt 展示：
- 浅色模式：浅紫色背景 (#f5f0ff)，左边框 3px 紫色 (#6C3EA6)
- 深色模式：深灰背景 (#2d2d3d)，左边框紫色
- 等宽字体（JetBrains Mono）
- 圆角 8px
- padding: 1.2rem
- 内部保留换行和缩进（white-space: pre-wrap）
- 在代码块右上角显示语言标签

### 3. 卡片网格布局
创建 `.card-grid` 和 `.card` class：
- 响应式网格：桌面 3 列，平板 2 列，手机 1 列
- 卡片样式：
  - 圆角 12px
  - 微妙的阴影
  - hover 时轻微上浮 + 阴影加深
  - padding: 1.5rem
  - 浅色模式白色背景，深色模式 #1e1e2e 背景
- 卡片内 `.card-icon` 大字号 emoji 展示
- 卡片内 `.card-title` 标题样式
- 卡片内 `.card-desc` 描述文字样式（灰色、小号）

### 4. 标签样式
```css
/* 自定义标签 pill 样式 */
.md-typeset .md-tag {
  /* 圆角 pill 形状 */
  /* 紫色系配色 */
}
```

### 5. 代码块增强
- 圆角 8px
- 更好的行间距
- 代码块 max-height: 600px + overflow scroll（防止超长 prompt 撑爆页面）

### 6. Admonition 样式微调
- 自定义 admonition type "prompt"：紫色，图标用 material-robot
- 自定义 admonition type "original"：橙色，图标用 material-link-variant（用于标注原帖链接）

### 7. 表格样式
- 斑马纹
- 圆角
- 表头深色背景

### 8. 响应式微调
- 移动端 nav 优化
- 移动端代码块横向滚动
- 移动端卡片单列

### 9. 滚动条美化（webkit）
- 窄滚动条
- 紫色系主题色

### 10. 页面过渡动画
- 淡入效果
- 卡片 hover 过渡

确保所有样式都兼容 light 和 dark 模式（使用 `[data-md-color-scheme="slate"]` 选择器）。
```

---

## Prompt 1.2 — 首页设计

```
重写 `docs/index.md`，设计一个精美的首页。

## 页面结构

### Hero 区域
```markdown
---
hide:
  - navigation
  - toc
---

# AI Wiki

> 🤖 AI 工具、Prompts、Skills 的开源分享站
>
> 把小红书装不下的干货，都放在这里。
```

### 关于我（简短）
- 3-4 句话的自我介绍占位
- 标注 `<!-- TODO: Gary 填写真实自我介绍 -->`
- 提及：AI 深度用户、小红书博主、开源爱好者

### 板块导航（卡片网格）
使用 Phase 1.1 中定义的 `.card-grid` 样式，展示 6 个板块：

| 板块 | Emoji | 描述 |
|------|-------|------|
| 博客 | 📝 | 小红书热帖文字版、AI 热点解读、实操教程 |
| Prompt 库 | 💡 | 精心调试的 Prompt 合集，覆盖编程 / 写作 / 研究 |
| Skills 库 | 🛠️ | Claude Skills 和自动化工作流模板 |
| 工具箱 | 🧰 | AI 工具推荐、平台对比、工作流搭建 |
| 项目 | 🚀 | 开源项目展示：TrendR、OpenClaw 等 |
| Ideas | 💭 | 实验性想法和探索记录 |

每个卡片链接到对应 section。使用 HTML + CSS class 实现：

```html
<div class="card-grid" markdown>

<a class="card" href="blog/">
  <div class="card-icon">📝</div>
  <div class="card-title">博客</div>
  <div class="card-desc">小红书热帖文字版、AI 热点解读、实操教程</div>
</a>

<!-- 其余 5 个卡片同理 -->

</div>
```

### 为什么做这个 Wiki
用 admonition (info) 包裹，内容：
- 小红书有字数限制，很多干货只能做成图片
- 图片里的代码和 Prompt 没法复制，读者体验差
- 想把优质内容结构化、开源出来
- 这里的一切都可以直接复制使用

### 最近更新
手动列出 3-5 个占位链接：
```markdown
## 最近更新

| 日期 | 内容 | 板块 |
|------|------|------|
| 2026-04-07 | 占位标题 1 | 博客 |
| 2026-04-06 | 占位标题 2 | Prompt 库 |
| ... | ... | ... |

<!-- TODO: 后续可以用插件自动生成 -->
```

### 底部统计和链接
- 内容统计：X 篇博客 / X 个 Prompts / X 个 Skills（手动数字占位）
- GitHub Star 按钮
- 小红书链接占位
- "贡献内容" 链接到 CONTRIBUTING.md

整个首页使用 `hide: [navigation, toc]` 让页面更宽敞。
确保在移动端也显示良好。
```

---

## Prompt 1.3 — 内容模板系统

```
在 `docs/_templates/` 下创建可复用的内容模板，并创建 CONTRIBUTING.md。

## 1. 模板文件

### a. `docs/_templates/blog-post.md` — 博客文章模板（供 blog plugin 使用）

```markdown
---
date: YYYY-MM-DD
authors:
  - gary
categories:
  - 待分类
tags:
  - 待填写
---

# 文章标题

> 📌 一句话摘要

<!-- more -->

## TL;DR

一句话总结核心要点。

## 正文

正文内容。

<!-- TODO: 替换为真实内容 -->

## 相关资源

- [资源名称](链接)

---

!!! original "原始来源"
    本文整理自小红书帖子：[原帖链接](#)
```

### b. `docs/_templates/prompt-template.md` — Prompt 分享模板

```markdown
---
tags:
  - prompt
  - 待填写
---

# Prompt 名称

> 💡 **适用场景**：一句话说明
>
> **推荐模型**：Claude Opus / Sonnet / GPT-4 / 通用
>
> **难度**：⭐ 入门 / ⭐⭐ 进阶 / ⭐⭐⭐ 高级

## Prompt 正文

​```text
（prompt 正文，读者可直接复制使用）
​```

!!! tip "使用技巧"
    - 技巧 1
    - 技巧 2

## 使用说明

1. 步骤一
2. 步骤二

## 效果示例

<!-- TODO: 添加使用效果截图或文字描述 -->

## 变体版本

=== "基础版"

    ​```text
    基础版 prompt
    ​```

=== "进阶版"

    ​```text
    增强版 prompt，加入更多约束
    ​```

=== "英文版"

    ​```text
    English version of the prompt
    ​```
```

### c. `docs/_templates/skill-template.md` — Claude Skill 模板

```markdown
---
tags:
  - skill
  - 待填写
---

# Skill 名称

> 🛠️ 一句话描述这个 Skill 做什么

| 属性 | 信息 |
|------|------|
| 类型 | 自动化 / 分析 / 生成 / 其他 |
| 适用工具 | Claude Code / Claude Desktop / 通用 |
| 依赖 | 无 / 需要 XXX |

## 功能说明

详细描述这个 Skill 的功能和使用场景。

## Skill 内容

​```markdown
（完整的 Skill / System Prompt / CLAUDE.md 内容）
​```

## 配套代码（可选）

​```python
# 如果有配套脚本
​```

## 安装 / 使用方法

1. 步骤一
2. 步骤二

!!! warning "注意事项"
    - 注意 1
    - 注意 2
```

### d. `docs/_templates/tool-template.md` — 工具推荐模板

```markdown
---
tags:
  - 工具
  - 待填写
---

# 工具名称

> 🧰 一句话描述

| 属性 | 信息 |
|------|------|
| 官网 | [链接]() |
| 价格 | 免费 / 免费增值 / 付费 ($X/月) |
| 平台 | macOS / Windows / Linux / Web / CLI |
| 上手难度 | ⭐ / ⭐⭐ / ⭐⭐⭐ |
| 推荐指数 | ⭐⭐⭐⭐⭐ |

## 我为什么推荐它

个人使用体验和推荐理由。

## 快速上手

​```bash
# 安装命令
​```

最简使用步骤。

## 进阶用法

高级技巧和配置。

## 替代品对比

| 工具 | 优势 | 劣势 |
|------|------|------|
| 本工具 | ... | ... |
| 替代品A | ... | ... |
```

### e. `docs/_templates/project-template.md` — 项目展示模板

```markdown
---
tags:
  - 项目
  - 待填写
---

# 项目名称

> 🚀 一句话描述

| 属性 | 信息 |
|------|------|
| GitHub | [链接]() |
| 状态 | 🟢 活跃开发 / 🟡 维护中 / 🔴 已归档 |
| 技术栈 | Python / TypeScript / ... |
| License | MIT / Apache 2.0 / ... |

## 项目简介

这个项目解决什么问题？

## 核心功能

- 功能 1
- 功能 2

## 快速开始

​```bash
# 安装和运行
​```

## 架构简述

<!-- TODO: 添加架构图 -->

## 截图 / 演示

<!-- TODO: 添加截图 -->
```

## 2. CONTRIBUTING.md

创建根目录的 `CONTRIBUTING.md`：

```markdown
# 贡献指南

感谢你对本 Wiki 的兴趣！

## 如何贡献内容

### 1. Fork 本仓库

### 2. 选择合适的模板

模板位于 `docs/_templates/` 目录：

| 模板 | 用途 |
|------|------|
| `blog-post.md` | 博客文章、小红书帖子整理 |
| `prompt-template.md` | Prompt 分享 |
| `skill-template.md` | Claude Skill 分享 |
| `tool-template.md` | 工具推荐 |
| `project-template.md` | 项目展示 |

### 3. 创建内容文件

- **博客文章**放在 `docs/blog/posts/` 下，文件名格式：`YYYY-MM-DD-标题.md`
- **Prompt** 放在 `docs/prompts/对应分类/` 下
- **Skill** 放在 `docs/skills/` 下
- **工具推荐**放在 `docs/toolbox/对应分类/` 下

### 4. 文件命名规范

- 使用小写英文 + 短横线：`deepseek-api-guide.md` ✅
- 不要用中文文件名：`深度求索教程.md` ❌
- 不要用空格：`my file.md` ❌
- 不要用下划线：`my_file.md` ❌（index.md 除外）

### 5. 图片规范

- 图片放在 `docs/assets/images/` 下，按内容分子目录
- 压缩图片后再提交（推荐用 tinypng.com）
- 图片文件名用英文

### 6. 提交 PR

- PR 标题简洁明了
- 描述中说明添加了什么内容
- 确保 `mkdocs build --strict` 没有报错

## 标签规范

常用标签：
- 内容类型：`prompt`, `skill`, `工具`, `教程`, `热点解读`
- AI 模型：`Claude`, `GPT`, `Gemini`, `DeepSeek`
- 主题：`编程`, `写作`, `研究`, `效率`
- 难度：`入门`, `进阶`, `高级`

## 问题反馈

发现 bug 或有内容建议？请提 [Issue](https://github.com/gy-hou/openresource-wiki/issues)。
```

确保所有模板中的代码块都能被 MkDocs 正确渲染（注意嵌套代码块的转义）。
```

---

## 本阶段完成标准

- [ ] `extra.css` 包含所有定义的样式，light/dark 双模式
- [ ] 首页有完整的卡片网格、自我介绍、统计区域
- [ ] 5 个内容模板都在 `docs/_templates/`
- [ ] `CONTRIBUTING.md` 存在且内容完整
- [ ] 首页在桌面和移动端都显示正常
