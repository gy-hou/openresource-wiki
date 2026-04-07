---
tags:
  - skill
  - 自动化
  - 效率
---

# 博客标签自动提取 Skill

> 自研 Skill：用 DeepSeek API 自动为博客文章提取 2-3 个标签

## 类型

构建脚本（Python CLI）

## 原理

1. 遍历 `docs/blog/posts/` 下所有 `.md` 文件
2. 读取文章正文（截取前 2000 字）
3. 调用 DeepSeek API，从预定义标签列表中选择 2-3 个最匹配的
4. 自动更新 frontmatter 中的 `tags` 字段

## 使用

```bash
# 设置环境变量
export DEEPSEEK_API_KEY=sk-xxx

# 运行
python3 scripts/auto_tags.py

# 或直接传 key
python3 scripts/auto_tags.py sk-xxx
```

## 预定义标签列表

```
Claude Code, Claude, DeepSeek, GPT, Gemini, OpenClaw,
AI Agent, API, Obsidian, prompt, skill,
知识库, 工作流, 效率, 教程, 编程, 写作, 研究,
长期记忆, 自动化, Fintech, 开源, 工具
```

需要新增标签时，修改 `scripts/auto_tags.py` 中的 `ALLOWED_TAGS` 列表。

## 配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 模型 | `deepseek-chat` | 成本极低（~0.001元/篇） |
| temperature | 0.3 | 低温度保证一致性 |
| max_tokens | 100 | 只需要返回 JSON 数组 |

## 源码

[`scripts/auto_tags.py`](https://github.com/gy-hou/publicwiki/blob/main/scripts/auto_tags.py)
