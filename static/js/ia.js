(function () {
  const chatInput = document.getElementById("chatInput");
  const chatSendBtn = document.getElementById("chatSendBtn");
  const chatMessages = document.getElementById("chatMessages");
  const quickPrompts = document.querySelectorAll(".quick-prompt");

  if (!chatInput || !chatSendBtn || !chatMessages) return;

  function getTime() {
    const now = new Date();
    return now.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function createMessage(text, role) {
    const safeText = escapeHtml(text);
    const icon =
      role === "ai"
        ? '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" x2="12" y1="19" y2="22"></line>'
        : '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>';

    const messageDiv = document.createElement("div");
    messageDiv.className = `message message-${role}`;
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">${icon}</svg>
      </div>
      <div class="message-content">
        <p>${safeText}</p>
        <p class="message-time">${getTime()}</p>
      </div>
    `;

    return messageDiv;
  }

  function sendUserMessage(rawText) {
    const text = rawText.trim();
    if (!text) return;

    chatMessages.appendChild(createMessage(text, "user"));
    chatInput.value = "";
    scrollToBottom();
    chatInput.focus();
  }

  chatSendBtn.addEventListener("click", function () {
    sendUserMessage(chatInput.value);
  });

  chatInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendUserMessage(chatInput.value);
    }
  });

  quickPrompts.forEach(function (button) {
    button.addEventListener("click", function () {
      const prompt = button.getAttribute("data-prompt") || "";
      chatInput.value = prompt;
      chatInput.focus();
    });
  });

  scrollToBottom();
  chatInput.focus();
})();
