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
    def xhs_profile(name, xhs_id, fans=0, likes_total=0, desc=""):
        """小红书主页 profile 卡片."""
        desc_line = desc if desc else f"{fans} 粉丝 · {likes_total} 获赞与收藏"
        return f"""<div class="repo-card">
<a href="https://www.xiaohongshu.com/user/profile/{xhs_id}" target="_blank" rel="noopener noreferrer">
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
        """GitHub 用户统计卡片 (light/dark)."""
        return f"""<div class="repo-card">
<a href="https://github.com/{username}" target="_blank" rel="noopener noreferrer">
<img class="gh-card-img gh-stats-light" src="{vercel_url}/api/?username={username}&theme=default&show_icons=true" alt="{username} GitHub stats">
<img class="gh-card-img gh-stats-dark" src="{vercel_url}/api/?username={username}&theme=dark&show_icons=true" alt="{username} GitHub stats">
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
