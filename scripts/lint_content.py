#!/usr/bin/env python3
"""
Wiki 内容健康检查工具

Usage:
    python scripts/lint_content.py
    python scripts/lint_content.py --docs-dir docs/ --strict
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class ContentLinter:
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.errors = []    # 必须修复
        self.warnings = []  # 建议修复
        self.infos = []     # 参考信息
        self._yaml_missing_reported = False

    def lint(self) -> None:
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

    def _check_frontmatter(self, path: Path, content: str) -> None:
        """检查 frontmatter"""
        # 某些页面不需要 tags（index、tags、404 等）
        skip_files = {"index.md", "tags.md", "404.md", "roadmap.md"}
        if path.name in skip_files:
            return

        if not content.startswith("---"):
            self.warnings.append(f"{path}: 缺少 frontmatter")
            return

        if yaml is None:
            if not self._yaml_missing_reported:
                self.infos.append("未安装 PyYAML，frontmatter 使用降级检查（建议 `pip install pyyaml`）")
                self._yaml_missing_reported = True
            parts = content.split("---", 2)
            if len(parts) >= 3:
                if re.search(r"^tags\s*:", parts[1], re.MULTILINE) is None:
                    self.warnings.append(f"{path}: frontmatter 中缺少 tags")
            return

        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                if fm and not fm.get("tags"):
                    self.warnings.append(f"{path}: frontmatter 中缺少 tags")
        except yaml.YAMLError as e:
            self.errors.append(f"{path}: frontmatter YAML 解析错误: {e}")

    def _check_empty(self, path: Path, content: str) -> None:
        """检查空文件"""
        # 去掉 frontmatter 后检查
        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL).strip()
        if not body:
            self.warnings.append(f"{path}: 文件内容为空（只有 frontmatter）")
        elif len(body) < 20:
            self.infos.append(f"{path}: 内容很少（{len(body)} 字符）")

    def _check_todos(self, path: Path, content: str) -> None:
        """检查 TODO 标记"""
        todos = re.findall(r"<!--\s*TODO.*?-->", content)
        if todos:
            self.infos.append(f"{path}: 包含 {len(todos)} 个 TODO 标记")

    def _check_broken_images(self, path: Path, content: str) -> None:
        """检查图片引用"""
        images = re.findall(r"!\[.*?\]\(((?!http)[^)]+)\)", content)
        for img in images:
            img_path = (self.docs_dir / path.parent / img).resolve()
            if not img_path.exists():
                alt_path = (self.docs_dir / img).resolve()
                if not alt_path.exists():
                    self.warnings.append(f"{path}: 图片不存在: {img}")

    def _check_broken_links(self, path: Path, content: str) -> None:
        """检查内部链接"""
        links = re.findall(r"\[.*?\]\(((?!http|#|mailto)[^)]+)\)", content)
        for link in links:
            link_path = link.split("#")[0]
            if not link_path:
                continue
            if link_path.endswith(".xml"):
                continue
            target = (self.docs_dir / path.parent / link_path).resolve()
            if not target.exists():
                alt_target = (self.docs_dir / link_path).resolve()
                if not alt_target.exists():
                    self.warnings.append(f"{path}: 内部链接目标不存在: {link}")

    def _check_filename(self, path: Path) -> None:
        """检查文件命名规范"""
        name = path.stem
        if name == "index" or name.startswith("."):
            return
        if not re.match(r"^[a-z0-9][a-z0-9\-]*$", name):
            self.warnings.append(f"{path}: 文件名不符合规范（应为小写英文+短横线）")

    def _check_unclosed_codeblocks(self, path: Path, content: str) -> None:
        """检查未闭合的代码块"""
        fences = re.findall(r"^(`{3,})", content, re.MULTILINE)
        if len(fences) % 2 != 0:
            self.errors.append(f"{path}: 可能存在未闭合的代码块（{len(fences)} 个 fence）")

    def report(self) -> int:
        """输出报告，返回 exit code"""
        if self.errors:
            print("ERRORS（必须修复）:")
            for e in self.errors:
                print(f"  {e}")
            print()

        if self.warnings:
            print("WARNINGS（建议修复）:")
            for w in self.warnings:
                print(f"  {w}")
            print()

        if self.infos:
            print("INFO（参考信息）:")
            for i in self.infos:
                print(f"  {i}")
            print()

        print(f"总计: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.infos)} infos")

        return 1 if self.errors else 0


def main() -> None:
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
