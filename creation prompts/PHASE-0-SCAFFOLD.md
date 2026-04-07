# Phase 0: 项目骨架搭建

> 本阶段创建项目的全部基础设施：配置文件、目录结构、CI/CD、开发工具。
> 完成后应能 `make serve` 本地预览一个空壳 Wiki。

---

## Prompt 0.1 — 初始化 MkDocs 项目 + 目录结构

```
你是一个高级全栈工程师。请在当前仓库根目录初始化一个完整的 MkDocs 项目。

## 技术栈
MkDocs + Material for MkDocs + Material Blog Plugin + GitHub Pages

## 关键约束
- 部署地址：https://gy-hou.github.io/publicwiki/
- 仓库名：publicwiki
- 语言：中文（zh）
- 不需要 i18n 插件

## 1. mkdocs.yml 完整配置

```yaml
site_name: "AI Wiki"
site_url: https://gy-hou.github.io/publicwiki/
site_author: gy-hou
site_description: "AI 工具、Prompts、Skills 开源分享 | 小红书同名博主"
repo_name: gy-hou/publicwiki
repo_url: https://github.com/gy-hou/publicwiki
edit_uri: edit/main/docs/
use_directory_urls: true

theme:
  name: material
  language: zh
  custom_dir: overrides
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.top
    - navigation.tracking
    - navigation.indexes
    - navigation.footer
    - search.highlight
    - search.suggest
    - search.share
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - content.action.edit
    - toc.follow
    - announce.dismiss
  palette:
    - scheme: default
      primary: deep purple
      accent: amber
      toggle:
        icon: material/brightness-7
        name: 切换到深色模式
    - scheme: slate
      primary: deep purple
      accent: amber
      toggle:
        icon: material/brightness-4
        name: 切换到浅色模式
  font:
    text: Noto Sans SC
    code: JetBrains Mono
  icon:
    repo: fontawesome/brands/github
    edit: material/pencil
    view: material/eye
    logo: material/robot-happy-outline
  favicon: assets/images/favicon.ico

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_mermaid
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.mark
  - pymdownx.critic
  - pymdownx.keys
  - pymdownx.snippets
  - attr_list
  - md_in_html
  - tables
  - footnotes
  - def_list
  - toc:
      permalink: true
      toc_depth: 3

plugins:
  - search:
      separator: '[\s\u200b\-\,\.\，\。\？\！\；\：]'
  - tags:
      tags_file: tags.md
  - blog:
      blog_dir: blog
      blog_toc: true
      post_date_format: yyyy-MM-dd
      post_url_format: "{slug}"
      post_excerpt: optional
      post_excerpt_separator: <!-- more -->
      categories: true
      categories_name: 分类
      categories_url_format: "category/{slug}"
      archive: true
      archive_name: 归档
      archive_url_format: "archive/{date}"
      archive_date_format: yyyy
      pagination: true
      pagination_per_page: 10
      authors: true
  - git-revision-date-localized:
      enable_creation_date: true
      type: date
      fallback_to_build_date: true

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/gy-hou
      name: GitHub
    - icon: simple/xiaohongshu
      link: "#"
      name: 小红书
  # analytics:
  #   provider: google
  #   property: G-XXXXXXXXXX
  generator: false

extra_css:
  - assets/stylesheets/extra.css

extra_javascript:
  - assets/javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

copyright: Copyright &copy; 2025-2026 gy-hou | CC BY-SA 4.0

nav:
  - 首页: index.md
  - 博客:
    - blog/index.md
  - Prompt 库:
    - prompts/index.md
    - 编程:
      - prompts/coding/index.md
    - 写作:
      - prompts/writing/index.md
    - 研究:
      - prompts/research/index.md
    - System Prompts:
      - prompts/system/index.md
  - Skills 库:
    - skills/index.md
    - 模板:
      - skills/templates/index.md
  - 工具箱:
    - toolbox/index.md
    - AI 平台:
      - toolbox/ai-platforms/index.md
    - 开发工具:
      - toolbox/dev-tools/index.md
    - 工作流:
      - toolbox/workflows/index.md
  - 项目:
    - projects/index.md
  - Ideas:
    - ideas/index.md
  - 关于:
    - about/index.md
    - 路线图: about/roadmap.md
  - 标签: tags.md
```

## 2. 创建以下完整目录结构

每个 index.md 文件写 1-2 句中文占位说明（不要留空）。

```
docs/
├── index.md                           # 首页（写"欢迎来到 AI Wiki"占位）
├── tags.md                            # 标签索引页，内容只写 [TAGS]
├── blog/
│   ├── index.md                       # Blog 首页（blog plugin 会自动管理）
│   ├── .authors.yml                   # 作者信息文件
│   └── posts/                         # Blog 文章存放目录（blog plugin 要求）
│       └── .gitkeep
├── prompts/
│   ├── index.md                       # "这里收录了各类精心调试的 Prompt"
│   ├── coding/
│   │   └── index.md                   # "编程相关的 Prompt 集合"
│   ├── writing/
│   │   └── index.md                   # "写作辅助 Prompt 集合"
│   ├── research/
│   │   └── index.md                   # "学术研究相关 Prompt 集合"
│   └── system/
│       └── index.md                   # "System Prompt 设计参考"
├── skills/
│   ├── index.md                       # "Claude Skills 和自动化工作流收录"
│   └── templates/
│       └── index.md                   # "可直接复用的 Skill 模板"
├── toolbox/
│   ├── index.md                       # "AI 工具推荐和使用心得"
│   ├── ai-platforms/
│   │   └── index.md                   # "主流 AI 平台对比与推荐"
│   ├── dev-tools/
│   │   └── index.md                   # "开发者工具推荐"
│   └── workflows/
│       └── index.md                   # "高效工作流搭建指南"
├── projects/
│   └── index.md                       # "我的开源项目展示"
├── ideas/
│   └── index.md                       # "一些实验性的想法和探索"
├── about/
│   ├── index.md                       # "关于我"占位
│   └── roadmap.md                     # "更新路线图"占位
├── assets/
│   ├── images/
│   │   └── .gitkeep
│   ├── stylesheets/
│   │   └── extra.css                  # 空文件，Phase 1 填充
│   └── javascripts/
│       └── mathjax.js                 # MathJax 配置
└── _templates/                        # 内容模板（不被 MkDocs 构建）
    └── .gitkeep
```

## 3. blog/.authors.yml 内容

```yaml
authors:
  gy-hou:
    name: gy-hou
    description: AI 工具深度用户 | 小红书博主
    avatar: https://github.com/gy-hou.png
```

## 4. docs/assets/javascripts/mathjax.js 内容

```javascript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise()
})
```

## 5. 创建以下根目录文件

### requirements.txt
```
mkdocs-material==9.6.7
mkdocs-git-revision-date-localized-plugin==1.4.5
```

### .gitignore
```
site/
__pycache__/
*.pyc
.DS_Store
.venv/
.env
node_modules/
*.egg-info/
dist/
build/
.cache/
```

### README.md
```markdown
# AI Wiki

AI 工具、Prompts、Skills 开源分享站。

**在线访问**：https://gy-hou.github.io/publicwiki/

## 本地开发

​```bash
# 安装依赖
pip install -r requirements.txt

# 本地预览
mkdocs serve

# 构建
mkdocs build
​```

## License

<!-- TODO: 选择 MIT 或 CC BY-SA 4.0 -->
```

## 6. 验证

创建完所有文件后，确保：
- 所有 index.md 都有内容（不是空文件）
- mkdocs.yml 语法正确（可以被 YAML parser 解析）
- nav 中引用的每个文件都存在
- 没有多余的文件被遗漏

不要安装任何包，只创建文件。
```

---

## Prompt 0.2 — GitHub Actions + CI

```
在当前仓库创建 CI/CD 配置。

## 1. 部署工作流 `.github/workflows/deploy.yml`

```yaml
name: Deploy Wiki

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # git-revision-date 插件需要完整历史

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build site
        run: mkdocs build --strict

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
```

## 2. 内容检查工作流 `.github/workflows/lint.yml`

```yaml
name: Content Check

on:
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build check (strict mode)
        run: mkdocs build --strict

      - name: Check for broken internal links
        run: |
          # 简单检查：确保 nav 中所有引用的 md 文件都存在
          python -c "
          import yaml, os, sys
          with open('mkdocs.yml') as f:
              config = yaml.safe_load(f)
          def extract_paths(nav, paths=None):
              if paths is None: paths = []
              if isinstance(nav, list):
                  for item in nav:
                      extract_paths(item, paths)
              elif isinstance(nav, dict):
                  for v in nav.values():
                      extract_paths(v, paths)
              elif isinstance(nav, str):
                  paths.append(nav)
              return paths
          paths = extract_paths(config.get('nav', []))
          missing = [p for p in paths if not os.path.exists(f'docs/{p}')]
          if missing:
              print('Missing files referenced in nav:')
              for m in missing: print(f'  - docs/{m}')
              sys.exit(1)
          print(f'All {len(paths)} nav references OK')
          "
```

## 3. Issue 模板 `.github/ISSUE_TEMPLATE/content-request.md`

```markdown
---
name: 内容请求
about: 请求添加新的 Prompt、教程、工具推荐等内容
title: '[内容请求] '
labels: ['content-request']
assignees: ''
---

## 请求类型

- [ ] Prompt
- [ ] 教程 / 帖子
- [ ] 工具推荐
- [ ] Claude Skill
- [ ] 其他

## 详细描述

请描述你希望看到的内容：

## 参考链接

如果有相关资源，请贴在这里：

## 优先级

- [ ] 高（很多人需要）
- [ ] 中（有用但不紧急）
- [ ] 低（锦上添花）
```

## 4. Issue 模板 `.github/ISSUE_TEMPLATE/bug-report.md`

```markdown
---
name: Bug 报告
about: 网站显示问题、链接失效等
title: '[Bug] '
labels: ['bug']
assignees: ''
---

## 问题描述

## 页面链接

## 截图（可选）

## 浏览器 / 设备
```

确保所有 YAML 文件语法正确。
```

---

## Prompt 0.3 — Makefile + 开发工具

```
创建开发工具文件，统一本地开发命令。

## 1. Makefile

```makefile
.PHONY: serve build clean install lint new-post help

# 默认目标
help:  ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	pip install -r requirements.txt

serve:  ## 本地预览（热重载）
	mkdocs serve --open

build:  ## 构建静态站点
	mkdocs build --strict

clean:  ## 清理构建产物
	rm -rf site/

lint:  ## 检查内容健康度
	python scripts/lint_content.py --docs-dir docs/

new-post:  ## 创建新博客文章 (usage: make new-post TITLE="文章标题")
	@if [ -z "$(TITLE)" ]; then echo "Usage: make new-post TITLE=\"文章标题\""; exit 1; fi
	@DATE=$$(date +%Y-%m-%d); \
	SLUG=$$(echo "$(TITLE)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-'); \
	FILE="docs/blog/posts/$${DATE}-$${SLUG}.md"; \
	echo "---" > $$FILE; \
	echo "date: $${DATE}" >> $$FILE; \
	echo "authors:" >> $$FILE; \
	echo "  - gy-hou" >> $$FILE; \
	echo "categories:" >> $$FILE; \
	echo "  - 待分类" >> $$FILE; \
	echo "tags:" >> $$FILE; \
	echo "  - 待填写" >> $$FILE; \
	echo "---" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "# $(TITLE)" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "<!-- more -->" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "正文内容..." >> $$FILE; \
	echo "Created: $$FILE"

deploy:  ## 手动部署（通常用 CI 自动部署）
	mkdocs gh-deploy --force
```

## 2. .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
indent_size = 4

[Makefile]
indent_style = tab
```

## 3. 更新 README.md

在 README.md 的"本地开发"部分，改为使用 Makefile 命令：

```markdown
## 本地开发

​```bash
# 安装依赖
make install

# 本地预览（自动打开浏览器）
make serve

# 构建
make build

# 创建新博客文章
make new-post TITLE="我的新文章"

# 查看所有可用命令
make help
​```
```

确保 Makefile 使用 tab 缩进（不是空格）。
```

---

## 本阶段完成标准

- [ ] `mkdocs.yml` 存在且语法正确
- [ ] 所有 `docs/` 下的 index.md 都有内容
- [ ] `requirements.txt` 有 pinned 版本
- [ ] `.github/workflows/deploy.yml` 存在
- [ ] `.github/workflows/lint.yml` 存在
- [ ] `Makefile` 存在，`make help` 能列出命令
- [ ] `.gitignore` 存在
- [ ] `README.md` 存在
- [ ] `overrides/` 目录存在
