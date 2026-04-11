/* ═══════════════════════════════════════
   Copy Prompt Logic
   ═══════════════════════════════════════ */

function copyPrompt(btn) {
  const container = btn && btn.closest(".prompt-block-enhanced");
  const contentNode = container && container.querySelector(".prompt-content");
  if (!contentNode) return;

  const content = contentNode.innerText;
  const write = navigator.clipboard && navigator.clipboard.writeText
    ? navigator.clipboard.writeText(content)
    : Promise.reject(new Error("clipboard_unavailable"));

  write
    .then(() => {
      const originalIcon = btn.innerHTML;
      btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4CAF50" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>';
      setTimeout(() => {
        btn.innerHTML = originalIcon;
      }, 1600);
    })
    .catch((err) => {
      console.error("无法复制:", err);
    });
}

/* ═══════════════════════════════════════
   Search + AI Chat Widget Logic
   ═══════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", function () {
  const WORKER_URL = "https://wiki-ai-chat.hougarry.workers.dev";
  const SITE_MODE = "wiki";
  const MAX_TURNS_PER_PAGE = 30;
  const TURN_COUNTER_KEY = `ai_chat_turn_count:${window.location.pathname}`;

  function softenSearchStatus() {
    const patch = () => {
      document.querySelectorAll(".md-search-result__meta").forEach((node) => {
        const text = (node.textContent || "").trim();
        if (/initializing search|正在初始化搜索/i.test(text)) {
          node.textContent = "正在准备搜索索引...";
          node.classList.add("search-meta-soft");
        }
      });
    };

    patch();

    const searchRoot = document.querySelector(".md-search");
    if (!searchRoot) return;

    const observer = new MutationObserver(patch);
    observer.observe(searchRoot, { childList: true, subtree: true, characterData: true });
  }

  softenSearchStatus();

  const chatBtn = document.getElementById("ai-chat-btn");
  const chatPanel = document.getElementById("ai-chat-panel");
  const chatClose = document.getElementById("ai-chat-close");
  const chatInput = document.getElementById("ai-chat-input");
  const chatSend = document.getElementById("ai-chat-send");
  const chatMessages = document.getElementById("ai-chat-messages");

  if (!chatBtn || !chatPanel || !chatClose || !chatInput || !chatSend || !chatMessages) {
    return;
  }

  const messages = [];
  let msgCounter = 0;
  let isSending = false;
  let introAdded = false;
  let turnCount = Number(window.sessionStorage.getItem(TURN_COUNTER_KEY) || 0);

  if (!Number.isFinite(turnCount) || turnCount < 0) {
    turnCount = 0;
  }

  const addMessage = (text, isUser = false) => {
    const id = `ai-chat-msg-${++msgCounter}`;
    const msg = document.createElement("div");
    msg.className = `ai-chat-msg ${isUser ? "ai-chat-user" : "ai-chat-assistant"}`;
    msg.id = id;
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
  };

  const removeMessage = (id) => {
    const node = document.getElementById(id);
    if (node) node.remove();
  };

  const detectUserLanguage = (text) => {
    const cjkCount = (text.match(/[\u3400-\u9fff]/g) || []).length;
    const latinCount = (text.match(/[A-Za-z]/g) || []).length;
    if (cjkCount > latinCount) return "zh";
    if (latinCount > 0) return "en";
    return "zh";
  };

  const isModelQuestion = (text) => {
    return /你.*什么模型|是什么模型|模型是什么|what model/i.test(text);
  };

  const ensureIntro = () => {
    if (introAdded) return;
    addMessage("你好，我可以帮你快速定位本站文章、提示词和技能内容。", false);
    introAdded = true;
  };

  const openPanel = () => {
    chatPanel.classList.add("open");
    chatBtn.classList.add("hidden");
    chatBtn.setAttribute("aria-expanded", "true");
    ensureIntro();
    setTimeout(() => chatInput.focus(), 30);
  };

  const closePanel = () => {
    chatPanel.classList.remove("open");
    chatBtn.classList.remove("hidden");
    chatBtn.setAttribute("aria-expanded", "false");
  };

  chatBtn.setAttribute("aria-expanded", "false");
  chatBtn.onclick = openPanel;
  chatClose.onclick = closePanel;

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && chatPanel.classList.contains("open")) {
      closePanel();
    }
  });

  const handleSend = async () => {
    const text = chatInput.value.trim();
    if (!text || isSending) return;

    if (turnCount >= MAX_TURNS_PER_PAGE) {
      addMessage(`本页会话次数已达 ${MAX_TURNS_PER_PAGE} 次，请刷新页面后继续。`, false);
      return;
    }

    isSending = true;
    chatSend.disabled = true;

    const responseLanguage = detectUserLanguage(text);
    addMessage(text, true);
    turnCount += 1;
    window.sessionStorage.setItem(TURN_COUNTER_KEY, String(turnCount));
    messages.push({ role: "user", content: text });
    chatInput.value = "";

    const typingId = addMessage("处理中...");

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const res = await fetch(WORKER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          site_mode: SITE_MODE,
          response_language: responseLanguage,
          messages,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data && data.error ? data.error : "AI 服务暂时不可用");
      }

      const reply = data.reply || "我暂时没有拿到结果，请稍后重试。";
      removeMessage(typingId);
      addMessage(reply, false);
      messages.push({ role: "assistant", content: reply });
    } catch (err) {
      removeMessage(typingId);

      if (isModelQuestion(text)) {
        const modelReply = "我是站内助手，当前通过 Cloudflare Worker 调用 DeepSeek Chat。";
        addMessage(modelReply, false);
        messages.push({ role: "assistant", content: modelReply });
      } else if (err && err.name === "AbortError") {
        addMessage("请求超时，请稍后重试。", false);
      } else {
        addMessage(`网络错误：${err.message}。请稍后重试。`, false);
      }
    } finally {
      isSending = false;
      chatSend.disabled = false;
      chatInput.focus();
    }
  };

  chatSend.onclick = handleSend;
  chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  });
});
