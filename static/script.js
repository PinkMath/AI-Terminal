// ======= STATE =======
let isLoading = false;
let currentTheme = localStorage.getItem("theme") || "dark";

// ======= DOM ELEMENTS =======
const textarea = document.getElementById("messageInput");
const messagesContainer = document.getElementById("messages");
const themeButton = document.getElementById("theme-button");
const moon = document.getElementById("moon")
const sun = document.getElementById("sun")

// ======= INITIALIZE =======
init();

function init() {
  document.documentElement.setAttribute("data-theme", currentTheme);
  setupThemeToggle();
  setupTextarea();
}

// ======= THEME TOGGLE =======
function setupThemeToggle() {
  themeButton.addEventListener("click", () => {
    currentTheme = currentTheme === "dark" ? "light" : "dark";
    if (currentTheme === "dark" ) { sun.style.display = "block"; moon.style.display = "none" }
    else if (currentTheme === "light" ) { sun.style.display = "none"; moon.style.display = "block" }
    else { sun.style.display = "block"; moon.style.display = "none" }
    document.documentElement.setAttribute("data-theme", currentTheme);
    localStorage.setItem("theme", currentTheme);
  });
}

// ======= TEXTAREA HANDLING =======
function setupTextarea() {
  textarea.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  });
}

// ======= SEND MESSAGE =======
async function sendMessage() {
  if (isLoading) return;
  const text = textarea.value.trim();
  if (!text) return;

  addMessage(text, "user");
  textarea.value = "";
  textarea.style.height = "auto";
  isLoading = true;
  textarea.disabled = true;

  const aiMsgDiv = createMessageDiv("ai");
  messagesContainer.appendChild(aiMsgDiv);

  const dotsIndicator = createTypingIndicator();
  aiMsgDiv.appendChild(dotsIndicator);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        try {
          const data = JSON.parse(line.slice(6));
          if (data.content) {
            fullText += data.content;
            aiMsgDiv.textContent = fullText + " ";
            scrollIfNearBottom(messagesContainer);
          }
        } catch(e){ console.error("Stream parse error:", e);}
      }
    }

    removeTypingIndicator(dotsIndicator);
    aiMsgDiv.textContent = "";
    renderFormattedMessage(aiMsgDiv, fullText);
    scrollIfNearBottom(messagesContainer);

  } catch (err) {
    console.error(err);
    aiMsgDiv.textContent = "Error connecting to backend.";
  } finally {
    isLoading = false;
    textarea.disabled = false;
    textarea.focus();
  }
}

// ======= MESSAGES UTILITY =======
function createMessageDiv(sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  return div;
}

function addMessage(text, sender) {
  const div = createMessageDiv(sender);
  div.textContent = text;
  messagesContainer.appendChild(div);
  scrollIfNearBottom(messagesContainer);
}

function scrollIfNearBottom(container, threshold=32){
  if(container.scrollHeight - container.scrollTop - container.clientHeight < threshold)
    container.scrollTop = container.scrollHeight;
}

// ======= TYPING DOTS =======
function createTypingIndicator(){
  const container = document.createElement("span");
  container.className = "typing-dots";
  
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    container.appendChild(dot);
  }

  return container;
}

function removeTypingIndicator(span){ span.remove(); }

// ======= CODE BLOCKS =======
function renderFormattedMessage(div, text) {
  // Regex to detect code blocks: ```[lang]? ... ```
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  let lastIndex = 0;

  let match;
  while ((match = codeBlockRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      const plainText = text.substring(lastIndex, match.index);
      div.appendChild(document.createTextNode(plainText));
    }

    const language = match[1] || ""; // optional language
    const codeContent = match[2];

    const pre = document.createElement("pre");
    const code = document.createElement("code");
    if (language) code.classList.add(language);
    code.textContent = codeContent;

    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-btn";
    copyBtn.textContent = "Copy";
    copyBtn.onclick = () => {
      navigator.clipboard.writeText(codeContent);
      copyBtn.textContent = "Copied!";
      setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
    };

    pre.append(copyBtn, code);
    div.appendChild(pre);

    lastIndex = codeBlockRegex.lastIndex;
  }

  if (lastIndex < text.length) {
    div.appendChild(document.createTextNode(text.substring(lastIndex)));
  }
}

function createCodeBlock(codeText){
  const lines = codeText.split("\n");
  if(lines[0].match(/^[a-zA-Z]+$/)) lines.shift();
  const codeContent = lines.join("\n");

  const pre = document.createElement("pre");
  const code = document.createElement("code");
  code.textContent = codeContent;

  const copyBtn = document.createElement("button");
  copyBtn.className="copy-btn";
  copyBtn.textContent="Copy";
  copyBtn.onclick = ()=>{
    navigator.clipboard.writeText(codeContent);
    copyBtn.textContent="Copied!";
    setTimeout(()=>copyBtn.textContent="Copy",1500);
  };
  pre.append(copyBtn, code);
  return pre;
}