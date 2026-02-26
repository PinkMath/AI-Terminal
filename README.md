<div align="center">
  <img src="./static/img/icon.jpg" height="300px" width="300px">
  
  # Ferret AI
</div>

# Private Assistant

A local AI assistant for software development, powered by DeepSeek Coder:6.7b.
Designed for PT-BR and EN-US, returning properly formatted code unless explanations are explicitly requested.

# Features

- Local, privacy-first AI – runs entirely on your machine
- Uses Ollama CLI to manage models
- Color-coded terminal interface
- Automatic detection and downloading of required model
- Multi-language support: Portuguese & English
- Ideal for coding, snippets, and developer assistance

# Requirements

- Python 3.8+
- Ollama CLI [Download](https://ollama.com/download)
- Internet connection for first-time model download

# Installation - Using the installer (In development)
1.Clone the repository:
```bash
git clone https://github.com/PinkMath/Ferret-AI.git
cd Ferret-AI
```
2.Run the installer:
```bash
python installer.py
```
# What it does:
- Checks Python version
- Installs `requests` library if missing
- Checks if Ollama CLI is installed
- Linux: installs automatically
- Windows: prompts for manual installation
- Checks if `deepseek-coder:6.7b` is downloaded; pulls if missing

3.Once complete, run the AI:
```bash
python app.py
```
or if you want to run it in the terminal:
```bash
python terminalAI/AiTerminal.py
```

# Installation - Manual (Recommended)
Step 1 - Install python
- Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip
```
- Windows [Download Python](https://www.python.org/downloads/)
Step 2 - Install `requests` and `flask` library
```bash
pip install requests flask
```
Step 3 - nstall Ollama CLI
- Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
- Windows:
Download and run the [official installer](https://ollama.com/download/windows). Ensure ollama.exe is in your PATH.
Step 4 – Pull the DeepSeek model
```bash
ollama pull deepseek-coder:6.7b
```
Step 5 – Run AI
```bash
python app.py
```
or if you want to run it in the terminal:
```bash
python terminalAI/AiTerminal.py
```

# Usage
Type your query or code request in the terminal
Commands to exit:
```code
exit, quit, close
```

# Troubleshooting
- requests missing error: run pip install requests
- Ollama CLI not found: ensure CLI is installed and in PATH
- Model missing: run ollama pull deepseek-coder:6.7b


# Art
Made by Flo: [YouTube](https://www.youtube.com/@djcoolflo)
