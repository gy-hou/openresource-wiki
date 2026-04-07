#!/usr/bin/env python3
"""Auto-extract 2-3 tags for each blog post using DeepSeek API."""

import os
import sys
import json
import re
import urllib.request
import urllib.error

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "blog", "posts")

# Allowed tags (keep consistent across the site)
ALLOWED_TAGS = [
    "Claude Code", "Claude", "DeepSeek", "GPT", "Gemini", "OpenClaw",
    "AI Agent", "API", "Obsidian", "prompt", "skill",
    "知识库", "工作流", "效率", "教程", "编程", "写作", "研究",
    "长期记忆", "自动化", "Fintech", "开源", "工具",
]

SYSTEM_PROMPT = f"""你是一个标签提取助手。给定一篇博客文章的内容，从以下标签列表中选择最匹配的 2-3 个标签。

可选标签：{json.dumps(ALLOWED_TAGS, ensure_ascii=False)}

规则：
- 只从列表中选择，不要发明新标签
- 返回纯 JSON 数组，如 ["Claude Code", "教程", "效率"]
- 选 2-3 个最相关的，不要多选
- 只返回 JSON，不要其他文字"""


def extract_frontmatter(content):
    """Parse YAML frontmatter and body."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]
    # Simple YAML parsing for our needs
    fm = {}
    current_key = None
    current_list = None
    for line in fm_text.strip().split("\n"):
        if line.startswith("  - "):
            if current_list is not None:
                current_list.append(line.strip("  - ").strip())
        elif ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val:
                fm[key] = val
            else:
                current_key = key
                current_list = []
                fm[key] = current_list
    return fm, body


def rebuild_frontmatter(fm, tags, original_content):
    """Replace tags in the original frontmatter."""
    if not original_content.startswith("---"):
        return original_content
    parts = original_content.split("---", 2)
    fm_text = parts[1]
    body = parts[2]

    # Remove existing tags block
    fm_lines = fm_text.strip().split("\n")
    new_lines = []
    skip_tag_items = False
    for line in fm_lines:
        if line.strip() == "tags:":
            skip_tag_items = True
            continue
        if skip_tag_items:
            if line.startswith("  - "):
                continue
            else:
                skip_tag_items = False
        new_lines.append(line)

    # Add new tags
    new_lines.append("tags:")
    for t in tags:
        new_lines.append(f"  - {t}")

    return "---\n" + "\n".join(new_lines) + "\n---" + body


def call_deepseek(api_key, content_snippet):
    """Call DeepSeek API to extract tags."""
    # Truncate to ~2000 chars to save tokens
    snippet = content_snippet[:2000]
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": snippet},
        ],
        "max_tokens": 100,
        "temperature": 0.3,
    }).encode()

    req = urllib.request.Request(
        DEEPSEEK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        reply = data["choices"][0]["message"]["content"].strip()
        # Parse JSON array from reply
        match = re.search(r'\[.*?\]', reply, re.DOTALL)
        if match:
            tags = json.loads(match.group())
            # Filter to allowed tags
            return [t for t in tags if t in ALLOWED_TAGS][:3]
    except Exception as e:
        print(f"  API error: {e}")
    return []


def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not api_key:
        print("Usage: DEEPSEEK_API_KEY=sk-xxx python auto_tags.py")
        sys.exit(1)

    posts_dir = os.path.abspath(POSTS_DIR)
    updated = 0

    for fname in sorted(os.listdir(posts_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(posts_dir, fname)
        with open(fpath, "r") as f:
            content = f.read()

        fm, body = extract_frontmatter(content)
        if not fm.get("date"):
            print(f"SKIP {fname} (no frontmatter)")
            continue

        print(f"Processing {fname}...")
        tags = call_deepseek(api_key, body)
        if not tags:
            print(f"  No tags extracted, skipping")
            continue

        print(f"  Tags: {tags}")
        new_content = rebuild_frontmatter(fm, tags, content)
        with open(fpath, "w") as f:
            f.write(new_content)
        updated += 1

    print(f"\nDone. Updated {updated} posts.")


if __name__ == "__main__":
    main()
