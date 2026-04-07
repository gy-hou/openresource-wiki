---
date: 2026-04-01
authors:
  - gy-hou
categories:
  - AI 工具
tags:
  - DeepSeek
  - API
  - 教程
---

# DeepSeek API 完全使用指南

> 手把手教你用 DeepSeek API，省钱又好用

<!-- more -->

## TL;DR

DeepSeek 是目前性价比最高的国产大模型 API 之一。本文手把手教你从注册到搭配 Chatbox 使用的全流程。

<!-- TODO: 替换为真实内容 -->

## 为什么选 DeepSeek

占位内容：对比各家 API 的价格和效果。

## 注册和获取 API Key

### 第一步：注册账号

占位内容：注册流程说明。

### 第二步：获取 API Key

占位内容：创建与复制 API Key 的步骤。

!!! warning "注意"
    API Key 要妥善保管，不要上传到 GitHub。

## 搭配 Chatbox 使用

{{ card_row(github_repo("Bin-Huang/chatbox")) }}

```json
{
  "api_endpoint": "https://api.deepseek.com/v1",
  "model": "deepseek-chat",
  "api_key": "your-api-key-here"
}
```

## 搭配代码使用

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

## 常见问题

??? question "API 调用报错怎么办？"
    占位回答：检查 endpoint、model 名称和 API Key 是否正确。

??? question "每月大概花多少钱？"
    占位回答：按 token 消耗计费，建议先做小规模压测估算预算。

## 相关资源

- [DeepSeek 官方文档](https://platform.deepseek.com/docs)
- [Chatbox 下载](https://chatboxai.app/)

---

!!! original "原始来源"
    本文整理自小红书帖子：<!-- TODO: 填入原帖链接 -->
