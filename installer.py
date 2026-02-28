import subprocess
import sys
import shutil
import platform
import os

MODEL = "deepseek-coder:6.7b"

# --- Color codes ---
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"

# --- Terminal Clearing ---
def clear_terminal_full():
    """
    Clear terminal and scrollback buffer fully, cross-platform.
    """
    if os.name == 'nt':
        os.system('cls')
        # Windows Terminal scrollback clear
        sys.stdout.write("\033[3J")
        sys.stdout.flush()
    else:
        # Unix-like: clear screen + scrollback + move cursor home
        sys.stdout.write("\033[3J\033[H\033[2J")
        sys.stdout.flush()

# --- Helper functions ---
def run_cmd(cmd, check=False, **kwargs):
    try:
        return subprocess.run(cmd, check=check, **kwargs)
    except FileNotFoundError:
        return None

def check_python(min_version=(3, 10)):
    current = sys.version_info
    print(f"{CYAN}Python version: {current.major}.{current.minor}.{current.micro}{RESET}")
    if current < min_version:
        print(f"{RED}Python {min_version[0]}.{min_version[1]}+ is required. Exiting.{RESET}")
        sys.exit(1)

def ensure_package(pkg_name):
    try:
        __import__(pkg_name)
        print(f"{GREEN}{pkg_name} is already installed{RESET}")
    except ImportError:
        print(f"{YELLOW}{pkg_name} not found — installing...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        print(f"{GREEN}Installed {pkg_name}{RESET}")

def check_ollama_cli():
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
    print("👉 Download from https://ollama.com/download (Windows installer)")
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
    result = run_cmd(["ollama", "list"], capture_output=True, text=True)
    if result and model.lower() in result.stdout.lower():
        print(f"{GREEN}Model '{model}' already downloaded{RESET}")
    else:
        print(f"{YELLOW}Model not detected — downloading...{RESET}")
        run_cmd(["ollama", "pull", model], check=True)
        print(f"{GREEN}Model '{model}' downloaded{RESET}")

# --- Main Installer ---
if __name__ == "__main__":
    clear_terminal_full()  # Clean terminal at start
    print(f"{CYAN}--- Ferret AI Environment Setup ---{RESET}\n")

    check_python(min_version=(3, 10))

    # Ensure required Python packages
    ensure_package("requests")
    ensure_package("pyperclip")  # For clipboard support

    # Ensure Ollama CLI is installed
    ensure_ollama_installed()

    # Ensure the model is downloaded
    ensure_model_downloaded(MODEL)

    print(f"\n{GREEN}✅ Setup completed successfully!{RESET}")
    print(f"{CYAN}You can now run your AI application using 'python -m ferret' or your main script.{RESET}")
