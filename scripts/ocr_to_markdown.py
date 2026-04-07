#!/usr/bin/env python3
"""
小红书截图 -> Markdown 转换工具

Usage:
    python scripts/ocr_to_markdown.py --input ./screenshots/ --output docs/blog/posts/ --engine claude
    python scripts/ocr_to_markdown.py --input ./screenshots/ --output docs/blog/posts/ --engine openai --dry-run
"""

import argparse
import base64
import os
import sys
from datetime import date
from pathlib import Path

# 支持的图片格式
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

# Blog post 模板
POST_TEMPLATE = """---
date: {date}
authors:
  - gary
categories:
  - {category}
tags:
  - {tags}
---

# {title}

> 📌 本文整理自小红书帖子

<!-- OCR 自动转录，请人工校对 -->
<!-- more -->

## TL;DR

{tldr}

## 正文

{content}

## 相关资源

<!-- TODO: 添加相关链接 -->

---

!!! original "原始来源"
    本文整理自小红书帖子：<!-- TODO: 填入原帖链接 -->
    原始截图：`{source_image}`
"""


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    """获取图片 MIME 类型"""
    ext = Path(image_path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/png")


def ocr_with_claude(image_path: str) -> dict:
    """使用 Claude Vision API 进行 OCR + 内容整理"""
    try:
        import anthropic
    except ImportError:
        print("Error: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY 环境变量未设置")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    image_data = encode_image(image_path)
    mime_type = get_mime_type(image_path)

    prompt = """请仔细识别这张小红书截图中的所有文字内容，并整理为结构化的 Markdown 格式。

要求：
1. 完整转录所有可见文字（不要遗漏）
2. 保持原文的段落结构
3. 如果有代码片段，用代码块包裹并标注语言
4. 如果有列表/步骤，用 Markdown 列表格式
5. 忽略水印、用户头像、点赞数等非内容元素

请以 JSON 格式返回：
{
  "title": "从内容推断的标题",
  "tldr": "一句话总结",
  "content": "完整的正文内容（Markdown 格式）",
  "category": "推断的分类（AI工具/教程/热点解读/其他）",
  "tags": "逗号分隔的标签建议"
}

只返回 JSON，不要其他内容。"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    import json

    text = response.content[0].text
    # 尝试从可能的 markdown 代码块中提取 JSON
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    return json.loads(text.strip())


def ocr_with_openai(image_path: str) -> dict:
    """使用 OpenAI Vision API 进行 OCR + 内容整理"""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: pip install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY 环境变量未设置")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    image_data = encode_image(image_path)
    mime_type = get_mime_type(image_path)

    prompt = """请仔细识别这张小红书截图中的所有文字内容，并整理为结构化的 Markdown 格式。

要求：
1. 完整转录所有可见文字
2. 保持原文的段落结构
3. 代码片段用代码块包裹
4. 列表/步骤用 Markdown 列表格式
5. 忽略水印、头像、点赞数等

请以 JSON 格式返回：
{"title": "标题", "tldr": "一句话总结", "content": "正文Markdown", "category": "分类", "tags": "标签"}

只返回 JSON。"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
                    },
                ],
            }
        ],
        max_tokens=4096,
    )

    import json

    text = response.choices[0].message.content
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    return json.loads(text.strip())


# 引擎映射
ENGINES = {
    "claude": ocr_with_claude,
    "openai": ocr_with_openai,
}


def process_image(image_path: str, output_dir: str, engine: str, dry_run: bool = False) -> str:
    """处理单张图片"""
    print(f"  处理: {image_path}")

    # 调用 OCR
    ocr_fn = ENGINES[engine]
    result = ocr_fn(image_path)

    # 生成文件名
    today = date.today().isoformat()
    slug = result["title"].lower().replace(" ", "-")[:50]

    # 简单处理中文文件名
    import re

    slug = re.sub(r"[^\w\-]", "", slug) or "untitled"
    filename = f"{today}-{slug}.md"
    filepath = os.path.join(output_dir, filename)

    # 生成 Markdown
    markdown = POST_TEMPLATE.format(
        date=today,
        title=result["title"],
        tldr=result.get("tldr", "TODO"),
        content=result.get("content", "TODO"),
        category=result.get("category", "待分类"),
        tags=result.get("tags", "待填写"),
        source_image=os.path.basename(image_path),
    )

    if dry_run:
        print(f"  [DRY RUN] 将写入: {filepath}")
        print(f"  标题: {result['title']}")
        print(f"  分类: {result.get('category', '?')}")
        print()
    else:
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"  已写入: {filepath}")

    return filepath


def main() -> None:
    parser = argparse.ArgumentParser(description="小红书截图 -> Markdown 转换工具")
    parser.add_argument("--input", required=True, help="截图目录路径")
    parser.add_argument("--output", required=True, help="输出目录路径")
    parser.add_argument("--engine", choices=list(ENGINES.keys()), default="claude", help="OCR 引擎")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入文件")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Error: 目录不存在: {input_dir}")
        sys.exit(1)

    # 收集图片
    images = sorted([str(f) for f in input_dir.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS])

    if not images:
        print(f"未找到图片文件 ({', '.join(sorted(IMAGE_EXTENSIONS))})")
        sys.exit(0)

    print(f"找到 {len(images)} 张图片，使用 {args.engine} 引擎")
    if args.dry_run:
        print("[DRY RUN 模式]")
    print()

    results = []
    for img in images:
        try:
            path = process_image(img, args.output, args.engine, args.dry_run)
            results.append(path)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n完成！处理了 {len(results)}/{len(images)} 张图片")
    if not args.dry_run:
        print("注意：请人工校对生成的 Markdown 文件")


if __name__ == "__main__":
    main()
