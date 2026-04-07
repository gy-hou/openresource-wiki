# 辅助脚本

## ocr_to_markdown.py

将小红书截图批量转换为 Markdown 博客文章。

### 安装依赖

```bash
# Claude 引擎
pip install anthropic

# OpenAI 引擎
pip install openai
```

### 使用方法

```bash
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
```

### 注意事项

- 生成的文件带有 `<!-- OCR 自动转录，请人工校对 -->` 标记
- 务必人工检查生成结果的准确性
- API Key 从环境变量读取，不要硬编码

## lint_content.py

检查 Wiki 内容健康度（frontmatter、链接、图片、代码块、TODO 等）。

### 依赖

```bash
pip install pyyaml
```

### 使用方法

```bash
# 默认检查 docs/
python scripts/lint_content.py

# 指定目录
python scripts/lint_content.py --docs-dir docs/

# 严格模式（warnings 也失败）
python scripts/lint_content.py --docs-dir docs/ --strict
```
