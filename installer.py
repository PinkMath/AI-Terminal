import subprocess
import sys
import shutil
import platform
import os

MODEL = "deepseek-coder:6.7b"

# Color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def run_cmd(cmd, check=False, **kwargs):
    try:
        return subprocess.run(cmd, check=check, **kwargs)
    except FileNotFoundError:
        return None

def check_python():
    print(f"{GREEN}Python version: {sys.version.split()[0]}{RESET}")

def check_and_install_requests():
    try:
        import requests
        print(f"{GREEN}requests is already installed{RESET}")
    except ImportError:
        print(f"{YELLOW}requests not found — installing...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print(f"{GREEN}Installed requests{RESET}")

def check_ollama_cli():
    # Check if Ollama CLI is available
    if shutil.which("ollama"):
        print(f"{GREEN}Ollama CLI is installed{RESET}")
        return True
    else:
        print(f"{YELLOW}Ollama CLI not found.{RESET}")
        return False

def install_ollama_linux():
    print(f"{YELLOW}Installing Ollama on Linux...{RESET}")
    subprocess.run(["bash", "-c", "curl -fsSL https://ollama.com/install.sh | sh"], check=True)
    print(f"{GREEN}Installed Ollama{RESET}")

def prompt_install_ollama_windows():
    print(f"{YELLOW}Please install Ollama manually on Windows:{RESET}")
    print("👉 Download from https://ollama.com/download (Windows installer):contentReference[oaicite:0]{index=0}")
    print("Then re‑run this installer once Ollama is installed.")

def ensure_ollama_installed():
    if check_ollama_cli():
        return
    system = platform.system()
    if system == "Linux":
        install_ollama_linux()
    elif system == "Windows":
        prompt_install_ollama_windows()
        sys.exit(1)
    else:
        print(f"{RED}Unsupported OS for automatic install: {system}{RESET}")
        sys.exit(1)

def ensure_model_downloaded(model):
    print(f"{YELLOW}Checking for model '{model}'...{RESET}")
    list_result = run_cmd(["ollama", "list"], capture_output=True, text=True)
    if list_result and model.lower() in list_result.stdout.lower():
        print(f"{GREEN}Model '{model}' already downloaded{RESET}")
    else:
        print(f"{YELLOW}Model not detected — downloading...{RESET}")
        run_cmd(["ollama", "pull", model], check=True)
        print(f"{GREEN}Model '{model}' downloaded{RESET}")

if __name__ == "__main__":
    print(f"{GREEN}Starting environment setup...{RESET}\n")
    check_python()
    check_and_install_requests()
    ensure_ollama_installed()
    ensure_model_downloaded(MODEL)
    print(f"\n{GREEN}Setup completed — you can now run your AI code!{RESET}")
