#!/usr/bin/env python3
"""Generate cover images for featured blog posts using Doubao (豆包) API."""

import os
import sys
import json
import urllib.request

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "blog", "posts")
COVERS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "images", "blog", "covers")
ARK_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

# Only generate covers for featured posts (by slug)
FEATURED_SLUGS = [
    "karpathy-knowledge-base",
    "deepseek-api-完全使用指南",
    "claude-code-进阶使用技巧",
    "openclaw-advanced",
    "claude-code-memory-analysis",
]


def extract_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line and not line.startswith("  "):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"')
    return fm, parts[2]


def gen_cover(api_key, title, body_snippet):
    """Call Doubao API to generate a cover image."""
    prompt = (
        f"科技博客封面图，文章标题：'{title}'。"
        f"内容概述：{body_snippet[:200]}。"
        "风格：未来科技感，深蓝色调为主，搭配紫色和青色光效，"
        "抽象几何线条和粒子效果，光线追踪，OC渲染，"
        "简洁大气，无文字，适合作为博客横幅封面，"
        "暗色背景，发光线条和节点，数据可视化风格。"
    )

    payload = json.dumps({
        "model": "doubao-seedream-5-0-260128",
        "prompt": prompt,
        "response_format": "url",
        "size": "2560x1440",
        "stream": False,
        "watermark": False,
    }).encode()

    req = urllib.request.Request(
        ARK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())

        # Response format: { "data": [{ "url": "..." }] }
        items = data.get("data", [])
        if items and items[0].get("url"):
            img_url = items[0]["url"]
            # Download the image
            img_req = urllib.request.Request(img_url)
            with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                img_data = img_resp.read()
                content_type = img_resp.headers.get("Content-Type", "image/png")
                ext = "jpg" if "jpeg" in content_type or "jpg" in content_type else "png"
                return img_data, ext

    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        print(f"  API error {e.code}: {body[:500]}")
    except Exception as e:
        print(f"  Error: {e}")
    return None, None


def slug_from_fm(fm, fname):
    """Get slug from frontmatter or filename."""
    if fm.get("slug"):
        return fm["slug"]
    name = os.path.splitext(fname)[0]
    parts = name.split("-", 3)
    if len(parts) >= 4 and parts[0].isdigit():
        return parts[3]
    return name


def main():
    api_key = os.environ.get("ARK_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not api_key:
        print("Usage: ARK_API_KEY=xxx python gen_covers.py")
        sys.exit(1)

    os.makedirs(COVERS_DIR, exist_ok=True)
    posts_dir = os.path.abspath(POSTS_DIR)
    generated = 0
    skipped_not_featured = 0

    for fname in sorted(os.listdir(posts_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(posts_dir, fname)
        with open(fpath, "r") as f:
            content = f.read()

        fm, body = extract_frontmatter(content)
        if not fm.get("date"):
            continue

        slug = slug_from_fm(fm, fname)

        # Only generate for featured posts
        if slug not in FEATURED_SLUGS:
            skipped_not_featured += 1
            continue

        # Check if cover already exists
        exists = False
        for ext in ["png", "jpg"]:
            if os.path.exists(os.path.join(COVERS_DIR, f"{slug}.{ext}")):
                print(f"SKIP {slug} (cover exists)")
                exists = True
                break
        if exists:
            continue

        title = fm.get("title", fname)
        for line in body.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        print(f"Generating cover for: {title}...")
        img_data, ext = gen_cover(api_key, title, body[:500])
        if img_data:
            out_path = os.path.join(COVERS_DIR, f"{slug}.{ext}")
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"  Saved: covers/{slug}.{ext} ({len(img_data)} bytes)")
            generated += 1
        else:
            print(f"  Failed to generate")

    print(f"\nDone. Generated {generated} covers. (Skipped {skipped_not_featured} non-featured)")
    if generated > 0:
        print(f"Covers saved to: {os.path.abspath(COVERS_DIR)}")


if __name__ == "__main__":
    main()
