# Phase 5: 最终打磨

> 本阶段完成 404 页面、LICENSE、最终验证，确保整个项目可以正常部署。

---

## Prompt 5.1 — 404 页面 + LICENSE + README 完善

```
完成最终的细节文件。

## 1. 创建 `docs/404.md`

```markdown
---
hide:
  - navigation
  - toc
  - footer
---

# 404 — 页面走丢了

<div style="text-align: center; padding: 2rem 0;">

<p style="font-size: 4rem; margin: 0;">🤖💨</p>

<p style="font-size: 1.2rem; color: var(--md-default-fg-color--light);">
你要找的页面不存在，可能已经被移动或删除。
</p>

<div style="margin-top: 2rem;">

[🏠 回到首页](index.md){ .md-button .md-button--primary }
&nbsp;&nbsp;
[🔍 搜索内容](#){ .md-button }

</div>

</div>

---

**可能的原因：**

- 链接拼写有误
- 页面已被移动到其他位置
- 页面还没写完（我们在努力了！）

**你可以：**

- 使用顶部搜索栏查找内容
- 浏览 [标签索引](tags.md) 找到感兴趣的主题
- 去 [GitHub Issues](https://github.com/gy-hou/publicwiki/issues) 告诉我们
```

## 2. 创建 `LICENSE`

创建 CC BY-SA 4.0 LICENSE 文件（这是内容共享的常用协议）：

```
Attribution-ShareAlike 4.0 International

=======================================================================

Creative Commons Corporation ("Creative Commons") is not a law firm and
does not provide legal services or legal advice. Distribution of
Creative Commons public licenses does not create a lawyer-client or
other relationship. Creative Commons makes its licenses and related
information available on an "as-is" basis. Creative Commons gives no
warranties regarding its licenses, any material licensed under their
terms and conditions, or any related information. Creative Commons
disclaims all liability for damages resulting from their use to the
fullest extent possible.

... (完整的 CC BY-SA 4.0 license 文本)
```

注意：请使用完整的 CC BY-SA 4.0 license 文本。
可以从 https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt 获取完整文本。
如果无法获取完整文本，创建一个简化版本并标注 TODO。

简化版：
```
Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)

Copyright (c) 2025-2026 gy-hou

You are free to:
- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution: You must give appropriate credit, provide a link to the license,
  and indicate if changes were made.
- ShareAlike: If you remix, transform, or build upon the material, you must
  distribute your contributions under the same license as the original.

Full license text: https://creativecommons.org/licenses/by-sa/4.0/legalcode

Code snippets and scripts in this repository are licensed under the MIT License
unless otherwise noted.
```

## 3. 完善 README.md

更新 README.md 为最终版本：

```markdown
# AI Wiki

[![Deploy](https://github.com/gy-hou/publicwiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/gy-hou/publicwiki/actions/workflows/deploy.yml)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> AI 工具、Prompts、Skills 开源分享站

🌐 **在线访问**：https://gy-hou.github.io/publicwiki/

## 这是什么

一个开源的 AI 知识库，收录了：

- 📝 **博客** — 小红书热帖文字版、AI 热点解读、实操教程
- 💡 **Prompt 库** — 精心调试的 Prompt 合集
- 🛠️ **Skills 库** — Claude Skills 和自动化模板
- 🧰 **工具箱** — AI 工具推荐和对比
- 🚀 **项目** — 开源项目展示

## 本地开发

​```bash
# 安装依赖
make install

# 本地预览
make serve

# 构建
make build

# 查看所有命令
make help
​```

## 贡献

欢迎贡献内容！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

内容部分采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 协议。
代码部分采用 MIT 协议。
```

确保所有 badge 链接正确（仓库名为 `gy-hou/publicwiki`）。
```

---

## Prompt 5.2 — 全面验证和修复

```
对整个项目进行全面检查，修复所有发现的问题。这是最后一个 prompt，请确保一切就绪。

## 检查清单

### 1. mkdocs.yml 验证
- [ ] YAML 语法正确（可被 Python yaml.safe_load 解析）
- [ ] nav 中引用的每个 .md 文件都存在
- [ ] 没有重复的 nav 条目
- [ ] plugins 配置正确（blog, tags, search, git-revision-date-localized, rss）
- [ ] theme 配置完整
- [ ] site_url 设置为 https://gy-hou.github.io/publicwiki/

### 2. 文件完整性
确保以下文件都存在且非空：
- [ ] mkdocs.yml
- [ ] requirements.txt
- [ ] .gitignore
- [ ] README.md
- [ ] LICENSE
- [ ] CONTRIBUTING.md
- [ ] Makefile
- [ ] .editorconfig
- [ ] docs/index.md（首页）
- [ ] docs/tags.md
- [ ] docs/404.md
- [ ] docs/blog/index.md
- [ ] docs/blog/.authors.yml
- [ ] docs/blog/posts/（至少 5 篇文章）
- [ ] docs/prompts/index.md + 4 个 prompt 页面
- [ ] docs/skills/index.md + 2 个 skill 页面
- [ ] docs/toolbox/index.md + 3 个工具页面
- [ ] docs/projects/index.md
- [ ] docs/ideas/index.md
- [ ] docs/about/index.md
- [ ] docs/about/roadmap.md
- [ ] docs/assets/stylesheets/extra.css
- [ ] docs/assets/javascripts/mathjax.js
- [ ] docs/robots.txt
- [ ] overrides/main.html
- [ ] overrides/partials/comments.html
- [ ] scripts/ocr_to_markdown.py
- [ ] scripts/lint_content.py
- [ ] scripts/README.md
- [ ] .github/workflows/deploy.yml
- [ ] .github/workflows/lint.yml
- [ ] .github/ISSUE_TEMPLATE/content-request.md
- [ ] .github/ISSUE_TEMPLATE/bug-report.md

### 3. 内容检查
- [ ] 所有 .md 文件的 frontmatter 格式正确
- [ ] 没有未闭合的代码块
- [ ] Blog 文章的 date 字段格式正确（YYYY-MM-DD）
- [ ] Blog 文章都在 docs/blog/posts/ 下
- [ ] 所有内部链接指向存在的文件
- [ ] 所有 index.md 都有实质性内容（不是空的）

### 4. 构建验证
- 尝试运行 `mkdocs build --strict`（如果已安装 mkdocs）
- 如果没有安装，至少确保 YAML 语法正确

### 5. 目录结构检查
- 输出完整的项目目录树（排除 .git、node_modules、site、__pycache__）
- 确认目录结构与 mkdocs.yml nav 一致

### 6. 修复
- 如果发现任何问题，**直接修复**，不要只是报告
- 修复后重新检查确保没有引入新问题

### 7. 最终输出
完成所有检查和修复后，输出：
1. 完整的目录树
2. 发现并修复的问题列表（如果有）
3. 仍然存在的 TODO 标记数量
4. 最终状态确认
```

---

## 本阶段完成标准

- [ ] 404.md 存在
- [ ] LICENSE 存在
- [ ] README.md 有 badge 和完整说明
- [ ] 全面验证通过，所有文件就绪
- [ ] 目录结构完整，无遗漏
- [ ] 项目准备好首次 push 和部署
