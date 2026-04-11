# Openresource-Wiki Assistant Index

> 用途：给站内 AI 助手提供“路径 + 简介”索引，帮助用户快速定位页面。
> 更新规则：每次新增或改文后，重建本文件。

## 使用规则（给助手）

- 用户问“去哪看/怎么找”时，优先返回 1-3 个最相关路径。
- 只返回站内真实存在的路径，不编造链接。
- 站内没有的信息，明确说明“本站未提供”。

## 博客文章（路径 + 简介）

- `/blog/openclaw-harness-engineering/` | **从 OpenClaw 看 Harness Engineering：2026 年 AI Agent 真正的壁垒，可能已经不是模型了** | 2026 年开始，大家比拼的不是 Agent 能不能工作，而是怎么让 Agent 可靠地工作。
- `/blog/openclaw-tulip-bubble/` | **OpenClaw 到底是不是郁金香泡沫？** | 判断一个东西是不是泡沫，不在于市场热度和关注度，而在于它是否对真实的生产和生活产生了重大影响。
- `/blog/claude-code-memory-analysis/` | **Claude Code 泄漏版：智能体长期记忆与自我进化解析** | 不是单 agent 变聪明，而是把 agent 做成了一套可调度、可持久化的 runtime
- `/blog/ai-model-landscape/` | **2026 年 AI 模型格局：谁在领跑？** | 从能力、成本和可用性三个角度看模型竞争态势
- `/blog/karpathy-ai-auto-research-trendr/` | **Karpathy AI 自动实验启发：让 AI 自动写综述** | 让 AI agent 自己搜索、筛选、精读、写综述，再自动沉淀到 Obsidian。
- `/blog/openclaw-advanced/` | **OpenClaw 新手到高阶全攻略：技能矩阵到手搓工作流** | 从新手到进阶，再到自己手搓工作流——一步一步带你走完
- `/blog/claude-code-进阶使用技巧/` | **Claude Code 进阶使用技巧** | 10 个高频技巧，帮你把 Claude Code 用得更稳更快
- `/blog/deepseek-api-完全使用指南/` | **DeepSeek API 完全使用指南** | 手把手教你用 DeepSeek API，省钱又好用
- `/blog/karpathy-knowledge-base/` | **一个 Prompt + 工具清单，搭建 Karpathy 本地知识库** | 把工具清单和 Prompt 直接复制发给你的 Claude Code / Codex 就能开搭
- `/blog/wechat-ai-agent-architecture/` | **我把整个微信社交上下文交给了 Agent** | 这不是“做了个微信机器人”，而是把 WeFlow、ilink 和 Agent 大脑真正焊成了一套主动式个人管家系统。
- `/blog/one-command-stop-openclaw-fake-work/` | **一个命令防止Openclaw假装干活** | 我给 OpenClaw 的 skill 写了硬约束，但它依然可能先交半成品再宣称完成。这里给一段可复用的验收 Prompt 来兜底。

## Prompt 页面（路径 + 简介）

- `/prompts/life/xiaohongshu-writer/` | **小红书爆款帖子写作 Prompt** | 适用场景：快速产出小红书风格的高可读帖子
- `/prompts/research/knowledge-base-manager/` | **LLM 本地知识库管理 Prompt** | 自研 Prompt：让 AI 管理你的本地 Markdown 知识库（Karpathy 风格）
- `/prompts/research/paper-reader/` | **论文精读 Prompt** | 适用场景：结构化精读论文并提炼可执行结论
- `/prompts/study/ai-assistant-system/` | **通用 AI 助手 System Prompt 模板** | 适用场景：快速搭建可控、稳定、可复用的 AI 助手
- `/prompts/study/tech-blog-writer/` | **技术博客写作 Prompt** | 自研 Prompt：把草稿 / 笔记快速整理成结构化技术博文
- `/prompts/work/Verifier-skill/` | **防 Agent 偷懒注入 Skill-Verifier** | 给 OpenClaw 增加“执行 + 验收 + 自动重试”闭环，减少人工盯盘。
- `/prompts/work/claude-code-workflow/` | **Claude Code 工程化工作流 Prompt** | 自研 Prompt：让 Claude Code 按"计划→执行→验证"闭环工作
- `/prompts/work/code-review-prompt/` | **代码审查 Prompt** | 适用场景：让 AI 对你的代码进行系统性审查

## 项目页面（路径 + 简介）

- `/projects/advanced-prompts-db/` | **Advanced Prompts DB** | ChatGPT 高级 Prompt 数据库，一键 Vercel 部署
- `/projects/openclaw/` | **OpenClaw 自动化浏览器** | 开源 AI 工具集 — 多 Agent 编排 + 可复用工作流模块
- `/projects/openresource-wiki/` | **OpenResource Wiki** | 你正在看的这个站点 — AI 工具、提示词库与技能库的开源知识站
- `/projects/trendr/` | **TrendR** | AI 驱动的自动化研究趋势追踪与文献综述工具

## 工具库页面（路径 + 简介）

- `/toolbox/ai-platforms/model-comparison/` | **主流 AI 模型实测对比** | 氪了主流 AI 会员后，按真实高强度使用场景给出一版实测评分。
- `/toolbox/dev-tools/ai-coding-tools/` | **AI 编程工具全景图** | 按真实开发工作流对比主流 AI 编程工具，帮助你快速选型。
- `/toolbox/workflows/wiki-setup-tools/` | **搭建个人 Wiki 的工具清单** | 分层梳理从写作到部署的关键工具

## 技能模板页面（路径 + 简介）

- `/skills/templates/auto-tag-extractor/` | **博客标签自动提取 Skill** | 自研 Skill：用 DeepSeek API 自动为博客文章提取 2-3 个标签
- `/skills/templates/chrome-cdp-setup/` | **Chrome CDP 双实例调试架构** | 🛠️ Chrome 146+ 远程调试的完整解决方案，支持 Claude Code / Codex / OpenClaw
- `/skills/templates/llm-wiki-agent/` | **LLM Wiki 知识库管理 Agent** | 🛠️ 用 AI Agent 自动维护 Markdown 知识库（添加、搜索、更新、整理）
- `/skills/templates/xhs-card-generator/` | **小红书知识卡片生成器** | 🛠️ 把长文内容自动切成小红书风格的知识卡片

## 维护日志

- 2026-04-12：重建为“每篇内容页路径 + 一句话简介”的索引格式（去除 index 聚合页）。
