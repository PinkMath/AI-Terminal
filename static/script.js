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
function sendMessage() {
  if (isLoading) return;

  const input = document.getElementById("messageInput");
  const text = input.value.trim();
  if (!text) return;

  // Display user message
  addMessage(text, "user");

  input.value = "";
  input.style.height = "auto";

  // Disable user input while AI types
  textarea.disabled = true;

  // Show typing indicator
  const messagesDiv = document.getElementById("messages");
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "ai");
  typingDiv.id = "typing";
  typingDiv.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  messagesDiv.appendChild(typingDiv);
  messagesDiv.scrollTo({ top: messagesDiv.scrollHeight, behavior: "smooth" });

  isLoading = true;

  // Send to backend
  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      // Start typing AI response in typingDiv
      typeMessage(data.response, typingDiv);
    })
    .catch(err => {
      console.error(err);
      isLoading = false;
      textarea.disabled = false;
      typingDiv.remove();
    });
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

      // Scroll only if user is near bottom
      if (isUserNearBottom(div.parentElement)) {
        div.parentElement.scrollTop = div.parentElement.scrollHeight;
      }

      setTimeout(type, Math.random() * 15 + 10);
    } else {
      // After typing finishes
      const finalText = div.textContent;
      div.textContent = "";
      renderFormattedMessage(div, finalText);

      // Scroll if user is near bottom
      if (isUserNearBottom(div.parentElement)) {
        div.parentElement.scrollTop = div.parentElement.scrollHeight;
      }

      // Re-enable user input
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
      if (lines[0].match(/^[a-zA-Z]+$/)) lines.shift(); // remove language
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
