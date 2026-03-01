import os
from pathlib import Path

# --- LOG DIRECTORY ---
possible_paths = [
    Path.home() / "OneDrive" / "Desktop",
    Path.home() / "Desktop",
]

for path in possible_paths:
    if path.exists():
        LOG_DIR = path / "logs_Ferret"
        break
else:
    LOG_DIR = Path.home() / "logs_Ferret"

CONFIG = {
    "url": "http://localhost:11434/api/chat",
    "model": "deepseek-coder:6.7b",
    "log_dir": LOG_DIR,
    "persona": "",  
    "max_context_messages": 100,
    "typing_speed": 0.005,
    "max_code_lines": 20,
}

PERSONAS = {
    "friendly": "Cheerful and encouraging AI. Responds in an upbeat tone. 😊",
    "witty": "AI with sarcastic and witty remarks. 😏",
    "concise": "AI that gives short, to-the-point answers. ⚡",
}

C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "brand": "\033[38;5;141m",
    "prompt": "\033[38;5;45m",
    "context": "\033[38;5;75m",
    "ai": "\033[38;5;82m",
    "code": "\033[38;5;51m",
    "info": "\033[38;5;220m",
    "error": "\033[38;5;196m",
    "yellow": "\033[33m",
    "light_yellow": "\033[1;33m",
    "green": "\033[38;5;118m",
    "cyan": "\033[36m",
}
# ur own AI, made by Mathus Souza, GitHub: https://github.com/PinkMath
