---
tags:
  - 项目
  - 开源
  - MkDocs
---

# Openresource-Wiki

> 你正在看的这个站点 — AI 工具、Prompts、Skills 的开源分享站

## 要解决的问题

小红书有字数和格式限制，很多干货只能做成图片，读者没法复制代码和 Prompt。好内容值得结构化，图片里的信息检索不到，不方便二次传播。

## 做了什么

- 搭建了基于 MkDocs Material 的完整 Wiki 站点
- 实现了博客系统（RSS、归档、分类、标签）
- 建立了 Prompt 库和 Skills 库，所有内容可搜索、可复制
- 集成了 AI 聊天助手（Cloudflare Worker + Claude API）
- 自动化 SEO（Open Graph、Twitter Card、RSS）
- 支持深色模式、移动端适配

## 技术栈

| 层级 | 技术 |
|------|------|
| 框架 | MkDocs + Material |
| 部署 | GitHub Pages |
| 模板 | Jinja2 |
| 样式 | 自定义 CSS |
| AI 聊天 | Cloudflare Worker + Claude API |
| CI/CD | GitHub Actions |

## 当前进度

| 模块 | 状态 |
|------|------|
| 博客系统 | 🟢 运行中 |
| Prompt 库 | 🟢 7+ prompts |
| Skills 库 | 🟢 4+ skills |
| 工具箱 | 🟢 可用 |
| AI 聊天助手 | 🟢 可用 |
| Newsletter | 🟢 Buttondown 集成 |
| 评论系统 | 🔴 待接入 |

## Repo

[:material-github: gy-hou/openresource-wiki](https://github.com/gy-hou/openresource-wiki){ .md-button }

## 下一步

- [ ] 接入评论系统（GitHub Discussions / Giscus）
- [ ] 增加更多原创 Prompts 和 Skills
- [ ] 国际化（英文版）
- [ ] 访问统计（Google Analytics / Umami）
