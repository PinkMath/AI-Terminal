let darkMode = true;

document.getElementById("messageInput")
  .addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

const textarea = document.getElementById("messageInput");

textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

function sendMessage() {
  const input = document.getElementById("messageInput");
  const text = input.value;
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  input.style.height = "auto"

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      typeMessage(data.response);
    });
}

function addMessage(text, sender) {
  const messages = document.getElementById("messages");

  const div = document.createElement("div");
  div.classList.add("message", sender);

  // Detect code blocks
  if (sender === "ai" && text.includes("```")) {
    const code = text.replace(/```[\w]*\n?|```/g, "");
    
    const pre = document.createElement("pre");
    const codeElement = document.createElement("code");
    codeElement.textContent = code;

    const copyBtn = document.createElement("button");
    copyBtn.textContent = "Copy";
    copyBtn.classList.add("copy-btn");

    copyBtn.onclick = () => {
      navigator.clipboard.writeText(code);
      copyBtn.textContent = "Copied!";
      setTimeout(() => copyBtn.textContent = "Copy", 1500);
    };

    pre.appendChild(copyBtn);
    pre.appendChild(codeElement);
    div.appendChild(pre);
  } else {
    div.textContent = text;
  }

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function toggleTheme() {
  const moon = document.getElementById('moon');
  const sun = document.getElementById('sun');
  const button = document.getElementById('theme-button');
  darkMode = !darkMode;

  if (darkMode) {
    moon.style.display = "none";
    sun.style.display = "block";
    button.style.backgroundColor = "#ff8c00"
    document.body.style.backgroundColor = "#111b21";
  } else {
    sun.style.display = "none";
    moon.style.display = "block";
    moon.style.color = "white";
    button.style.backgroundColor = "#140d00"
    document.body.style.backgroundColor = "#f0f0f0";
  }
}

function isUserNearBottom(container, threshold = 30) {
  // How far user is from bottom in pixels
  return (container.scrollHeight - container.scrollTop - container.clientHeight) < threshold;
}

function typeMessage(text) {
  const messages = document.getElementById("messages");

  const aiDiv = document.createElement("div");
  aiDiv.classList.add("message", "ai");
  messages.appendChild(aiDiv);

  let index = 0;

  function type() {
    if (index < text.length) {
      aiDiv.textContent += text.charAt(index);
      index++;

      // Auto-scroll only if user is near bottom
      if (isUserNearBottom(messages)) {
        messages.scrollTop = messages.scrollHeight;
      }

      setTimeout(type, 5);
    } else {
      // After typing finishes → re-render with code detection
      const finalText = aiDiv.textContent;
      aiDiv.textContent = "";
      renderFormattedMessage(aiDiv, finalText);

      // Scroll if user is near bottom
      if (isUserNearBottom(messages)) {
        messages.scrollTop = messages.scrollHeight;
      }
    }
  }

  type();
}

function renderFormattedMessage(div, text) {
  const parts = text.split(/```/);

  parts.forEach((part, index) => {
    // Even index = normal text
    if (index % 2 === 0) {
      const span = document.createElement("span");
      span.textContent = part;
      div.appendChild(span);
    } 
    // Odd index = code block
    else {
      const lines = part.split("\n");

      // Remove language identifier if exists
      if (lines[0].match(/^[a-zA-Z]+$/)) {
        lines.shift();
      }

      const codeContent = lines.join("\n");

      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = codeContent;

      const copyBtn = document.createElement("button");
      copyBtn.textContent = "Copy";
      copyBtn.classList.add("copy-btn");

      copyBtn.onclick = () => {
        navigator.clipboard.writeText(codeContent);
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy", 1500);
      };

      pre.appendChild(copyBtn);
      pre.appendChild(code);
      div.appendChild(pre);
    }
  });
}

toggleTheme()
