---
tags:
  - 项目
  - 开源
  - JavaScript
---

# Advanced Prompts DB

> ChatGPT 高级 Prompt 数据库，一键 Vercel 部署

![Advanced Prompts DB Hero](../assets/images/projects/advanced-prompts-db.svg){ .project-hero }

## 要解决的问题

优质的 ChatGPT Prompt 散落在各个论坛和文档中，缺少一个结构化、可搜索、可自部署的 Prompt 集合。

## 做了什么

- 整理了高质量 ChatGPT Prompt 集合
- 实现了一键 Vercel 部署方案
- 支持搜索、分类浏览
- 提供了中英文双语内容

## 代表 Prompt（节选）

{{ prompt("你是一名资深提示工程师。请将用户目标拆分为：任务定义、输入约束、输出结构、评估标准，并返回可直接执行的高质量 Prompt。", tag="Prompt Builder") }}

{{ prompt("请基于下面代码做严格代码审查，输出：阻断问题、兼容性风险、性能风险、可维护性建议，并给出最小可行修复方案。", tag="Code Review Pro") }}

## 技术栈

<div class="md-tags">
  <span class="md-tag">JavaScript</span>
  <span class="md-tag">Vercel</span>
  <span class="md-tag">JSON</span>
  <span class="md-tag">Markdown</span>
  <span class="md-tag">Prompt Engineering</span>
</div>

## 当前进度

| 模块 | 状态 |
|------|------|
| Prompt 数据库 | 🟢 可用 |
| 搜索功能 | 🟢 可用 |
| 一键部署 | 🟢 可用 |
| 持续更新 | 🟢 活跃 |

## Repo

[:material-github: gy-hou/chatgpt-advanced-prompts](https://github.com/gy-hou/chatgpt-advanced-prompts){ .md-button }

## 下一步

- [ ] 增加更多分类维度
- [ ] 支持用户提交 Prompt
- [ ] 添加 Prompt 效果评分

<div class="blog-share">
  <div class="blog-share-title">分享这个项目</div>
  <div class="blog-share-buttons">
    <a href="#" onclick="return shareToWechat(event);" class="share-btn share-btn--wechat" title="微信分享">
      微信
    </a>
    <a href="https://xhslink.com/m/3lRU7a53RSt" target="_blank" rel="noopener" class="share-btn share-btn--xhs" title="小红书">
      小红书
    </a>
    <a href="https://github.com/gy-hou/openresource-wiki" target="_blank" rel="noopener" class="share-btn share-btn--github" title="GitHub">
      GitHub
    </a>
  </div>
</div>
