# AI Wiki — 总体计划

> 本文件是所有执行方案的索引和架构决策记录。具体 Codex prompt 见各 Phase 文件。

## 核心决策

| 决策项 | 结论 |
|--------|------|
| 技术栈 | MkDocs + Material for MkDocs |
| 部署方式 | GitHub Pages (子路径) |
| 访问地址 | `https://gy-hou.github.io/publicwiki/` |
| GitHub 仓库名 | `publicwiki`（仓库名决定子路径，需要在 GitHub 上创建为 `publicwiki`）|
| Blog 管理 | 使用 Material 内置 blog plugin（自动分页、RSS、归档）|
| 多语言 | 暂不支持，后续再加 |
| 内容策略 | 全部先用模板占位，后续替换真实内容 |
| 评论系统 | Giscus（基于 GitHub Discussions）|
| Projects 板块 | 先留空壳，内容后填 |

## 架构图

```
gy-hou.github.io (学术主站)
└── /publicwiki/  ← 本项目，独立仓库 "publicwiki"
    ├── /             首页
    ├── /blog/        博客帖子（Material blog plugin 管理）
    ├── /prompts/     Prompt 库
    ├── /skills/      Claude Skills 库
    ├── /toolbox/     工具推荐
    ├── /projects/    项目展示（OpenClaw / TrendR 等）
    ├── /ideas/       实验性想法
    ├── /about/       关于 & 路线图
    └── /tags/        标签索引
```

## 与原方案的关键变化

1. **posts → blog**：用 Material blog plugin 替代手动 posts 目录，获得自动分页 / RSS / 归档 / 摘要
2. **sub-path 部署**：`site_url` 设为 `https://gy-hou.github.io/publicwiki/`，`use_directory_urls: true`
3. **去掉 i18n**：减少首次交付复杂度
4. **增加 Makefile**：本地开发命令统一入口
5. **CI 增强**：除部署外增加 markdown lint + link check
6. **requirements.txt pin 版本**：避免构建不可复现

## 执行文件索引

| 文件 | 内容 | Codex prompts |
|------|------|---------------|
| [PHASE-0-SCAFFOLD.md](PHASE-0-SCAFFOLD.md) | 项目骨架：mkdocs.yml、目录、CI、Makefile | 3 个 prompt |
| [PHASE-1-DESIGN.md](PHASE-1-DESIGN.md) | 视觉设计：CSS、首页、模板系统 | 3 个 prompt |
| [PHASE-2-CONTENT.md](PHASE-2-CONTENT.md) | 占位内容填充：blog/prompts/skills/toolbox/projects | 5 个 prompt |
| [PHASE-3-FEATURES.md](PHASE-3-FEATURES.md) | 高级功能：blog plugin、Giscus、标签、SEO | 4 个 prompt |
| [PHASE-4-TOOLING.md](PHASE-4-TOOLING.md) | 工程工具：OCR 脚本、lint 脚本、CI workflow | 3 个 prompt |
| [PHASE-5-POLISH.md](PHASE-5-POLISH.md) | 最终打磨：404、验证、文档 | 2 个 prompt |

## 执行顺序

```
Phase 0 (骨架) → Phase 1 (设计) → Phase 2 (内容) → Phase 3 (功能) → Phase 4 (工具) → Phase 5 (打磨)
```

每个 Phase 内的 prompt **按顺序执行**，Phase 之间也按顺序。共 **20 个 prompt**。

## Codex 完成后你需要手动做的事

1. 在 GitHub 上创建仓库名为 `publicwiki`
2. 填写 `mkdocs.yml` 中的 `repo_url`
3. 去 https://giscus.app/ 获取 Giscus 配置值并填入
4. 替换 favicon、logo、og 图片
5. 选择 License（MIT 或 CC BY-SA 4.0）
6. 用真实内容替换所有模板占位（搜索 `<!-- TODO` 即可找到）
7. 在仓库 Settings → Pages 中启用 GitHub Pages（source: gh-pages branch）
