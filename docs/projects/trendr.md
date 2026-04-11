---
tags:
  - 项目
  - Python
  - AI
---

# TrendR

> AI 驱动的自动化研究趋势追踪与文献综述工具

![TrendR Hero](../assets/images/projects/trendr.svg){ .project-hero }

## 要解决的问题

研究者每天面对海量论文和技术博客，手动追踪领域趋势既耗时又容易遗漏。需要一个能自动收集、分析、总结研究趋势的工具。

## 做了什么

- 构建了基于 PPO + Actor-Critic 的 RL Trading Agent，支持 MLP/Transformer 消融实验
- 开发了本地 Agent 系统，集成 QMD + Scrapling 实现自动数据采集
- 实现了结构化知识库管理，支持自动摄入和查询

## 技术栈

<div class="md-tags">
  <span class="md-tag">Python</span>
  <span class="md-tag">PyTorch</span>
  <span class="md-tag">PPO</span>
  <span class="md-tag">Actor-Critic</span>
  <span class="md-tag">MLP</span>
  <span class="md-tag">Transformer</span>
  <span class="md-tag">Scrapling</span>
  <span class="md-tag">QMD</span>
  <span class="md-tag">Local LLM Agent</span>
</div>

## 当前进度

| 模块 | 状态 |
|------|------|
| RL Trading Agent 核心 | 🟡 开发中 |
| MLP/Transformer 消融实验 | 🟡 进行中 |
| 数据采集管道 | 🟢 可用 |
| Agent 工作流 | 🟡 迭代中 |
| 文档 | 🔴 待完善 |

## Repo

- 暂未公开（开发阶段）

## 下一步

- [ ] 完成 Transformer vs MLP 消融实验对比报告
- [ ] 接入更多数据源（arXiv, Semantic Scholar）
- [ ] 搭建 Web Dashboard 可视化趋势
- [ ] 开源核心模块

<div class="blog-share">
  <div class="blog-share-title">分享这个项目</div>
  <div class="blog-share-buttons">
    <a href="#" onclick="return shareToWechat(event);" class="share-btn share-btn--wechat" title="微信分享">
      微信
    </a>
    <a href="https://xhslink.com/m/3lRU7a53RSt" target="_blank" rel="noopener" class="share-btn share-btn--xhs" title="小红书">
      小红书
    </a>
    <a href="https://github.com/gy-hou/openresource-wiki" target="_blank" rel="noopener" class="share-btn share-btn--github" title="GitHub">
      GitHub
    </a>
  </div>
</div>
