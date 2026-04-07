# Phase 4: 工程工具

> 本阶段创建辅助脚本和 CI 集成，提升内容管理效率。

---

## Prompt 4.1 — OCR 转 Markdown 脚本

```
创建 `scripts/ocr_to_markdown.py`，用于将小红书截图批量转换为 Markdown 文件。

## 功能需求

1. 读取指定目录下的图片（png, jpg, jpeg, webp）
2. 调用 Vision API 进行 OCR + 内容整理
3. 输出格式化的 Markdown 文件，自动套用 blog post 模板
4. 支持多种 OCR 引擎

## 完整代码

```python
#!/usr/bin/env python3
"""
小红书截图 → Markdown 转换工具

Usage:
    python scripts/ocr_to_markdown.py --input ./screenshots/ --output docs/blog/posts/ --engine claude
    python scripts/ocr_to_markdown.py --input ./screenshots/ --output docs/blog/posts/ --engine openai --dry-run
"""

import argparse
import os
import sys
import base64
from pathlib import Path
from datetime import date

# 支持的图片格式
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

# Blog post 模板
POST_TEMPLATE = '''---
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
'''


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    """获取图片 MIME 类型"""
    ext = Path(image_path).suffix.lower()
    mime_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
    }
    return mime_map.get(ext, 'image/png')


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
        messages=[{
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
        }],
    )

    import json
    text = response.content[0].text
    # 尝试从可能的 markdown 代码块中提取 JSON
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
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
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_data}"
                    },
                },
            ],
        }],
        max_tokens=4096,
    )

    import json
    text = response.choices[0].message.content
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
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
    slug = re.sub(r'[^\w\-]', '', slug) or "untitled"
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


def main():
    parser = argparse.ArgumentParser(description="小红书截图 → Markdown 转换工具")
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
    images = sorted([
        str(f) for f in input_dir.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    ])

    if not images:
        print(f"未找到图片文件 ({', '.join(IMAGE_EXTENSIONS)})")
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
        print("⚠️  请人工校对生成的 Markdown 文件")


if __name__ == "__main__":
    main()
```

## 同时创建 `scripts/README.md`

```markdown
# 辅助脚本

## ocr_to_markdown.py

将小红书截图批量转换为 Markdown 博客文章。

### 安装依赖

​```bash
# Claude 引擎
pip install anthropic

# OpenAI 引擎
pip install openai
​```

### 使用方法

​```bash
# 设置 API Key
export ANTHROPIC_API_KEY="your-key"
# 或
export OPENAI_API_KEY="your-key"

# 预览模式（不实际写入）
python scripts/ocr_to_markdown.py \
  --input ./screenshots/ \
  --output docs/blog/posts/ \
  --engine claude \
  --dry-run

# 正式转换
python scripts/ocr_to_markdown.py \
  --input ./screenshots/ \
  --output docs/blog/posts/ \
  --engine claude
​```

### 注意事项

- 生成的文件带有 `<!-- OCR 自动转录，请人工校对 -->` 标记
- 务必人工检查生成结果的准确性
- API Key 从环境变量读取，不要硬编码
```

确保脚本可以直接运行（`python scripts/ocr_to_markdown.py --help`）。
```

---

## Prompt 4.2 — 内容健康检查脚本

```
创建 `scripts/lint_content.py`，检查文档健康度。

## 完整代码

```python
#!/usr/bin/env python3
"""
Wiki 内容健康检查工具

Usage:
    python scripts/lint_content.py
    python scripts/lint_content.py --docs-dir docs/ --strict
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path


class ContentLinter:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.errors = []    # 必须修复
        self.warnings = []  # 建议修复
        self.infos = []     # 参考信息

    def lint(self):
        """运行所有检查"""
        md_files = list(self.docs_dir.rglob("*.md"))
        print(f"扫描 {len(md_files)} 个 Markdown 文件...\n")

        for md_file in md_files:
            rel_path = md_file.relative_to(self.docs_dir)

            # 跳过模板目录
            if "_templates" in str(rel_path):
                continue

            content = md_file.read_text(encoding="utf-8")

            self._check_frontmatter(rel_path, content)
            self._check_empty(rel_path, content)
            self._check_todos(rel_path, content)
            self._check_broken_images(rel_path, content)
            self._check_broken_links(rel_path, content)
            self._check_filename(rel_path)
            self._check_unclosed_codeblocks(rel_path, content)

    def _check_frontmatter(self, path, content):
        """检查 frontmatter"""
        # 某些页面不需要 tags（index、tags、404 等）
        skip_files = {'index.md', 'tags.md', '404.md', 'roadmap.md'}
        if path.name in skip_files:
            return

        if not content.startswith("---"):
            self.warnings.append(f"{path}: 缺少 frontmatter")
            return

        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                if fm and not fm.get("tags"):
                    self.warnings.append(f"{path}: frontmatter 中缺少 tags")
        except yaml.YAMLError as e:
            self.errors.append(f"{path}: frontmatter YAML 解析错误: {e}")

    def _check_empty(self, path, content):
        """检查空文件"""
        # 去掉 frontmatter 后检查
        body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL).strip()
        if not body:
            self.warnings.append(f"{path}: 文件内容为空（只有 frontmatter）")
        elif len(body) < 20:
            self.infos.append(f"{path}: 内容很少（{len(body)} 字符）")

    def _check_todos(self, path, content):
        """检查 TODO 标记"""
        todos = re.findall(r'<!--\s*TODO.*?-->', content)
        if todos:
            self.infos.append(f"{path}: 包含 {len(todos)} 个 TODO 标记")

    def _check_broken_images(self, path, content):
        """检查图片引用"""
        images = re.findall(r'!\[.*?\]\(((?!http)[^)]+)\)', content)
        for img in images:
            # 解析相对路径
            img_path = (self.docs_dir / path.parent / img).resolve()
            if not img_path.exists():
                # 也检查从 docs 根目录的路径
                alt_path = (self.docs_dir / img).resolve()
                if not alt_path.exists():
                    self.warnings.append(f"{path}: 图片不存在: {img}")

    def _check_broken_links(self, path, content):
        """检查内部链接"""
        links = re.findall(r'\[.*?\]\(((?!http|#|mailto)[^)]+)\)', content)
        for link in links:
            # 去掉锚点
            link_path = link.split("#")[0]
            if not link_path:
                continue
            target = (self.docs_dir / path.parent / link_path).resolve()
            if not target.exists():
                alt_target = (self.docs_dir / link_path).resolve()
                if not alt_target.exists():
                    self.warnings.append(f"{path}: 内部链接目标不存在: {link}")

    def _check_filename(self, path):
        """检查文件命名规范"""
        name = path.stem
        if name == "index" or name.startswith("."):
            return
        # 允许: 小写字母、数字、短横线、日期前缀
        if not re.match(r'^[a-z0-9][a-z0-9\-]*$', name):
            self.warnings.append(f"{path}: 文件名不符合规范（应为小写英文+短横线）")

    def _check_unclosed_codeblocks(self, path, content):
        """检查未闭合的代码块"""
        fences = re.findall(r'^(`{3,})', content, re.MULTILINE)
        if len(fences) % 2 != 0:
            self.errors.append(f"{path}: 可能存在未闭合的代码块（{len(fences)} 个 fence）")

    def report(self) -> int:
        """输出报告，返回 exit code"""
        total = len(self.errors) + len(self.warnings) + len(self.infos)

        if self.errors:
            print("❌ ERRORS（必须修复）:")
            for e in self.errors:
                print(f"  {e}")
            print()

        if self.warnings:
            print("⚠️  WARNINGS（建议修复）:")
            for w in self.warnings:
                print(f"  {w}")
            print()

        if self.infos:
            print("ℹ️  INFO（参考信息）:")
            for i in self.infos:
                print(f"  {i}")
            print()

        print(f"总计: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.infos)} infos")

        return 1 if self.errors else 0


def main():
    parser = argparse.ArgumentParser(description="Wiki 内容健康检查")
    parser.add_argument("--docs-dir", default="docs/", help="文档目录")
    parser.add_argument("--strict", action="store_true", help="严格模式：warnings 也返回非零 exit code")
    args = parser.parse_args()

    linter = ContentLinter(args.docs_dir)
    linter.lint()
    exit_code = linter.report()

    if args.strict and linter.warnings:
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
```

确保脚本可以直接运行。唯一的外部依赖是 `pyyaml`（通常已安装）。
在 `scripts/README.md` 中添加 lint_content.py 的使用说明。
```

---

## Prompt 4.3 — CI 增强：PR 时自动 lint

```
更新 `.github/workflows/lint.yml`，在 PR 时运行内容检查脚本。

将 Phase 0 创建的 lint.yml 更新为：

```yaml
name: Content Check

on:
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  build-check:
    name: Build Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build check (strict mode)
        run: mkdocs build --strict

  content-lint:
    name: Content Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install PyYAML
        run: pip install pyyaml

      - name: Run content linter
        run: python scripts/lint_content.py --docs-dir docs/

  link-check:
    name: Link Check
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

      - name: Build site
        run: mkdocs build

      - name: Check internal links
        run: |
          python -c "
          import os, re, sys
          site_dir = 'site'
          broken = []
          for root, dirs, files in os.walk(site_dir):
              for f in files:
                  if not f.endswith('.html'):
                      continue
                  filepath = os.path.join(root, f)
                  with open(filepath) as fh:
                      content = fh.read()
                  # 检查内部 href
                  for match in re.finditer(r'href=\"(/wiki/[^\"#]+)\"', content):
                      link = match.group(1).replace('/wiki/', '')
                      target = os.path.join(site_dir, link)
                      if not os.path.exists(target) and not os.path.exists(target + '/index.html'):
                          broken.append(f'{filepath}: {match.group(1)}')
          if broken:
              print(f'Found {len(broken)} broken internal links:')
              for b in broken[:20]:
                  print(f'  {b}')
              # 暂时不 fail，只 warn
              # sys.exit(1)
          else:
              print('No broken internal links found')
          "
```

确保 YAML 语法正确，所有 job 都能正常运行。
```

---

## 本阶段完成标准

- [ ] `scripts/ocr_to_markdown.py` 存在且 `--help` 能正常输出
- [ ] `scripts/lint_content.py` 存在且能正常运行
- [ ] `scripts/README.md` 文档完整
- [ ] `.github/workflows/lint.yml` 包含 3 个 job
- [ ] Makefile 的 `lint` 目标能运行脚本
