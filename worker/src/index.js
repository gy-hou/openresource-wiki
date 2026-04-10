/**
 * AI Chat — Cloudflare Worker proxy for DeepSeek API
 * Serves both Openresource-Wiki and academic homepage.
 *
 * Secrets (set via `wrangler secret put`):
 *   DEEPSEEK_API_KEY
 *
 * Environment vars (in wrangler.toml):
 *   ALLOWED_ORIGINS
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

const ACADEMIC_PROMPT_EN = `You are the AI assistant for Lucas's academic homepage (gy-hou.github.io).

About Lucas:
- Student at USTC (University of Science and Technology of China)
- Research interests: AI, Fintech, LLM applications
- Projects: TrendR (AI-powered literature review), OpenClaw (AI tool collection), Openresource-Wiki (open-source knowledge sharing)
- Active on Xiaohongshu (小红书) sharing AI tools & tutorials
- GitHub: github.com/gy-hou
- Model backend: DeepSeek Chat API, proxied through Cloudflare Worker

What you can help with:
- Questions about Lucas's research, projects, and publications
- Information about the site's content (news, projects, CV, blog)
- General academic inquiries related to AI and Fintech

Known publications currently listed on the site:
1) Problems and Countermeasures of Industrial Investment Funds in China's New Economic Phase
   - Journal: Journal of Regional Financial Research
   - Year: 2020
2) Research on the Influencing Factors of Subsidy Thresholds for Government-Guided Venture Capital Funds
   - Journal: Review of Investment Studies (CSSCI)
   - Year: 2021

Rules:
- Reply in English only
- Be friendly, concise, and professional
- Don't fabricate publications, grades, or details not on the site
- Keep answers under 200 words
- If asked about "your model", explicitly say you use DeepSeek Chat via Cloudflare Worker proxy
- For detailed inquiries, suggest contacting Lucas directly`;

const MAX_MESSAGES = 10;

function safePathnameFromUrl(rawUrl) {
  if (!rawUrl) return "";
  try {
    const parsed = new URL(rawUrl);
    return parsed.pathname || "";
  } catch {
    return "";
  }
}

function getSiteMode(siteMode, origin, referer) {
  const refererPath = safePathnameFromUrl(referer);
  const fromWikiPath = refererPath === "/openresource-wiki" || refererPath.startsWith("/openresource-wiki/");
  const fromWikiOrigin = !!(origin && origin.includes("openresource-wiki"));

  // Headers are more trustworthy than client-provided body flags.
  if (fromWikiPath || fromWikiOrigin) {
    return "wiki";
  }

  if (siteMode === "wiki" || siteMode === "academic") {
    return siteMode;
  }

  return "academic";
}

function getSystemPrompt(siteMode, responseLanguage) {
  if (siteMode === "wiki") {
    return responseLanguage === "en" ? WIKI_PROMPT_EN : WIKI_PROMPT_ZH;
  }
  return ACADEMIC_PROMPT_EN;
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
      const responseLanguage = getResponseLanguage(body?.response_language, messages);
      const siteMode = getSiteMode(siteModeFromBody, origin, referer);
      const systemPrompt = getSystemPrompt(siteMode, responseLanguage);
      const trimmed = trimAndSanitizeMessages(messages);

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
