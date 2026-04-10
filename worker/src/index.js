/**
 * AI Chat — Cloudflare Worker proxy for DeepSeek API
 * Serves Openresource-Wiki only.
 *
 * Secrets (set via `wrangler secret put`):
 *   DEEPSEEK_API_KEY
 *
 * Environment vars (in wrangler.toml):
 *   ALLOWED_ORIGINS
 *   WIKI_CONTEXT_URL (optional)
 */

const WIKI_PROMPT_ZH = `你是 Openresource-Wiki 的智能助手。Openresource-Wiki 是一个开源知识分享站，由 Lucas（USTC，专注 AI 工具测评 / Fintech）维护。

站点板块：
- 博客：小红书热帖文字版、AI 热点解读、实操教程
- Prompt 库：编程 / 写作 / 研究方向的 Prompt 合集
- Skills 库：Claude Skills 和自动化工作流模板（如小红书知识卡片生成器）
- 工具箱：AI 平台对比、开发工具推荐、工作流搭建指南
- 项目：TrendR（AI 文献综述）、OpenClaw（AI 工具集）、Openresource-Wiki 本站
- Ideas：实验性想法（科技 / 金融 / 学术 / 开源方向）

重点文章：
1.「一个 Prompt + 工具清单，搭建 Karpathy 本地知识库」— 用 Claude Code + Obsidian 搭建本地 LLM Wiki
2.「OpenClaw 新手到高阶全攻略」— 技能矩阵、MCP 插件、手搓工作流
3.「Claude Code 泄漏版解析」— 长期记忆系统、Dream System、Agent Runtime 架构
4.「DeepSeek API 使用指南」— 注册、获取 Key、搭配 Chatbox 使用
5.「Claude Code 进阶技巧」— 10 个实用技巧，任务拆分 + 验证闭环

规则：
- 用中文回答，简洁友好
- 你是 Openresource-Wiki 助手，不是学术主页助手
- 模型后端是 DeepSeek Chat，经 Cloudflare Worker 代理
- 只回答与本站内容相关的问题
- 如果被问到站点没有的内容，建议访客去对应板块看看或提 Issue
- 如果被问到“Lucas 具体论文列表 / Google Scholar 引用次数”等本站未明确提供的数据，必须明确说“本站未提供，建议去学术主页或 Google Scholar 查询”
- 不要编造不存在的文章或功能
- 回答控制在 200 字以内`;

const WIKI_PROMPT_EN = `You are the AI assistant for Openresource-Wiki.

Site focus:
- Practical AI tools, prompt engineering, and agent workflows
- Tutorials and project write-ups (TrendR, OpenClaw, Openresource-Wiki)
- Prompt/Skill libraries and tool comparisons

Rules:
- Answer in English for this turn
- You are the assistant for Openresource-Wiki, not the academic homepage assistant
- Model backend: DeepSeek Chat via Cloudflare Worker proxy
- Keep the response concise and practical
- Only answer based on site-related content
- If asked for Lucas publication list or Google Scholar citation metrics not explicitly available on this wiki, clearly say it is not provided on this site and suggest checking the academic homepage or Google Scholar
- If information is unavailable, say so clearly
- Do not fabricate links, features, or articles`;

const MAX_MESSAGES = 10;
const CONTEXT_CACHE_TTL_MS = 10 * 60 * 1000;
const MAX_CONTEXT_CHARS = 3200;
const DEFAULT_WIKI_CONTEXT_URL = "https://raw.githubusercontent.com/gy-hou/openresource-wiki/main/docs/assets/ai/wiki-assistant-index.md";
const contextCache = { fetchedAt: 0, content: "" };

function safePathnameFromUrl(rawUrl) {
  if (!rawUrl) return "";
  try {
    const parsed = new URL(rawUrl);
    return parsed.pathname || "";
  } catch {
    return "";
  }
}

function isLocalDev(origin, referer) {
  return /(localhost|127\.0\.0\.1)/.test(origin || "") || /(localhost|127\.0\.0\.1)/.test(referer || "");
}

function isWikiRequest(siteMode, origin, referer) {
  const refererPath = safePathnameFromUrl(referer);
  const fromWikiPath = refererPath === "/openresource-wiki" || refererPath.startsWith("/openresource-wiki/");
  const fromBody = siteMode === "wiki";
  return fromWikiPath || (fromBody && !!origin) || isLocalDev(origin, referer);
}

function getSystemPrompt(responseLanguage) {
  return responseLanguage === "en" ? WIKI_PROMPT_EN : WIKI_PROMPT_ZH;
}

function getContextUrl(env) {
  return env.WIKI_CONTEXT_URL || DEFAULT_WIKI_CONTEXT_URL;
}

function sanitizeContext(raw) {
  if (!raw || typeof raw !== "string") return "";
  return raw
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/\r/g, "")
    .trim()
    .slice(0, MAX_CONTEXT_CHARS);
}

async function loadAssistantContext(env) {
  const cached = contextCache;
  const now = Date.now();
  if (cached && cached.content && now - cached.fetchedAt < CONTEXT_CACHE_TTL_MS) {
    return cached.content;
  }

  const contextUrl = getContextUrl(env);
  if (!contextUrl) {
    return "";
  }

  try {
    const res = await fetch(contextUrl, {
      method: "GET",
      headers: { Accept: "text/markdown,text/plain;q=0.9,*/*;q=0.1" },
    });

    if (!res.ok) {
      return cached?.content || "";
    }

    const content = sanitizeContext(await res.text());
    contextCache.fetchedAt = now;
    contextCache.content = content;
    return content;
  } catch {
    return cached?.content || "";
  }
}

function shouldAttachContext(messages) {
  // "New conversation" heuristic: no assistant turns yet.
  return !messages.some((m) => m?.role === "assistant");
}

function trimAndSanitizeMessages(messages) {
  return messages
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .slice(-MAX_MESSAGES);
}

function detectLanguageFromText(text) {
  if (!text) return "zh";
  const cjkCount = (text.match(/[\u3400-\u9fff]/g) || []).length;
  const latinCount = (text.match(/[A-Za-z]/g) || []).length;
  if (cjkCount > latinCount) return "zh";
  if (latinCount > 0) return "en";
  return "zh";
}

function getResponseLanguage(responseLanguage, messages) {
  if (responseLanguage === "en" || responseLanguage === "zh") {
    return responseLanguage;
  }

  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i]?.role === "user") {
      return detectLanguageFromText(messages[i].content);
    }
  }

  return "zh";
}

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(env, request) });
    }

    if (request.method !== "POST") {
      return json({ error: "POST only" }, 405, env, request);
    }

    try {
      const body = await request.json();
      const messages = body?.messages;
      const siteModeFromBody = body?.site_mode;

      if (!Array.isArray(messages) || messages.length === 0) {
        return json({ error: "messages required" }, 400, env, request);
      }

      const origin = request.headers.get("Origin") || "";
      const referer = request.headers.get("Referer") || "";
      if (!isWikiRequest(siteModeFromBody, origin, referer)) {
        return json({ error: "This endpoint is for Openresource-Wiki only." }, 403, env, request);
      }

      const responseLanguage = getResponseLanguage(body?.response_language, messages);
      const trimmed = trimAndSanitizeMessages(messages);
      const basePrompt = getSystemPrompt(responseLanguage);
      let systemPrompt = basePrompt;

      if (shouldAttachContext(trimmed)) {
        const context = await loadAssistantContext(env);
        if (context) {
          systemPrompt = `${basePrompt}\n\n可参考的站内索引（手动维护）:\n${context}`;
        }
      }

      const res = await fetch("https://api.deepseek.com/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${env.DEEPSEEK_API_KEY}`,
        },
        body: JSON.stringify({
          model: "deepseek-chat",
          messages: [{ role: "system", content: systemPrompt }, ...trimmed],
          max_tokens: 512,
          temperature: 0.2,
          stream: false,
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        return json({ error: "DeepSeek API error", detail: text }, 502, env, request);
      }

      const data = await res.json();
      const reply = data.choices?.[0]?.message?.content || "抱歉，暂时无法回答。";

      return json({ reply }, 200, env, request);
    } catch (e) {
      return json({ error: e.message }, 500, env, request);
    }
  },
};

function corsHeaders(env, request) {
  const origin = request?.headers?.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || env.ALLOWED_ORIGIN || "").split(",").map(s => s.trim());
  const match = allowed.includes(origin) ? origin : allowed[0] || "*";
  return {
    "Access-Control-Allow-Origin": match,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function json(data, status, env, request) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders(env, request) },
  });
}
