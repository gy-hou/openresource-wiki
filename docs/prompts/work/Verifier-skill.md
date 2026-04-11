---
tags:
  - prompt
  - Verifier Skill
  - OpenClaw
  - AI Agent
  - 验收
  - 编程
  - 效率
---

# 防 Agent 偷懒注入 Skill-Verifier

> 给 OpenClaw 增加“执行 + 验收 + 自动重试”闭环，减少人工盯盘。

## 适用场景

- 模型经常“先交半成品，再等你追问”
- Skill 里有硬约束，但执行不稳定
- 你希望把“催三遍”变成自动验收与自动打回

## 使用方式

1. 把下面整段 Prompt 发给 CC / Codex（不是发给 OpenClaw）。
2. 先填入你的 `Skill 文件路径`。
3. 按 Prompt 里的执行顺序推进：先 `Step 0` 生成 checklist，再逐步实现。

## Prompt 正文（原文）

```text
Skill 文件路径：[在这里填你的 skill 文件路径]
帮我在本地搭建Agent 执行验收系统
我的 OpenClaw 在实际运行中发现一个严重问题：模型会"偷懒"——skill 里明确写了约束，模型读了也承认了，但执行时只做最省力的部分，提前宣称完成。需要人工反复追问才能补齐。
现在要建一套自动化验收机制，彻底替代人工盯盘。开始
先读取我指定的 skill 文件，生成 skill_checklist.json，给我确认后再写代码。

架构设计（三层）
Openclaw 执行任务
       ↓ 输出结果
[Layer 1] 硬规则门禁（Python）
       ↓ 通过？
       │── 不通过 → 生成缺项清单 → 注入回Openclaw 重试
       ↓ 通过
[Layer 2] LLM Verifier（第三方API，审计输出质量）
       ↓ 通过？
       │── 不通过 → 生成具体问题描述 → 注入回Openclaw重试
       ↓ 通过
[Layer 3] 放行发布 / 推送
       
重试上限：最多 2 次。超过 → 标记任务失败，推送告警给我。

你要做的事
Step 0: 读取 skill 文件
先读取我 workspace 中的 skill 文件（路径我会指定），提取出所有显式约束和验收条件。

重点关注：XXXA, XXB

这个 checklist 是整个系统的唯一事实来源，后续 Layer 1 和 Layer 2 都基于它工作。
如果 skill 文件里的约束是模糊的，你标注出来让我确认，不要自己猜。

Step 1: 写 Layer 1 — 硬规则门禁（Python）
文件名：verifier_hard_gate.py
这是纯本地 Python 脚本，不调任何 API。 输入：Openclaw 的执行输出（文件内容 + 执行日志） 输出：pass / fail + 缺项清单（JSON）
（1）给出具体检查项：XXC, XXD.
把这些提取成一个 JSON 格式的 skill_checklist.json：
 （2）给出输出格式--关键设计原则：
* retry_instruction 必须包含具体缺项，不能只说"没做完"
* 每一项检查都要有明确的 pass/fail，不要用模糊的评分
* 宁可误报（false negative），不可漏报（false positive）

Step 2: 写 Layer 2 — Agent Verifier
文件名：verifier_llm.py
这层只在 Layer 1 通过后才触发。目的是抓 Layer 1 抓不到的"软偷懒"：
* 数据是真实抓取的还是搜索摘要伪装的
* 内容质量是否达标（不是一堆空泛描述）
* 是否存在明显的复制粘贴/编造痕迹
调用 第三方API（推荐 Haiku，够用且便宜）：


Step 3: 写编排器 — 把 Layer 1 + Layer 2 + 重试串起来
文件名：verifier_orchestrator.py
输入：
  - skill_checklist.json 路径
  - Openclaw输出文件路径
  - Openclaw执行日志路径
  - 重试回调函数（用于把 retry_instruction 注入回 Openclaw）
  - 告警回调函数（用于推送失败通知给我）

流程：
  1. 加载 skill_checklist.json
  2. 运行 Layer 1 硬规则检查
     - 如果 fail → 生成 retry_instruction → 调用重试回调 → 等待新输出 → 回到 2
  3. 运行 Layer 2 LLM 验证
     - 如果 fail → 生成 retry_instruction → 调用重试回调 → 等待新输出 → 回到 2
  4. 全部通过 → 返回 VERIFIED，放行发布
  
  重试计数器：最多 2 次（Layer 1 + Layer 2 合计）
  超过 2 次 → 返回 FAILED → 调用告警回调
编排器需要支持：
* 命令行调用（方便集成到现有工作流）
* 作为 Python 模块 import（方便嵌入 OpenClaw）
* 每次运行生成一份审计日志（记录每层的 pass/fail、retry 内容、最终结果）

Step 4: 写强制输出格式注入器
文件名：completion_checklist_injector.py
这个脚本生成一段文本，在 MiniMax 执行任务之前注入到 prompt 末尾，强制它在输出结尾附带结构化自检表。
根据 skill_checklist.json 自动生成，并输出结果：
额外要求
1. 所有代码加完整的类型标注（type hints）
2. 所有 API 调用加 try/except 和超时处理
3. Claude API key 从环境变量 ANTHROPIC_API_KEY 读取
4. 输出的审计日志写入 logs/verify_{skill_name}_{timestamp}.json
5. 写一个 README.md 说明如何安装依赖、配置、运行
6. 写测试用例：至少覆盖"全通过""Layer1 fail""Layer2 fail""超过重试上限"四种场景

Step 5: 冒烟测试（验收系统自身的验收）
写入文件，命名：tests/test_verifier.py。确保验收系统本身被验证。
根据当前skill 给出必须覆盖的测试场景。
mock 数据要求
* 准备至少 2 份 mock 输出文件：一份合格、一份不合格
* 准备至少 2 份 mock 日志：一份有 CDP 证据、一份没有
* Layer 2 的 LLM 调用在测试中 mock 掉，不实际调 API

额外要求
1. 所有代码加完整的类型标注（type hints）
2. 所有 API 调用加 try/except 和超时处理
3. 第三方API key 从环境变量读取
4. 审计日志写入 logs/verify_{skill_name}_{timestamp}.json
5. 写 README.md：安装依赖、配置、运行方式、架构图
6. 项目结构清晰，不要把所有东西塞一个文件

【强制要求】任务完成后，你必须在输出末尾附带以下格式的自检表，逐项如实填写。
缺少此表或内容与实际不符将导致任务被自动打回。

执行顺序

Step 0 → 输出 skill_checklist.json → 等我确认
确认后 →
Step 1 → verifier_hard_gate.py
Step 2 → verifier_llm.py
Step 3 → verifier_orchestrator.py
Step 4 → completion_checklist_injector.py
Step 5 → tests/test_verifier.py + mock 数据
最后 → README.md
现在开始。先读取 skill 文件，生成 skill_checklist.json。

```

## 补充建议

- 执行模型与验收模型分离（执行便宜、验收更稳）。
- 默认把 `false positive` 风险压到最低，宁可误报要求重跑。
- 单次任务先做小规模冒烟，再接入完整业务流。
