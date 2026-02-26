let darkMode = true;

document.addEventListener('keydown', function (e) {
  if (e.key === "Enter") sendMessage()
});

function sendMessage() {
  const input = document.getElementById("messageInput");
  const text = input.value;
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      addMessage(data.response, "ai");
    });
}

function addMessage(text, sender) {
  const messages = document.getElementById("messages");

  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.innerText = text;

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

toggleTheme()
