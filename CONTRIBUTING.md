# 贡献指南

感谢你对本 Wiki 的兴趣！

## 如何贡献内容

### 1. Fork 本仓库

### 2. 选择合适的模板

模板位于 `docs/_templates/` 目录：

| 模板 | 用途 |
|------|------|
| `blog-post.md` | 博客文章、小红书帖子整理 |
| `prompt-template.md` | Prompt 分享 |
| `skill-template.md` | Claude Skill 分享 |
| `tool-template.md` | 工具推荐 |
| `project-template.md` | 项目展示 |

### 3. 创建内容文件

- **博客文章**放在 `docs/blog/posts/` 下，文件名格式：`YYYY-MM-DD-标题.md`
- **Prompt** 放在 `docs/prompts/对应分类/` 下
- **Skill** 放在 `docs/skills/` 下
- **工具推荐**放在 `docs/toolbox/对应分类/` 下

### 4. 文件命名规范

- 使用小写英文 + 短横线：`deepseek-api-guide.md` ✅
- 不要用中文文件名：`深度求索教程.md` ❌
- 不要用空格：`my file.md` ❌
- 不要用下划线：`my_file.md` ❌（index.md 除外）

### 5. 图片规范

- 图片放在 `docs/assets/images/` 下，按内容分子目录
- 压缩图片后再提交（推荐用 tinypng.com）
- 图片文件名用英文

### 6. 提交 PR

- PR 标题简洁明了
- 描述中说明添加了什么内容
- 确保 `mkdocs build --strict` 没有报错

## 标签规范

常用标签：
- 内容类型：`prompt`, `skill`, `工具`, `教程`, `热点解读`
- AI 模型：`Claude`, `GPT`, `Gemini`, `DeepSeek`
- 主题：`编程`, `写作`, `研究`, `效率`
- 难度：`入门`, `进阶`, `高级`

## 问题反馈

发现 bug 或有内容建议？请提 [Issue](https://github.com/gy-hou/openresource-wiki/issues)。
