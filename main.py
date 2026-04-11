"""MkDocs Macros — reusable card components."""


def define_env(env):
    """Register Jinja2 macros for card widgets."""

    @env.macro
    def xhs_note(title, url, likes=0, favorites=0, desc=""):
        """小红书笔记卡片."""
        fav_display = favorites if favorites else "—"
        desc_html = f'<p class="xhs-note-desc">{desc}</p>' if desc else ""
        return f"""<div class="repo-card">
<a href="{url}" target="_blank" rel="noopener noreferrer">
<div class="xhs-note-card">
  <div class="xhs-note-header">
    <span class="xhs-badge">
      <svg class="xhs-badge-icon" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg"><rect width="18" height="18" rx="4" fill="#FF2442"/><text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei',sans-serif" font-size="7" font-weight="bold" fill="white">书</text></svg>
      小红书
    </span>
    <span class="xhs-note-title">{title}</span>
  </div>
  {desc_html}
  <div class="xhs-note-stats">
    <span class="xhs-stat">
      <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
      {likes}
    </span>
    <span class="xhs-stat">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" xmlns="http://www.w3.org/2000/svg"><path d="M5 5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16l-7-3.5L5 21V5z"/></svg>
      {fav_display}
    </span>
  </div>
</div>
</a>
</div>"""

    @env.macro
    def xhs_profile(name, xhs_id, fans=0, likes_total=0, desc="", url=""):
        """小红书主页 profile 卡片."""
        desc_line = desc if desc else f"{fans} 粉丝 · {likes_total} 获赞与收藏"
        href = url if url else f"https://www.xiaohongshu.com/user/profile/{xhs_id}"
        return f"""<div class="repo-card">
<a href="{href}" target="_blank" rel="noopener noreferrer">
<div class="xhs-card">
  <div class="xhs-card-inner">
    <div class="xhs-logo-area">
      <svg class="xhs-icon" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="10" fill="#FF2442"/><text x="50%" y="56%" dominant-baseline="middle" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei',sans-serif" font-size="13" font-weight="bold" fill="white">小红书</text></svg>
    </div>
    <div class="xhs-info">
      <div class="xhs-platform">小红书</div>
      <div class="xhs-username">@{name}</div>
      <div class="xhs-desc">{desc_line}</div>
    </div>
    <div class="xhs-arrow">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </div>
  </div>
</div>
</a>
</div>"""

    @env.macro
    def github_stats(username, vercel_url="https://github-readme-stats-ten-mu-29.vercel.app"):
        """GitHub 主页卡片（profile card 样式）."""
        return f"""<div class="repo-card">
<a href="https://github.com/{username}" target="_blank" rel="noopener noreferrer">
<div class="gh-profile-card">
  <div class="gh-profile-inner">
    <div class="gh-logo-area">
      <svg class="gh-icon" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="10" fill="#24292f"/><path d="M20 8a12 12 0 0 0-3.79 23.4c.6.1.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61a3.18 3.18 0 0 0-1.33-1.76c-1.09-.74.08-.73.08-.73a2.52 2.52 0 0 1 1.84 1.24 2.56 2.56 0 0 0 3.5 1 2.56 2.56 0 0 1 .76-1.6c-2.67-.3-5.47-1.33-5.47-5.93a4.64 4.64 0 0 1 1.24-3.22 4.3 4.3 0 0 1 .12-3.18s1-.32 3.3 1.23a11.38 11.38 0 0 1 6.01 0c2.3-1.55 3.3-1.23 3.3-1.23a4.3 4.3 0 0 1 .12 3.18 4.64 4.64 0 0 1 1.23 3.22c0 4.61-2.8 5.63-5.48 5.92a2.87 2.87 0 0 1 .82 2.23v3.29c0 .32.21.7.82.58A12 12 0 0 0 20 8z" fill="white"/></svg>
    </div>
    <div class="gh-info">
      <div class="gh-platform">GitHub</div>
      <div class="gh-username">@{username}</div>
    </div>
    <div class="gh-arrow">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </div>
  </div>
</div>
</a>
</div>"""

    @env.macro
    def github_repo(repo, vercel_url="https://github-readme-stats-ten-mu-29.vercel.app"):
        """GitHub 仓库 pin 卡片 (light/dark)."""
        owner, name = repo.split("/", 1)
        return f"""<div class="repo-card">
<a href="https://github.com/{repo}" target="_blank" rel="noopener noreferrer">
<img class="gh-card-img gh-stats-light" src="{vercel_url}/api/pin/?username={owner}&repo={name}&theme=default&show_icons=true" alt="{repo}">
<img class="gh-card-img gh-stats-dark" src="{vercel_url}/api/pin/?username={owner}&repo={name}&theme=dark&show_icons=true" alt="{repo}">
</a>
</div>"""

    @env.macro
    def card_row(*cards):
        """Wrap multiple cards in a flex row."""
        return '<div class="repo-card-row">\n' + "\n".join(cards) + "\n</div>"

    @env.macro
    def featured(items):
        """Featured carousel. items = list of (title, url, cover_slug).
        cover_slug maps to assets/images/blog/covers/{slug}.jpg"""
        cards = []
        fallback_colors = ["blue", "green", "purple", "orange", "teal"]
        for i, item in enumerate(items):
            title, url = item[0], item[1]
            slug = item[2] if len(item) > 2 else None
            # Try cover image first, fall back to gradient
            if slug and not slug in ("blue", "green", "purple", "orange", "teal"):
                style = (
                    f'background-image: url(\"assets/images/blog/covers/{slug}.jpg\");'
                    f'background-size: cover; background-position: center;'
                )
                cards.append(
                    f'<a class="featured-card" style=\'{style}\' href="{url}">'
                    f'<div class="featured-card-title">{title}</div></a>'
                )
            else:
                color = slug if slug in ("blue", "green", "purple", "orange", "teal") else fallback_colors[i % 5]
                cards.append(
                    f'<a class="featured-card featured-card--{color}" href="{url}">'
                    f'<div class="featured-card-title">{title}</div></a>'
                )
        script = (
            '<script>'
            'document.addEventListener("DOMContentLoaded",function(){'
            'document.querySelectorAll(".featured-wrapper").forEach(function(w){'
            'var c=w.querySelector(".featured-carousel");'
            'var prev=w.querySelector(".featured-nav--prev");'
            'var next=w.querySelector(".featured-nav--next");'
            'if(!c||!prev||!next)return;'
            'function step(){var card=c.querySelector(".featured-card");'
            'return card?card.offsetWidth+16:300}'
            'prev.addEventListener("click",function(){c.scrollBy({left:-step(),behavior:"smooth"})});'
            'next.addEventListener("click",function(){c.scrollBy({left:step(),behavior:"smooth"})});'
            '})});'
            '</script>'
        )
        return (
            '<div class="featured-wrapper">\n'
            '<button class="featured-nav featured-nav--prev" aria-label="上一组" type="button">&#8249;</button>\n'
            '<div class="featured-carousel">\n'
            + "\n".join(cards)
            + '\n</div>\n'
            '<button class="featured-nav featured-nav--next" aria-label="下一组" type="button">&#8250;</button>\n'
            '</div>\n'
            + script
        )

    @env.macro
    def blog_cover(slug):
        """Blog post cover image, shown at bottom of post."""
        return (
            f'<div class="blog-cover">'
            f'<img src="/assets/images/blog/covers/{slug}.jpg" alt="cover" loading="lazy">'
            f'</div>'
        )

    @env.macro
    def prompt(content, tag="System Prompt"):
        """炫酷的 Prompt 展示块，带一键复制."""
        # 转义 HTML 字符防止注入，但保留换行
        safe_content = content.replace("<", "&lt;").replace(">", "&gt;")
        return f"""
<div class="prompt-block-enhanced">
  <div class="prompt-header">
    <div class="prompt-tag">
      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      {tag}
    </div>
    <div class="prompt-copy-btn" onclick="copyPrompt(this)" title="复制提示词">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 4v8a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-8a2 2 0 0 0-2 2z"/><path d="M16 18v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2h2"/></svg>
    </div>
  </div>
  <div class="prompt-content">{safe_content}</div>
</div>
"""
