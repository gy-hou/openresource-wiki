# Codex 执行顺序速查

> 按顺序将每个 prompt 发给 Codex 执行。每个 prompt 独立，跑完一个再发下一个。

## 总览：20 个 Prompt

| # | Phase | Prompt | 做什么 |
|---|-------|--------|--------|
| 1 | 0.1 | PHASE-0 | 初始化 MkDocs 项目 + 全部目录结构 |
| 2 | 0.2 | PHASE-0 | GitHub Actions (deploy + lint) + Issue 模板 |
| 3 | 0.3 | PHASE-0 | Makefile + .editorconfig + README 更新 |
| 4 | 1.1 | PHASE-1 | 自定义 CSS 样式 |
| 5 | 1.2 | PHASE-1 | 首页设计 |
| 6 | 1.3 | PHASE-1 | 内容模板 + CONTRIBUTING.md |
| 7 | 2.1 | PHASE-2 | 5 篇 Blog 占位文章 |
| 8 | 2.2 | PHASE-2 | 4 个 Prompt 模板页面 |
| 9 | 2.3 | PHASE-2 | 2 个 Skill 模板页面 |
| 10 | 2.4 | PHASE-2 | 3 个工具箱模板页面 |
| 11 | 2.5 | PHASE-2 | Projects / Ideas / About / Roadmap |
| 12 | 3.1 | PHASE-3 | Giscus 评论系统 |
| 13 | 3.2 | PHASE-3 | 标签系统优化 |
| 14 | 3.3 | PHASE-3 | SEO + OG tags + robots.txt |
| 15 | 3.4 | PHASE-3 | RSS 订阅 |
| 16 | 4.1 | PHASE-4 | OCR → Markdown 脚本 |
| 17 | 4.2 | PHASE-4 | 内容 lint 脚本 |
| 18 | 4.3 | PHASE-4 | CI 增强 lint workflow |
| 19 | 5.1 | PHASE-5 | 404 + LICENSE + README 完善 |
| 20 | 5.2 | PHASE-5 | 全面验证和修复 |

## 执行方法

1. 打开对应的 Phase 文件
2. 复制 ` ``` ` 包裹的 prompt 文本
3. 发给 Codex 执行
4. 等待完成后，发下一个

## 注意

- Phase 0 必须最先完成（后续都依赖它的目录结构）
- Phase 内的 prompt 按顺序执行
- Phase 2 的内容后续由 Gary 替换为真实内容
- 所有 `<!-- TODO -->` 标记的位置需要手动填写
