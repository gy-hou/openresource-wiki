---
hide:
  - navigation
  - toc
---

# AI Wiki

> 🤖 AI 工具、Prompts、Skills 的开源分享站
>
> 把小红书装不下的干货，都放在这里。

## 关于我

我是一个长期深度使用 AI 的实践者，也在小红书持续分享能直接复用的工作方法。  
我希望把分散在图片、评论区和对话里的经验整理成结构化知识，减少重复踩坑。  
作为开源爱好者，我会把能公开的模板、流程和思路持续沉淀在这里。  
这个站点会优先更新“可复制、可落地”的内容，而不是只讲概念。

<!-- TODO: Gary 填写真实自我介绍 -->

## 板块导航

<div class="card-grid">

<a class="card" href="blog/">
  <div class="card-icon">📝</div>
  <div class="card-title">博客</div>
  <div class="card-desc">小红书热帖文字版、AI 热点解读、实操教程</div>
</a>

<a class="card" href="prompts/">
  <div class="card-icon">💡</div>
  <div class="card-title">Prompt 库</div>
  <div class="card-desc">精心调试的 Prompt 合集，覆盖编程 / 写作 / 研究</div>
</a>

<a class="card" href="skills/">
  <div class="card-icon">🛠️</div>
  <div class="card-title">Skills 库</div>
  <div class="card-desc">Claude Skills 和自动化工作流模板</div>
</a>

<a class="card" href="toolbox/">
  <div class="card-icon">🧰</div>
  <div class="card-title">工具箱</div>
  <div class="card-desc">AI 工具推荐、平台对比、工作流搭建</div>
</a>

<a class="card" href="projects/">
  <div class="card-icon">🚀</div>
  <div class="card-title">项目</div>
  <div class="card-desc">开源项目展示：TrendR、OpenClaw 等</div>
</a>

<a class="card" href="ideas/">
  <div class="card-icon">💭</div>
  <div class="card-title">Ideas</div>
  <div class="card-desc">实验性想法和探索记录</div>
</a>

</div>

!!! info "为什么做这个 Wiki"
    - 小红书有字数限制，很多干货只能做成图片。
    - 图片里的代码和 Prompt 没法复制，读者体验会被打断。
    - 我想把优质内容结构化、开源出来，方便持续迭代。
    - 这里的内容都尽量做到“看完就能复制使用”。

## 最近更新

| 日期 | 内容 | 板块 |
|------|------|------|
| 2026-04-07 | [一个 Prompt + 工具清单，搭建 Karpathy 本地知识库](blog/posts/2026-04-07-karpathy-knowledge-base.md) | 博客 |
| 2026-04-04 | [OpenClaw 新手到高阶全攻略](blog/posts/ope.md) | 博客 |
| 2026-04-01 | [DeepSeek API 完全使用指南](blog/posts/2026-04-01-deepseek-api-guide.md) | 博客 |
| 2026-03-25 | [Claude Code 进阶使用技巧](blog/posts/2026-03-25-claude-code-tips.md) | 博客 |
| 2026-03-10 | [Claude Code 泄漏版：智能体长期记忆与自我进化](blog/posts/2026-03-10-prompt-engineering-101.md) | 博客 |
| 2026-04-06 | [代码审查 Prompt](prompts/coding/code-review-prompt.md) | Prompt 库 |
| 2026-04-05 | [小红书知识卡片生成器](skills/templates/xhs-card-generator.md) | Skills 库 |

<!-- TODO: 后续可以用插件自动生成 -->

## 统计与链接

- 内容统计：`5` 篇博客 / `4` 个 Prompts / `2` 个 Skills
- GitHub Star：
  [![GitHub Repo stars](https://img.shields.io/github/stars/gy-hou/publicwiki?style=for-the-badge&logo=github)](https://github.com/gy-hou/publicwiki)
- RSS 订阅：[:material-rss: feed_rss_created.xml](https://gy-hou.github.io/publicwiki/feed_rss_created.xml)
- 贡献内容：[查看 CONTRIBUTING.md](https://github.com/gy-hou/publicwiki/blob/main/CONTRIBUTING.md)

<div class="repo-card-row">
<div class="repo-card">
<a href="https://github.com/gy-hou/publicwiki" target="_blank" rel="noopener noreferrer">
<img class="gh-card-img" src="https://gh-card.dev/repos/gy-hou/publicwiki.svg" alt="gy-hou/publicwiki">
</a>
</div>
<div class="repo-card">
<a href="https://www.xiaohongshu.com/discovery/item/69d27fe6000000002103823e" target="_blank" rel="noopener noreferrer">
<div class="xhs-note-card">
  <div class="xhs-note-header">
    <span class="xhs-badge">
      <svg class="xhs-badge-icon" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg"><rect width="18" height="18" rx="4" fill="#FF2442"/><text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei',sans-serif" font-size="7" font-weight="bold" fill="white">书</text></svg>
      小红书
    </span>
    <span class="xhs-note-title">一个命令和工具清单实现Karpathy本地知识库</span>
  </div>
  <p class="xhs-note-desc">把工具清单和 Prompt 直接复制发给你的 Claude Code / Codex 就能开搭</p>
  <div class="xhs-note-stats">
    <span class="xhs-stat">
      <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
      294
    </span>
    <span class="xhs-stat">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" xmlns="http://www.w3.org/2000/svg"><path d="M5 5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16l-7-3.5L5 21V5z"/></svg>
      650
    </span>
  </div>
</div>
</a>
</div>
</div>

## 🏷️ 热门标签

[:material-tag: prompt](tags.md){ .md-tag }
[:material-tag: Claude](tags.md){ .md-tag }
[:material-tag: 教程](tags.md){ .md-tag }
[:material-tag: Claude Code](tags.md){ .md-tag }
[:material-tag: skill](tags.md){ .md-tag }
[:material-tag: 编程](tags.md){ .md-tag }
[:material-tag: DeepSeek](tags.md){ .md-tag }
[:material-tag: 写作](tags.md){ .md-tag }
