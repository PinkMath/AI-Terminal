# ur own AI, made by Mathus Souza, GitHub: https://github.com/PinkMath
import textwrap
import requests
import shutil
import json
import sys
import time
import threading
import os
import random
from datetime import datetime
from pathlib import Path

try:
    import pyperclip
    CLIPBOARD_ENABLED = True
except ImportError:
    CLIPBOARD_ENABLED = False

# --- LOG DIRECTORY ---
possible_paths = [
    Path.home() / "OneDrive" / "Desktop",
    Path.home() / "Desktop",
]
for path in possible_paths:
    if path.exists():
        LOG_DIR = path / "logs_App"
        break
else:
    LOG_DIR = Path.home() / "logs_App"  # Linux default

# --- CONFIGURATION ---
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

# --- STYLING ---
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
}

# --- UTILITY ---
def _print_banner():
    banner = f"""
{C['brand']}{C['bold']}
███████╗███████╗██████╗ ██████╗ ███████╗████████╗
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
█████╗  █████╗  ██████╔╝██████╔╝█████╗     ██║   
██╔══╝  ██╔══╝  ██╔══██╗██╔══██╗██╔══╝     ██║   
██║     ███████╗██║  ██║██║  ██║███████╗   ██║   
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   

          Ferret AI Terminal
{C['reset']}
"""
    print(banner)


def _typing_indicator(stop_event):
    spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{C['ai']}{spinner[i % len(spinner)]}{C['reset']} Thinking...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 30 + "\r")


def _get_terminal_width(default=80):
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


# --- AI CLASS ---
class FerretAI:
    def __init__(self):
        self.messages = []
        self.code_blocks = []  # store AI code blocks separately
        self._select_persona()
        self.log_file = os.path.join(CONFIG["log_dir"], f"chat_ID-{datetime.now().strftime('%Y%m%d')}.txt")
        self._setup_env()

    def _select_persona(self):
        print("\nSelect AI persona:")
        for key in PERSONAS:
            print(f"  {key}")
        choice = input("Persona: ").strip().lower()
        CONFIG["persona"] = PERSONAS.get(choice, list(PERSONAS.values())[0])
        self.messages.append({"role": "system", "content": CONFIG["persona"]})
        print(f"{C['ai']}Persona set: {CONFIG['persona']}{C['reset']}\n")

    def _setup_env(self):
        if not os.path.exists(CONFIG["log_dir"]):
            os.makedirs(CONFIG["log_dir"])
        os.system('cls' if os.name == 'nt' else 'clear')
        _print_banner()
        print(f"● {C['context']}Model: {CONFIG['model']}{C['reset']}")
        print(f"● {C['info']}Commands: /clear, /exit, /code, /copy <num>{C['reset']}")
        print(f"● {C['context']}Logs saving to: {CONFIG['log_dir']}{C['reset']}")
        print(f"● {C['yellow']}Tip: Use '/clear' to reset context without clearing logs{C['reset']}\n")
        greetings = ["Hey there! 👋", "What's up? 😎", "Hello, human! 🤖"]
        print(f"{C['ai']}{random.choice(greetings)}{C['reset']}\n")

    def log_interaction(self, user_text, ai_text):
        with open(self.log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(f"[{timestamp}] USER: {user_text}\n[{timestamp}] AI: {ai_text}\n{'-'*30}\n")

    def _context_bar(self, ctx_size):
        ratio = min(ctx_size / CONFIG["max_context_messages"], 1.0)
        bar_length = 12
        filled = int(bar_length * ratio)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty
        color = C['context'] if ratio <= 0.4 else C['info'] if ratio <= 0.75 else C['error']
        return f"{color}[{bar}] {int(ratio*100)}%{C['reset']}"

    # --- CODE RENDERING ---
    def _render_code_block(self, code_text, show_gutter=True):
        lines = code_text.strip().split("\n")
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        term_width = _get_terminal_width()
        gutter = f"{C['code']}│{C['reset']}"  
        max_line_width = term_width - len(gutter) - 5

        wrapped_lines = []
        for line in lines:
            wrapped_lines.extend(textwrap.wrap(line, width=max_line_width) or [""])

        if show_gutter:
            for idx, line in enumerate(wrapped_lines, start=1):
                number_str = str(idx).rjust(3)
                print(f"{gutter} {number_str} {C['light_yellow']}{line.ljust(max_line_width)}{C['reset']}")
        return "\n".join(wrapped_lines)

    # --- CHAT LOOP ---
    def chat(self):
        while True:
            try:
                ctx_size = len(self.messages) - 1
                prompt = f"{self._context_bar(ctx_size)}\n{C['prompt']} λ{C['reset']} "
                first_line = input(prompt).strip()
                if not first_line:
                    continue
                cmd = first_line.lower()

                if cmd == '/exit':
                    print(f"{C['yellow']}Signing off.{C['reset']}")
                    break
                if cmd == '/clear':
                    self.messages = [{"role": "system", "content": CONFIG["persona"]}]
                    self.code_blocks = []
                    self._setup_env()
                    print(f"{C['brand']}🗑️ Context purged. Memory fresh.{C['reset']}\n")
                    continue

                if cmd.startswith('/code'):
                    parts = first_line.split()
                    lang = parts[1] if len(parts) > 1 else ""
                    print(f"{C['brand']}Entering code mode. Type '/end' to send.{C['reset']}\n")
                    lines = []
                    while True:
                        line = input(f"{C['code']}... {C['reset']}")
                        if line.strip().lower() == "/end":
                            break
                        lines.append(line)
                    if not lines:
                        print(f"{C['yellow']}No code entered.{C['reset']}")
                        continue
                    user_input = f"```{lang}\n" + "\n".join(lines) + "\n```"

                elif cmd.startswith('/copy'):
                    if len(cmd.split()) == 2 and cmd.split()[1].isdigit():
                        idx = int(cmd.split()[1]) - 1
                        if 0 <= idx < len(self.code_blocks):
                            if CLIPBOARD_ENABLED:
                                pyperclip.copy(self.code_blocks[idx])
                                print(f"{C['green']}Copied code block {idx+1} ✅{C['reset']}")
                            else:
                                print(f"{C['yellow']}pyperclip not installed.{C['reset']}")
                        else:
                            print(f"{C['yellow']}Invalid code block number.{C['reset']}")
                    else:
                        print(f"{C['yellow']}Usage: /copy <number>{C['reset']}")
                    continue

                else:
                    user_input = first_line

                self.messages.append({"role": "user", "content": user_input})

                stop_event = threading.Event()
                spinner_thread = threading.Thread(target=_typing_indicator, args=(stop_event,))
                spinner_thread.start()

                try:
                    response = requests.post(
                        CONFIG["url"],
                        json={"model": CONFIG["model"], "messages": self.messages, "stream": True},
                        stream=True,
                        timeout=20
                    )
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    stop_event.set()
                    spinner_thread.join()
                    print(f"\n{C['error']}Network error: {e}{C['reset']}")
                    continue

                stop_event.set()
                spinner_thread.join()
                print(f"\n{C['ai']}•ᴗ•{C['reset']} ", end="")

                full_response = ""
                in_code_block = False
                code_buffer = ""

                for line in response.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line.decode("utf-8"))
                    content = chunk.get("message", {}).get("content", "")
                    full_response += content

                    while content:
                        if content.startswith("```"):
                            in_code_block = not in_code_block
                            content = content[3:]
                            if not in_code_block and code_buffer:
                                code_text = "```\n" + code_buffer + "\n```"
                                self._render_code_block(code_text)
                                self.code_blocks.append(self._render_code_block(code_text, show_gutter=False))
                                code_buffer = ""
                            continue
                        if in_code_block:
                            newline_pos = content.find("\n")
                            if newline_pos != -1:
                                code_buffer += content[:newline_pos] + "\n"
                                content = content[newline_pos+1:]
                            else:
                                code_buffer += content
                                content = ""
                        else:
                            for char in content:
                                sys.stdout.write(char)
                                sys.stdout.flush()
                                time.sleep(CONFIG["typing_speed"])
                            content = ""

                if code_buffer.strip():
                    code_text = "```\n" + code_buffer.strip() + "\n```"
                    self._render_code_block(code_text)
                    self.code_blocks.append(self._render_code_block(code_text, show_gutter=False))

                print("\n")
                self.log_interaction(user_input, full_response)
                self.messages.append({"role": "assistant", "content": full_response})

            except KeyboardInterrupt:
                print(f"\n{C['yellow']}Interrupted.{C['reset']}")
                break
            except Exception as e:
                print(f"\n{C['error']}Fault: {e}{C['reset']}\n")


if __name__ == "__main__":
    app = FerretAI()
    app.chat()