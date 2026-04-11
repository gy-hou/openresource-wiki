---
tags:
  - 项目
  - 开源
  - MkDocs
---

# OpenResource Wiki

> 你正在看的这个站点 — AI 工具、提示词库与技能库的开源知识站

![OpenResource Wiki Hero](../assets/images/projects/openresource-wiki.svg){ .project-hero }

## 要解决的问题

小红书有字数和格式限制，很多干货只能做成图片，读者没法复制代码和 Prompt。好内容值得结构化，图片里的信息检索不到，不方便二次传播。

## 做了什么

- 搭建了基于 MkDocs Material 的完整 Wiki 站点
- 实现了博客系统（RSS、归档、分类、标签）
- 建立了提示词库和技能库，所有内容可搜索、可复制
- 集成了 AI 聊天助手（Cloudflare Worker + Claude API）
- 自动化 SEO（Open Graph、Twitter Card、RSS）
- 支持深色模式、移动端适配

## 技术栈

<div class="md-tags">
  <span class="md-tag">MkDocs</span>
  <span class="md-tag">Material for MkDocs</span>
  <span class="md-tag">GitHub Pages</span>
  <span class="md-tag">Jinja2</span>
  <span class="md-tag">Custom CSS</span>
  <span class="md-tag">Cloudflare Worker</span>
  <span class="md-tag">Claude API</span>
  <span class="md-tag">GitHub Actions</span>
</div>

## 当前进度

| 模块 | 状态 |
|------|------|
| 博客系统 | 🟢 运行中 |
| 提示词库 | 🟢 7+ prompts |
| 技能库 | 🟢 4+ skills |
| 工具库 | 🟢 可用 |
| AI 聊天助手 | 🟢 可用 |
| 邮箱订阅 | 🟢 Buttondown 集成 |
| 评论系统 | 🔴 待接入 |

## Repo

[:material-github: gy-hou/openresource-wiki](https://github.com/gy-hou/openresource-wiki){ .md-button }

## 下一步

- [ ] 接入评论系统（GitHub Discussions / Giscus）
- [ ] 增加更多原创提示词与技能模板
- [ ] 国际化（英文版）
- [ ] 访问统计（Google Analytics / Umami）

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
