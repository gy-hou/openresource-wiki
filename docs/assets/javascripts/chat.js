/**
 * AI Wiki Chat Widget
 * Floating chat button → expandable panel → calls Cloudflare Worker
 */
(function () {
  // ← 部署 Worker 后替换这个 URL
  var WORKER_URL = "https://wiki-ai-chat.hougarry.workers.dev";

  var messages = [];
  var isOpen = false;

  // Build DOM
  var wrapper = document.createElement("div");
  wrapper.id = "ai-chat-wrapper";
  wrapper.innerHTML =
    '<button id="ai-chat-btn" title="AI 助手">' +
    '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></button>' +
    '<div id="ai-chat-panel">' +
    '<div id="ai-chat-header">' +
    '<span>🤖 AI Wiki 助手</span>' +
    '<button id="ai-chat-close">&times;</button></div>' +
    '<div id="ai-chat-messages"></div>' +
    '<div id="ai-chat-input-row">' +
    '<input id="ai-chat-input" type="text" placeholder="问我关于本站的问题..." maxlength="200">' +
    '<button id="ai-chat-send">发送</button></div></div>';

  document.body.appendChild(wrapper);

  var btn = document.getElementById("ai-chat-btn");
  var panel = document.getElementById("ai-chat-panel");
  var closeBtn = document.getElementById("ai-chat-close");
  var msgBox = document.getElementById("ai-chat-messages");
  var input = document.getElementById("ai-chat-input");
  var sendBtn = document.getElementById("ai-chat-send");

  btn.onclick = function () {
    isOpen = !isOpen;
    panel.classList.toggle("open", isOpen);
    btn.classList.toggle("hidden", isOpen);
    if (isOpen && messages.length === 0) {
      appendMsg("assistant", "你好！我是 AI Wiki 助手，可以回答关于本站内容的问题。试试问我「有什么好用的 Prompt？」");
    }
    if (isOpen) input.focus();
  };

  closeBtn.onclick = function () {
    isOpen = false;
    panel.classList.remove("open");
    btn.classList.remove("hidden");
  };

  sendBtn.onclick = doSend;
  input.onkeydown = function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      doSend();
    }
  };

  function doSend() {
    var text = input.value.trim();
    if (!text) return;
    input.value = "";
    appendMsg("user", text);
    messages.push({ role: "user", content: text });

    // Show typing indicator
    var typingId = appendMsg("assistant", "思考中...");

    fetch(WORKER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: messages }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var reply = data.reply || data.error || "抱歉，出了点问题。";
        removeMsg(typingId);
        appendMsg("assistant", reply);
        messages.push({ role: "assistant", content: reply });
      })
      .catch(function () {
        removeMsg(typingId);
        appendMsg("assistant", "网络错误，请稍后重试。");
      });
  }

  var msgCounter = 0;

  function appendMsg(role, text) {
    var id = "msg-" + ++msgCounter;
    var div = document.createElement("div");
    div.className = "ai-chat-msg ai-chat-" + role;
    div.id = id;
    div.textContent = text;
    msgBox.appendChild(div);
    msgBox.scrollTop = msgBox.scrollHeight;
    return id;
  }

  function removeMsg(id) {
    var el = document.getElementById(id);
    if (el) el.remove();
  }
})();
