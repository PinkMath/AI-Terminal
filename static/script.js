let darkMode = true;
let isLoading = false;

// ======= INPUT HANDLING =======
const textarea = document.getElementById("messageInput");

textarea.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// ======= SEND MESSAGE =======
async function sendMessage() {
  if (isLoading) return;

  const input = document.getElementById("messageInput");
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  input.style.height = "auto";
  textarea.disabled = true;
  isLoading = true;

  const messagesDiv = document.getElementById("messages");
  const aiMsgDiv = document.createElement("div");
  aiMsgDiv.classList.add("message", "ai");
  messagesDiv.appendChild(aiMsgDiv);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    // 2. Attach to the stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          try {
            const data = JSON.parse(line.substring(6));
            if (data.content) {
              fullText += data.content;
              
              aiMsgDiv.textContent = fullText;
              
              if (isUserNearBottom(messagesDiv)) {
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
              }
            }
          } catch (e) { console.error("Error parsing stream:", e); }
        }
      }
    }

    aiMsgDiv.textContent = ""; 
    renderFormattedMessage(aiMsgDiv, fullText);

  } catch (err) {
    console.error("Fetch error:", err);
    aiMsgDiv.textContent = "Error connecting to backend.";
  } finally {
    isLoading = false;
    textarea.disabled = false;
    textarea.focus();
  }
}
// ======= ADD MESSAGE =======
function addMessage(text, sender) {
  const messages = document.getElementById("messages");
  const div = document.createElement("div");
  div.classList.add("message", sender);

  if (sender === "ai" && text.includes("```")) {
    renderFormattedMessage(div, text);
  } else {
    div.textContent = text;
  }

  messages.appendChild(div);
  messages.scrollTo({ top: messages.scrollHeight, behavior: "smooth" });
}

// ======= TYPE AI MESSAGE =======
function typeMessage(text, div) {
  let index = 0;

  function type() {
    if (index < text.length) {
      div.textContent += text.charAt(index);
      index++;

      if (isUserNearBottom(div.parentElement)) {
        div.parentElement.scrollTop = div.parentElement.scrollHeight;
      }

      setTimeout(type, Math.random() * 15 + 10);
    } else {
      const finalText = div.textContent;
      div.textContent = "";
      renderFormattedMessage(div, finalText);

      if (isUserNearBottom(div.parentElement)) {
        div.parentElement.scrollTop = div.parentElement.scrollHeight;
      }

      isLoading = false;
      textarea.disabled = false;
      textarea.focus();
    }
  }

  type();
}

// ======= FORMAT CODE BLOCKS =======
function renderFormattedMessage(div, text) {
  const parts = text.split(/```/);

  parts.forEach((part, index) => {
    if (index % 2 === 0) {
      const span = document.createElement("span");
      span.textContent = part;
      div.appendChild(span);
    } else {
      const lines = part.split("\n");
      if (lines[0].match(/^[a-zA-Z]+$/)) lines.shift(); 
      const codeContent = lines.join("\n");

      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = codeContent;

      const copyBtn = document.createElement("button");
      copyBtn.classList.add("copy-btn");
      copyBtn.textContent = "Copy";
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(codeContent);
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
      };

      pre.appendChild(copyBtn);
      pre.appendChild(code);
      div.appendChild(pre);
    }
  });
}

// ======= SCROLL UTILITY =======
function isUserNearBottom(container, threshold = 32) {
  return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
}

// ======= THEME TOGGLE =======
function toggleTheme() {
  const moon = document.getElementById("moon");
  const sun = document.getElementById("sun");
  const button = document.getElementById("theme-button");
  darkMode = !darkMode;

  if (darkMode) {
    moon.style.display = "none";
    sun.style.display = "block";
    button.style.backgroundColor = "#ff8c00";
    document.body.style.backgroundColor = "#111b21";
  } else {
    sun.style.display = "none";
    moon.style.display = "block";
    moon.style.color = "white";
    button.style.backgroundColor = "#140d00";
    document.body.style.backgroundColor = "#f0f0f0";
  }
}

toggleTheme();
