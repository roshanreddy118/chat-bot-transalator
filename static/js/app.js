let ws;
const messagesEl = document.getElementById("messages");
const btnJoin = document.getElementById("btnJoin");
const btnSend = document.getElementById("btnSend");
const inputMessage = document.getElementById("inputMessage");
const nameEl = document.getElementById("name");
const inputLangEl = document.getElementById("inputLang");
const outputLangEl = document.getElementById("outputLang");
const systemEl = document.getElementById("system");

function appendMessage(msg, className = "msg") {
  const el = document.createElement("div");
  el.className = className;
  el.innerHTML = msg;
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

btnJoin.onclick = () => {
  const name = nameEl.value.trim() || "User";
  const outputLang = outputLangEl.value || "en";

  const protocol = location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${location.host}/ws`;
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: "join", name, lang: outputLang }));
    appendMessage("✅ Connected to chat");
    inputMessage.disabled = false;
    btnSend.disabled = false;
    btnJoin.disabled = true;
  };

  ws.onmessage = (ev) => {
    const data = JSON.parse(ev.data);
    if (data.type === "system") {
      appendMessage(`<em>${data.msg}</em>`, "msg");
    } else if (data.type === "ai_chat") {
      // AI Assistant response - special styling
      appendMessage(`
        <div class="ai-response">
          <b>${data.from}:</b> 
          <div class="ai-question">${data.text}</div>
          <div class="ai-answer">${data.translated_text}</div>
          <small class="ai-lang">(Response in ${data.to_lang})</small>
        </div>
      `, "msg ai-msg");
    } else if (data.type === "chat") {
      // Regular chat message - show translation more clearly
      if (data.from_lang !== data.to_lang) {
        // Different languages - show translation
        appendMessage(`<b>${data.from}:</b> <span class='original'>${data.text}</span> <small>(${data.from_lang})</small><br><span class='translated'>📝 ${data.translated_text}</span> <small>(${data.to_lang})</small>`);
      } else {
        // Same language - just show the message
        appendMessage(`<b>${data.from}:</b> ${data.text}`);
      }
    }
  };

  ws.onclose = () => {
    appendMessage("❌ Disconnected from server");
    inputMessage.disabled = true;
    btnSend.disabled = true;
    btnJoin.disabled = false;
  };
};

btnSend.onclick = () => {
  const text = inputMessage.value.trim();
  if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;
  const inputLang = inputLangEl.value;
  ws.send(JSON.stringify({ type: "message", text, lang: inputLang }));
  inputMessage.value = "";
};

inputMessage.addEventListener("keydown", (e) => {
  if (e.key === "Enter") btnSend.click();
});
