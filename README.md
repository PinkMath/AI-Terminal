<div align="center">
  <img src="./static/img/icon.jpg" height="300px" width="300px">

  # 🦦 Ferret AI
  ### Local • Privacy-First • Developer-Focused AI Assistant
</div>

---

## 🚀 What is Ferret AI?

**Ferret AI** is a fully local, privacy-first coding assistant powered by `deepseek-coder:6.7b` via Ollama.

No cloud.  
No API keys.  
No telemetry.  

Just fast, offline AI designed for developers.

Optimized for:
- 🇧🇷 Portuguese (PT-BR)
- 🇺🇸 English (EN-US) ~> (mainly language)

By default, it returns properly formatted code unless explanations are explicitly requested.

---

## 🎥 Demo

### App Interface
https://github.com/user-attachments/assets/8008f0c7-984d-419b-9b04-2ea5181f2fe9

### Terminal Interface
https://github.com/user-attachments/assets/936e1137-47c8-4c5d-8d69-8837c8ed9dd9

---

## ✨ Features

- 🖥 100% Local AI (runs entirely on your machine)
- 🔐 Privacy-first – no external APIs
- 🤖 Powered by DeepSeek-Coder 6.7B
- 📦 Automatic model detection & download
- 🎨 Color-coded terminal interface
- 🌎 Multi-language support (PT-BR & EN-US)
- 💻 Built for coding, snippets & dev assistance
- 🧠 Uses Ollama CLI for model management

---

## ⚡ Quick Start (Recommended)

```bash
git clone https://github.com/PinkMath/Ferret-AI.git
cd Ferret-AI
python app.py
```

> ⚠ Requires Ollama installed (see below)

---

# 🛠 Installation

## Option 1 — Installer (In Development)

```bash
git clone https://github.com/PinkMath/Ferret-AI.git
cd Ferret-AI
python installer.py
```

### The installer will:
- ✔ Check Python version
- ✔ Install `requests` if missing
- ✔ Check if Ollama CLI is installed
- ✔ Auto-install Ollama (Linux)
- ✔ Prompt manual install (Windows)
- ✔ Pull `deepseek-coder:6.7b` if missing

Run the app after installation:

```bash
python app.py
```

Terminal mode:

```bash
python terminalAI/AiTerminal.py
```

---

## Option 2 — Manual Installation

### Step 1 — Install Python (3.8+)

**Linux (apt):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Linux (pacman):**
```bash
sudo pacman -Sy
sudo pacman -S python python-pip
```

**Windows:**  
Download from: https://www.python.org/downloads/

---

### Step 2 — Install Dependencies

```bash
pip install requests flask
```

---

### Step 3 — Install Ollama CLI

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**  
Download the official installer:  
https://ollama.com/download/windows  

Ensure `ollama.exe` is in your PATH.

---

### Step 4 — Pull the Model

```bash
ollama pull deepseek-coder:6.7b
```

---

### Step 5 — Run Ferret AI

```bash
python app.py
```

Or terminal mode:

```bash
python terminalAI/AiTerminal.py
```

---

# 💻 Usage

Type your code request or question in the interface.

### Exit commands:
```
exit
quit
close
```

---

# 🧩 Tech Stack

- Python
- Ollama
- DeepSeek-Coder 6.7B
- Flask
- Requests

---

# 🐛 Troubleshooting

**Missing `requests` error**
```bash
pip install requests
```

**Ollama CLI not found**
- Ensure it is installed
- Ensure it is added to PATH

**Model missing**
```bash
ollama pull deepseek-coder:6.7b
```

**App not running**
- Ensure Python 3.8+
- Ensure virtual environment is activated (if using venv)

---

# 🛣 Roadmap

- [ ] GUI improvements
- [ ] Model selector support
- [ ] Config file system
- [ ] Plugin architecture
- [ ] Performance optimizations

---

# 📜 License

MIT License

---

# 🎨 Credits

Made by Flo  
YouTube: https://www.youtube.com/@djcoolflo

---

⭐ If you like the project, consider starring the repo!
