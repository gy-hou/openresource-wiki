# Phase 3: 高级功能

> 本阶段添加评论、标签优化、SEO、和社交分享功能。

---

## Prompt 3.1 — Giscus 评论系统

```
为 Wiki 添加 Giscus 评论系统（基于 GitHub Discussions）。

## 1. 创建 `overrides/partials/comments.html`

```html
{% if page.meta.comments != false %}
<h2 id="__comments">{{ lang.t("meta.comments") }}</h2>

<!-- Giscus 评论系统 -->
<!-- 使用前需要：
     1. 在 GitHub 仓库 Settings → Features 中开启 Discussions
     2. 安装 Giscus App: https://github.com/apps/giscus
     3. 去 https://giscus.app/ 填入仓库信息，获取 data-repo-id 和 data-category-id
     4. 将下方占位值替换为真实值
-->
<script
  src="https://giscus.app/client.js"
  data-repo="gy-hou/publicwiki"
  data-repo-id="<!-- TODO: 在 https://giscus.app/ 获取 -->"
  data-category="Announcements"
  data-category-id="<!-- TODO: 在 https://giscus.app/ 获取 -->"
  data-mapping="pathname"
  data-strict="0"
  data-reactions-enabled="1"
  data-emit-metadata="0"
  data-input-position="top"
  data-theme="preferred_color_scheme"
  data-lang="zh-CN"
  data-loading="lazy"
  crossorigin="anonymous"
  async>
</script>

<!-- 跟随 MkDocs Material 主题切换 -->
<script>
  var giscus = document.querySelector("script[src*=giscus]")

  /* 监听主题切换 */
  var defined = function () {
    return document.querySelector("[data-md-color-scheme]")
  }

  var observer = new MutationObserver(function() {
    var scheme = document.body.getAttribute("data-md-color-scheme")
    var theme = scheme === "slate" ? "dark" : "light"

    /* 通知 Giscus iframe 切换主题 */
    var frame = document.querySelector(".giscus-frame")
    if (frame) {
      frame.contentWindow.postMessage(
        { giscus: { setConfig: { theme: theme } } },
        "https://giscus.app"
      )
    }
  })

  if (defined()) {
    observer.observe(defined(), {
      attributes: true,
      attributeFilter: ["data-md-color-scheme"]
    })
  }
</script>
{% endif %}
```

## 2. 确保 `mkdocs.yml` 中已有 `custom_dir: overrides`

已经在 Phase 0 配置了，确认存在即可。

## 3. 创建 overrides 目录结构

确保以下目录和文件存在（如果还不存在）：
```
overrides/
└── partials/
    └── comments.html
```

## 4. 在 `docs/about/index.md` 底部添加说明

在 About 页面添加一段关于评论系统的说明：
```markdown
## 💬 评论

每个页面底部都有评论区（基于 GitHub Discussions），
欢迎留言讨论！需要 GitHub 账号登录。
```

不需要修改其他文件，Material 主题会自动在每个页面底部加载评论组件。
如果某个页面不想显示评论，在 frontmatter 中添加 `comments: false`。
```

---

## Prompt 3.2 — 标签系统优化

```
优化标签系统和标签索引页。

## 1. 确保 `docs/tags.md` 内容正确

```markdown
---
hide:
  - navigation
  - toc
---

# 标签索引

> 🏷️ 按标签浏览所有内容

[TAGS]
```

## 2. 检查所有内容页面的标签

遍历所有 `docs/` 下的 .md 文件（除了 index.md 和 tags.md），确保：
- 每个内容页面都有 `tags` 字段在 frontmatter 中
- 标签使用统一的命名（中文标签用中文，英文品牌名保持英文）

## 3. 在 `docs/assets/stylesheets/extra.css` 中添加标签相关样式

如果 Phase 1 中还没添加：
```css
/* 标签页面网格布局 */
.md-typeset .md-tags {
  /* 标签列表样式 */
}

/* 标签 pill 样式 */
.md-typeset [data-md-tag] a {
  border-radius: 16px;
  padding: 2px 10px;
  font-size: 0.75rem;
}
```

## 4. 更新首页的"热门标签"区域

在 `docs/index.md` 底部添加或更新"热门标签"：
```markdown
## 🏷️ 热门标签

[:material-tag: Prompt](tags.md#prompt){ .md-tag }
[:material-tag: Claude](tags.md#claude){ .md-tag }
[:material-tag: 教程](tags.md#教程){ .md-tag }
[:material-tag: AI工具](tags.md#ai工具){ .md-tag }
[:material-tag: Skill](tags.md#skill){ .md-tag }
[:material-tag: 编程](tags.md#编程){ .md-tag }
[:material-tag: DeepSeek](tags.md#deepseek){ .md-tag }
[:material-tag: 写作](tags.md#写作){ .md-tag }
```

## 5. 在 `mkdocs.yml` nav 中确保 Tags 页面位置合理

Tags 页面应该在 nav 的最后一项（在"关于"之后）。
```

---

## Prompt 3.3 — SEO 和社交分享

```
优化 Wiki 的 SEO 和社交分享体验。

## 1. 创建 `overrides/main.html`

```html
{% extends "base.html" %}

{% block extrahead %}
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{ page.meta.title or page.title }} - AI Wiki">
  <meta property="og:description" content="{{ page.meta.description or config.site_description }}">
  <meta property="og:url" content="{{ page.canonical_url }}">
  <meta property="og:site_name" content="AI Wiki">
  <meta property="og:image" content="{{ config.site_url }}assets/images/og-default.png">
  <meta property="og:locale" content="zh_CN">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ page.meta.title or page.title }} - AI Wiki">
  <meta name="twitter:description" content="{{ page.meta.description or config.site_description }}">
  <meta name="twitter:image" content="{{ config.site_url }}assets/images/og-default.png">

  <!-- 额外 SEO -->
  <meta name="author" content="gy-hou">
  <link rel="canonical" href="{{ page.canonical_url }}">

  {% if page.meta.date %}
  <meta property="article:published_time" content="{{ page.meta.date }}">
  {% endif %}
{% endblock %}
```

## 2. 创建占位图片

在 `docs/assets/images/` 下创建以下占位文件（用纯文本占位，后续替换为真实图片）：

- `og-default.png` — 创建一个 `og-default.txt` 占位文件，内容说明需要的图片规格：
  ```
  占位文件。请替换为 1200x630 的 OG 分享图片。
  建议包含：站点名称 "AI Wiki"、简短描述、品牌色。
  ```

- `favicon.txt` — 占位文件：
  ```
  占位文件。请替换为 favicon.ico（32x32 或 16x16）。
  ```

- `logo.txt` — 占位文件：
  ```
  占位文件。请替换为导航栏 logo 图片。建议 PNG 格式，白色或透明背景。
  ```

## 3. 添加 sitemap 配置

MkDocs 默认生成 sitemap.xml，确保在 mkdocs.yml 中没有禁用它。
不需要额外配置。

## 4. 添加 robots.txt

创建 `docs/robots.txt`：
```
User-agent: *
Allow: /
Sitemap: https://gy-hou.github.io/publicwiki/sitemap.xml
```

## 5. 更新 mkdocs.yml

在 extra 字段确认以下配置：
```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/gy-hou
      name: GitHub
    - icon: simple/xiaohongshu
      link: "#"  # TODO: 填写小红书链接
      name: 小红书
  generator: false  # 隐藏 "Made with Material for MkDocs"
```

确保 copyright 字段存在：
```yaml
copyright: Copyright &copy; 2025-2026 gy-hou | <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>
```
```

---

## Prompt 3.4 — RSS 订阅

```
为 Blog 添加 RSS 订阅支持。

## 1. 更新 `requirements.txt`

添加：
```
mkdocs-rss-plugin==1.15.0
```

## 2. 在 `mkdocs.yml` plugins 中添加 RSS 插件

```yaml
plugins:
  # ... 已有插件 ...
  - rss:
      match_path: "blog/posts/.*"
      date_from_meta:
        as_creation: date
      categories:
        - categories
        - tags
      image: https://gy-hou.github.io/publicwiki/assets/images/og-default.png
```

注意：RSS plugin 要放在 blog plugin 之后。

## 3. 在首页和 blog 页面添加 RSS 链接

在 `docs/blog/index.md` 顶部添加：
```markdown
[:material-rss: 订阅 RSS](feed_rss_created.xml){ .md-button }
```

在 `docs/index.md` 的底部链接区域也添加 RSS 链接。

## 4. 在 `overrides/main.html` 的 `extrahead` block 中添加

```html
<!-- RSS -->
<link rel="alternate" type="application/rss+xml" title="AI Wiki" href="{{ config.site_url }}feed_rss_created.xml">
```

确保 RSS feed 能正确生成（依赖 blog 文章有正确的 date frontmatter）。
```

---

## 本阶段完成标准

- [ ] Giscus 评论组件文件存在，配置完整（占位值标注清晰）
- [ ] 标签索引页正常工作
- [ ] OG meta tags 在每个页面的 HTML head 中
- [ ] robots.txt 存在
- [ ] RSS 插件配置正确
- [ ] 所有修改不破坏 `mkdocs build --strict`
