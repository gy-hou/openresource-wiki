# Phase 2: 占位内容填充

> 本阶段为所有板块填充结构完整的模板内容。
> 所有正文都是占位，后续由 Gary 替换为真实内容。
> 每篇内容用 `<!-- TODO: 替换为真实内容 -->` 标注。

---

## Prompt 2.1 — Blog 文章（5 篇模板帖子）

```
在 `docs/blog/posts/` 下创建 5 篇模板博客文章。使用 Material blog plugin 的格式。

所有文章的正文都是占位内容，但结构必须完整（标题、frontmatter、各个 section），
让读者能看到最终效果的样子。每篇文章在正文中标注 `<!-- TODO: 替换为真实内容 -->`。

### 文章 1: `docs/blog/posts/2026-04-01-deepseek-api-guide.md`

```markdown
---
date: 2026-04-01
authors:
  - gy-hou
categories:
  - AI 工具
tags:
  - DeepSeek
  - API
  - 教程
---

# DeepSeek API 完全使用指南

> 手把手教你用 DeepSeek API，省钱又好用

<!-- more -->

## TL;DR

DeepSeek 是目前性价比最高的国产大模型 API 之一。本文手把手教你从注册到搭配 Chatbox 使用的全流程。

<!-- TODO: 替换为真实内容 -->

## 为什么选 DeepSeek

占位内容：对比各家 API 的价格和效果...

## 注册和获取 API Key

### 第一步：注册账号

占位内容...

### 第二步：获取 API Key

占位内容...

!!! warning "注意"
    API Key 要妥善保管，不要上传到 GitHub。

## 搭配 Chatbox 使用

​```json
{
  "api_endpoint": "https://api.deepseek.com/v1",
  "model": "deepseek-chat",
  "api_key": "your-api-key-here"
}
​```

## 搭配代码使用

​```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
​```

## 常见问题

??? question "API 调用报错怎么办？"
    占位回答...

??? question "每月大概花多少钱？"
    占位回答...

## 相关资源

- [DeepSeek 官方文档](https://platform.deepseek.com/docs)
- [Chatbox 下载](https://chatboxai.app/)

---

!!! original "原始来源"
    本文整理自小红书帖子：<!-- TODO: 填入原帖链接 -->
```

### 文章 2: `docs/blog/posts/2026-03-25-claude-code-tips.md`

- 标题：Claude Code 进阶使用技巧
- categories: [AI 工具]
- tags: [Claude, Claude Code, 效率]
- 结构：TL;DR → 基础配置 → 10 个实用技巧（每个一小节，含代码示例）→ 常见坑 → 相关资源
- 每个技巧占位但标题要真实有用（如：善用 /compact、Plan 模式、自定义 Skills 等）

### 文章 3: `docs/blog/posts/2026-03-20-gemini-edu-discount.md`

- 标题：用 edu 邮箱薅 Google Gemini 15 个月会员
- categories: [薅羊毛]
- tags: [Gemini, Google, 教程, edu]
- 结构：TL;DR → 你需要什么 → 详细步骤（5步，含截图占位 `![步骤X截图](../../assets/images/placeholder.png)`）→ 常见问题 → 注意事项

### 文章 4: `docs/blog/posts/2026-03-15-ai-model-landscape.md`

- 标题：2026 年 AI 模型格局：谁在领跑？
- categories: [热点解读]
- tags: [AI模型, Claude, GPT, Gemini, DeepSeek]
- 结构：TL;DR → 各家最新动态（Claude/GPT/Gemini/DeepSeek 各一节）→ 个人排名 → 怎么选

### 文章 5: `docs/blog/posts/2026-03-10-prompt-engineering-101.md`

- 标题：Prompt Engineering 快速入门：从零到能用
- categories: [教程]
- tags: [Prompt, 入门, 教程]
- 结构：TL;DR → 什么是 Prompt Engineering → 5 个核心原则（每个配示例）→ 常见误区 → 推荐阅读

## 同时完成

1. 确保 `docs/blog/index.md` 内容正确（blog plugin 会自动生成列表，这个文件通常只需要：
   ```markdown
   ---
   hide:
     - toc
   ---

   # 博客

   欢迎来到博客区！这里有小红书热帖的文字版、AI 热点解读、实操教程等内容。
   ```

2. 更新 `mkdocs.yml` nav 中的博客部分（blog plugin 通常自动管理，确认 nav 配置正确）

3. 确保所有文章的 frontmatter 格式正确，date 字段符合 `YYYY-MM-DD` 格式

4. 所有文章中的代码块都要能正确渲染
```

---

## Prompt 2.2 — Prompt 库内容（4 个模板 Prompt）

```
在 `docs/prompts/` 下创建 4 个模板 Prompt 页面。正文是占位，但结构和格式要完整。

### Prompt 1: `docs/prompts/coding/code-review-prompt.md`

```markdown
---
tags:
  - prompt
  - 编程
  - Code Review
---

# 代码审查 Prompt

> 💡 **适用场景**：让 AI 对你的代码进行系统性审查
>
> **推荐模型**：Claude Opus / Sonnet
>
> **难度**：⭐ 入门

## Prompt 正文

​```text
你是一位资深软件工程师，请对以下代码进行全面的 Code Review。

请从以下维度逐一评审：

1. **正确性**：代码逻辑是否正确？是否有 bug？
2. **安全性**：是否存在安全漏洞（注入、XSS、敏感信息泄露等）？
3. **性能**：是否有明显的性能问题？
4. **可读性**：命名是否清晰？结构是否合理？
5. **可维护性**：是否容易理解和修改？
6. **最佳实践**：是否遵循了语言/框架的惯用写法？

对于每个问题，请：
- 指出具体的代码位置
- 解释为什么是问题
- 给出修改建议（附代码示例）

最后给出总体评分（1-10）和改进优先级排序。

代码如下：
​```

<!-- TODO: 可以替换为更精细的版本 -->

!!! tip "使用技巧"
    - 可以指定编程语言让审查更精准
    - 把相关的测试代码也一起发，评审会更全面
    - 如果是大型项目，分模块发送效果更好

## 效果示例

<!-- TODO: 添加实际使用截图 -->

## 变体版本

=== "基础版"

    ​```text
    请审查以下代码，指出潜在问题并给出改进建议。
    ​```

=== "安全专项版"

    ​```text
    你是一位安全工程师，请对以下代码进行安全审计。
    重点检查：SQL注入、XSS、CSRF、敏感信息泄露、
    权限绕过、不安全的反序列化等 OWASP Top 10 问题。
    ​```

=== "性能专项版"

    ​```text
    你是一位性能优化专家，请分析以下代码的性能瓶颈。
    关注：时间复杂度、空间复杂度、数据库查询效率、
    缓存策略、并发问题等。
    ​```
```

### Prompt 2: `docs/prompts/writing/xiaohongshu-writer.md`

- 标题：小红书爆款帖子写作 Prompt
- tags: [prompt, 写作, 小红书]
- 难度：⭐ 入门
- Prompt 正文：一个帮助生成小红书风格帖子的 system prompt（包含：标题技巧、正文结构、emoji 使用、话题标签）
- 变体：种草版 / 教程版 / 测评版

### Prompt 3: `docs/prompts/research/paper-reader.md`

- 标题：论文精读 Prompt
- tags: [prompt, 研究, 论文]
- 推荐模型：Claude Opus（长上下文）
- 难度：⭐⭐ 进阶
- Prompt 正文：一个结构化论文阅读 prompt（输出：一句话总结、核心贡献、方法论、实验结果、局限性、与其他工作的关系）
- 变体：快速扫读版 / 深度精读版 / 复现评估版

### Prompt 4: `docs/prompts/system/ai-assistant-system.md`

- 标题：通用 AI 助手 System Prompt 模板
- tags: [prompt, System Prompt, 模板]
- 难度：⭐⭐ 进阶
- Prompt 正文：一个可定制的 system prompt 框架（角色定义、能力边界、输出格式、语气风格、安全约束）
- 变体：客服版 / 教学版 / 专家顾问版

## 同时更新

1. 更新 `docs/prompts/index.md`：用卡片网格展示 4 个分类，每个分类显示已有的 prompt 数量（占位数字）
2. 更新各子目录的 `index.md`：列出该分类下的 prompt（链接列表）
3. 更新 `mkdocs.yml` nav，加入所有新页面
```

---

## Prompt 2.3 — Skills 库内容（2 个模板 Skill）

```
在 `docs/skills/` 下创建 2 个模板 Skill 页面。

### Skill 1: `docs/skills/templates/xhs-card-generator.md`

```markdown
---
tags:
  - skill
  - 小红书
  - 自动化
---

# 小红书知识卡片生成器

> 🛠️ 把长文内容自动切成小红书风格的知识卡片

| 属性 | 信息 |
|------|------|
| 类型 | 内容生成 |
| 适用工具 | Claude Code |
| 依赖 | 无 |

## 功能说明

输入一篇长文或大纲，自动生成适合小红书传播的图文卡片系列。每张卡片控制在合适的信息密度，配合美观的 HTML 模板。

## Skill 内容

​```markdown
<!-- TODO: 填入完整的 Skill prompt -->
当用户提供文章或主题时，将内容拆分为 5-8 张知识卡片...
​```

## 使用方法

1. 在 Claude Code 中加载此 Skill
2. 提供文章内容或主题
3. 生成的卡片可以直接截图发小红书

!!! tip "最佳实践"
    - 每张卡片控制在 3-5 个要点
    - 标题要有吸引力
    - 适当使用 emoji 增加可读性
```

### Skill 2: `docs/skills/templates/llm-wiki-agent.md`

- 标题：LLM Wiki 知识库管理 Agent
- tags: [skill, 知识库, Agent]
- 适用工具：Claude Code / Codex
- 功能：让 AI Agent 自动管理 Markdown 知识库（添加、搜索、更新、整理笔记）
- Skill 内容占位，参考 Karpathy 的 LLM Wiki idea
- 使用方法步骤

## 同时更新

1. `docs/skills/index.md`：展示 Skills 库的说明和列表
2. `docs/skills/templates/index.md`：列出可用模板
3. `mkdocs.yml` nav
```

---

## Prompt 2.4 — 工具箱内容（3 个模板页面）

```
在 `docs/toolbox/` 下创建 3 个模板工具推荐页面。

### 页面 1: `docs/toolbox/ai-platforms/model-comparison.md`

```markdown
---
tags:
  - 工具
  - AI模型
  - 对比
---

# 主流 AI 模型实测对比

> 🧰 各家大模型横向对比，帮你选择最适合的

<!-- TODO: 替换为真实数据 -->

## 模型一览表

| 模型 | 厂商 | 价格（百万token） | 上下文窗口 | 强项 | 个人评分 |
|------|------|-------------------|------------|------|----------|
| Claude Opus | Anthropic | $15 / $75 | 200K | 长文分析、编程 | ⭐⭐⭐⭐⭐ |
| GPT-4o | OpenAI | $5 / $15 | 128K | 全能、多模态 | ⭐⭐⭐⭐ |
| Gemini 2.5 Pro | Google | $1.25 / $10 | 1M | 超长上下文 | ⭐⭐⭐⭐ |
| DeepSeek-V3 | DeepSeek | ¥1 / ¥2 | 128K | 性价比、中文 | ⭐⭐⭐⭐ |

## 各模型详评

### Claude Opus

占位评价...

### GPT-4o

占位评价...

### Gemini 2.5 Pro

占位评价...

### DeepSeek-V3

占位评价...

## 怎么选？

!!! tip "选择建议"
    - **预算有限**：DeepSeek
    - **编程为主**：Claude Opus + Claude Code
    - **需要多模态**：GPT-4o 或 Gemini
    - **超长文档**：Gemini 2.5 Pro
```

### 页面 2: `docs/toolbox/dev-tools/ai-coding-tools.md`

- 标题：AI 编程工具全景图
- tags: [工具, 编程, AI]
- 内容：对比表格 + 简评
  - Claude Code, Cursor, GitHub Copilot, Aider, Windsurf, Codex
  - 列：工具名、类型（CLI/IDE/插件）、价格、模型、强项
  - 每个工具 3-5 句简评

### 页面 3: `docs/toolbox/workflows/wiki-setup-tools.md`

- 标题：搭建个人 Wiki 的工具清单
- tags: [工具, Wiki, 工作流]
- 用分层结构推荐工具：
  - 框架层：MkDocs, Docusaurus, VitePress, Hugo
  - 编辑层：VS Code, Obsidian, Typora
  - 部署层：GitHub Pages, Vercel, Netlify
  - 辅助层：搜索插件、评论系统、分析工具
  - 每层一个表格

## 同时更新

1. 所有 toolbox 相关 index.md
2. mkdocs.yml nav
```

---

## Prompt 2.5 — Projects / Ideas / About 页面

```
填充剩余的板块页面。

### 1. `docs/projects/index.md`

```markdown
---
hide:
  - toc
---

# 开源项目

> 🚀 我的开源项目展示。大部分项目都在积极开发中。

<!-- TODO: 项目上线后替换为真实内容 -->

<div class="card-grid" markdown>

<div class="card" markdown>
<div class="card-icon">📊</div>
<div class="card-title">TrendR</div>
<div class="card-desc">自动化文献综述工具，追踪研究领域趋势</div>
<br>
🟡 开发中 · Python · [GitHub](#)
</div>

<div class="card" markdown>
<div class="card-icon">🐾</div>
<div class="card-title">OpenClaw</div>
<div class="card-desc">开源 AI 工具集</div>
<br>
🟡 开发中 · [GitHub](#)
</div>

<div class="card" markdown>
<div class="card-icon">🌐</div>
<div class="card-title">AI Wiki</div>
<div class="card-desc">就是本站！AI 工具和 Prompt 的开源分享</div>
<br>
🟢 活跃 · MkDocs · [GitHub](https://github.com/gy-hou/publicwiki)
</div>

</div>

!!! info "想了解更多？"
    每个项目的详细文档正在撰写中，敬请期待。
```

### 2. `docs/ideas/index.md`

```markdown
# Ideas 实验室

> 💭 这里记录一些实验性的想法和探索。不一定成熟，但希望能激发灵感。

<!-- TODO: 添加具体 idea 页面 -->

!!! note "关于这个板块"
    这里的内容可能不够完善，甚至可能是错的。
    它们更像是思考的草稿，而不是最终结论。
    欢迎讨论和质疑！

## 即将到来

- [ ] LLM 作为个人知识库管理工具的可行性
- [ ] 用 AI 自动化小红书内容生产工作流
- [ ] 个人 AI Agent 工作流设计模式
- [ ] 开源社区运营的一些想法

*有想讨论的 idea？欢迎在评论区留言或提 Issue。*
```

### 3. `docs/about/index.md`

```markdown
---
hide:
  - toc
---

# 关于我

<!-- TODO: 替换为真实自我介绍 -->

## 👋 你好

<!-- TODO: 替换以下占位内容 -->

这里是一段关于自己的介绍。包括：

- 教育背景（占位）
- 目前在做什么（占位）
- 兴趣方向（占位）

## 🤔 为什么做这个 Wiki

几个原因：

1. **小红书有字数和格式限制**——很多干货只能做成图片，读者没法复制代码和 Prompt
2. **好内容值得结构化**——图片里的信息检索不到，不方便二次传播
3. **开源精神**——我从开源社区获益良多，希望也能回馈一些
4. **自我驱动的学习**——整理和分享的过程本身就是最好的学习

## 📱 找到我

| 平台 | 链接 |
|------|------|
| GitHub | [gy-hou](https://github.com/gy-hou) |
| 小红书 | <!-- TODO: 填写小红书链接 --> |
| 邮箱 | <!-- TODO: 填写邮箱 --> |

## 💬 反馈

- 内容建议 → [提 Issue](https://github.com/gy-hou/publicwiki/issues)
- 投稿 → [贡献指南](https://github.com/gy-hou/publicwiki/blob/main/CONTRIBUTING.md)
```

### 4. `docs/about/roadmap.md`

```markdown
# 更新路线图

> 📋 记录 Wiki 的建设进度和未来计划

## 已完成 ✅

- [x] 搭建 Wiki 基础框架（MkDocs + Material）
- [x] 配置 GitHub Actions 自动部署
- [x] 创建内容模板系统
- [x] 设计首页和视觉样式
- [x] 填充模板示例内容
- [x] 配置 Blog 插件
- [x] 添加标签系统

## 进行中 🚧

- [ ] 迁移小红书热帖 Top 10（文字版）
- [ ] 整理并发布 Prompt 库 v1（10+ prompts）
- [ ] 发布 Claude Skills 合集

## 计划中 📝

- [ ] 添加 Giscus 评论系统
- [ ] 搭建 OCR → Markdown 自动化管道
- [ ] 添加 RSS 订阅
- [ ] AI 工具对比评测系列
- [ ] 完善 Projects 板块文档
- [ ] 添加站内统计（访问量、热门页面）

## 长期愿景 🌟

- [ ] 英文版本支持
- [ ] 社区贡献机制完善
- [ ] 自动化内容管道（小红书 → Wiki 半自动同步）
- [ ] Newsletter 订阅

---

*最后更新：2026-04-07*

*有建议？欢迎在 [Issues](https://github.com/gy-hou/publicwiki/issues) 中提出。*
```

## 同时更新

1. `mkdocs.yml` nav 确保所有新页面都已加入
2. 确保首页 `docs/index.md` 的"最近更新"区域链接到这些新页面
```

---

## 本阶段完成标准

- [ ] 5 篇 blog 文章存在且格式正确（blog plugin 能识别）
- [ ] 4 个 prompt 页面存在，每个都有完整的 prompt 代码块
- [ ] 2 个 skill 页面存在
- [ ] 3 个 toolbox 页面存在
- [ ] projects / ideas / about / roadmap 页面内容完整
- [ ] 所有 index.md 都更新了内容列表
- [ ] mkdocs.yml nav 完整无遗漏
- [ ] `mkdocs build --strict` 无报错
