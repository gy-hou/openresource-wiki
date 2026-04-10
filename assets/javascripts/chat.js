/* ═══════════════════════════════════════
   Copy Prompt Logic
   ═══════════════════════════════════════ */

function copyPrompt(btn) {
  const container = btn.closest(".prompt-block-enhanced");
  const content = container.querySelector(".prompt-content").innerText;

  navigator.clipboard.writeText(content).then(() => {
    // 视觉反馈
    const originalIcon = btn.innerHTML;
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#4CAF50" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>';
    
    setTimeout(() => {
      btn.innerHTML = originalIcon;
    }, 2000);
  }).catch(err => {
    console.error('无法复制: ', err);
  });
}

/* ═══════════════════════════════════════
   AI Chat Widget Logic
   ═══════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", function() {
  const WORKER_URL = "https://wiki-ai-chat.hougarry.workers.dev";
  const chatBtn = document.getElementById("ai-chat-btn");
  const chatPanel = document.getElementById("ai-chat-panel");
  const chatClose = document.getElementById("ai-chat-close");
  const chatInput = document.getElementById("ai-chat-input");
  const chatSend = document.getElementById("ai-chat-send");
  const chatMessages = document.getElementById("ai-chat-messages");

  if (!chatBtn || !chatPanel || !chatClose || !chatInput || !chatSend || !chatMessages) return;

  const messages = [];
  let msgCounter = 0;
  let isSending = false;

  chatBtn.onclick = () => {
    chatPanel.classList.toggle("open");
    chatBtn.classList.toggle("hidden");
  };

  chatClose.onclick = () => {
    chatPanel.classList.remove("open");
    chatBtn.classList.remove("hidden");
  };

  const addMessage = (text, isUser = false) => {
    const id = `ai-chat-msg-${++msgCounter}`;
    const msg = document.createElement("div");
    msg.className = `ai-chat-msg ${isUser ? 'ai-chat-user' : 'ai-chat-assistant'}`;
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

  const isModelQuestion = (text) => {
    return /你.*什么模型|是什么模型|模型是什么|what model/i.test(text);
  };

  const handleSend = async () => {
    const text = chatInput.value.trim();
    if (!text || isSending) return;

    isSending = true;
    addMessage(text, true);
    messages.push({ role: "user", content: text });
    chatInput.value = "";

    const typingId = addMessage("思考中...");

    try {
      const res = await fetch(WORKER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages }),
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data?.error || "AI 服务暂时不可用");
      }

      const reply = data.reply || "我暂时没有拿到结果，请稍后重试。";
      removeMessage(typingId);
      addMessage(reply, false);
      messages.push({ role: "assistant", content: reply });
    } catch (err) {
      removeMessage(typingId);
      if (isModelQuestion(text)) {
        const modelReply = "我是站点内置助手，当前通过 Cloudflare Worker 调用 DeepSeek Chat 模型。";
        addMessage(modelReply, false);
        messages.push({ role: "assistant", content: modelReply });
      } else {
        addMessage(`网络错误：${err.message}。请稍后重试。`, false);
      }
    } finally {
      isSending = false;
    }
  };

  chatSend.onclick = handleSend;
  chatInput.onkeypress = (e) => { if(e.key === 'Enter') handleSend(); };
});
