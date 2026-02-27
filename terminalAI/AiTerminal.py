# ur own privaty AI, made by GitHub: https://github.com/PinkMath
import requests
import json
import sys
import time
import os
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
CONFIG = {
    "url": "http://localhost:11434/api/chat",
    "model": "deepseek-coder:6.7b",
    "log_dir": Path.home() / "logs_Term",
    "persona": "Senior Full-stack Engineer. Expert in Python, Rust, and Architecture. Responds in Pt-br/En-us.",
    "typing_speed": 0.005 
}

# --- STYLING ---
C = {
    "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
    "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
    "white": "\033[37m", "bold": "\033[1m", "reset": "\033[0m"
}

class FerretAI:
    def __init__(self):
        self.messages = [{"role": "system", "content": CONFIG["persona"]}]
        self.log_file = os.path.join(CONFIG["log_dir"], f"chat_{datetime.now().strftime('%Y%m%d')}.txt")
        self._setup_env()

    def _setup_env(self):
        if not os.path.exists(CONFIG["log_dir"]):
            os.makedirs(CONFIG["log_dir"])
            
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{C['magenta']}{C['bold']}Ferret AI | {CONFIG['model']}{C['reset']}")
        print(f"{C['yellow']}Commands: /clear, /exit{C['reset']}")
        print(f"{C['blue']}Logs saving to: {CONFIG['log_dir']}{C['reset']}\n")

    def log_interaction(self, user_text, ai_text):
        with open(self.log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(f"[{timestamp}] USER: {user_text}\n[{timestamp}] AI: {ai_text}\n{'-'*30}\n")

    def chat(self):
        while True:
            try:
                ctx_size = len(self.messages) - 1
                user_input = input(f"{C['blue']}[{ctx_size}]{C['reset']} {C['cyan']}λ{C['reset']} ").strip()
                
                if not user_input: continue
                cmd = user_input.lower()
                
                if cmd in ['/exit']: 
                    print(f"{C['yellow']}Signing off.{C['reset']}")
                    break
                
                if cmd == '/clear':
                    self.messages = [{"role": "system", "content": CONFIG["persona"]}]
                    self._setup_env()
                    print(f"{C['magenta']}✨ Context purged. Memory fresh.{C['reset']}\n")
                    continue

                self.messages.append({"role": "user", "content": user_input})
                
                response = requests.post(
                    CONFIG["url"],
                    json={"model": CONFIG["model"], "messages": self.messages, "stream": True},
                    stream=True
                )
                response.raise_for_status()

                print(f"\n{C['green']}Assistant:{C['reset']} ", end="")
                
                full_response = ""
                in_code_block = False
                backtick_count = 0
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        content = chunk.get("message", {}).get("content", "")
                        
                        for char in content:
                            if char == '`':
                                backtick_count += 1
                            else:
                                if backtick_count >= 3:
                                    in_code_block = not in_code_block
                                    color = (C['bold'] + C['cyan']) if in_code_block else C['green']
                                    sys.stdout.write(C['reset'] + color)
                                backtick_count = 0

                            sys.stdout.write(char)
                            sys.stdout.flush()
                            time.sleep(CONFIG["typing_speed"])
                        
                        full_response += content

                print(C['reset'] + "\n") 
                self.log_interaction(user_input, full_response)
                self.messages.append({"role": "assistant", "content": full_response})

            except KeyboardInterrupt:
                print(f"\n{C['yellow']}Interrupted.{C['reset']}")
                break
            except Exception as e:
                print(f"\n{C['red']}Fault: {e}{C['reset']}\n")

if __name__ == "__main__":
    app = FerretAI()
    app.chat()
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
