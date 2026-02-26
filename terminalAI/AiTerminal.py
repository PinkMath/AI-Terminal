# ur own privaty AI, made by GitHub: https://github.com/PinkMath
# LLM inputs
import requests
import re

API_URL = "http://localhost:11434/api/chat"
MODEL = "deepseek-coder:6.7b"  # Make sure you pulled this model

# Initialize chat history with system instructions
messages = [
    {
        "role": "system",
        "content": (
            "You are a senior software engineer assistant."
            "Only return code unless explicitly asked for explanations."
            "Your main languages are pt-br and en-us."
            "Format code in proper blocks and make it copy-paste ready."
        )
    }
]

# Color codes
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

def clean_terminal():
    print("\033[1;1H")
    print("\033[2J")

def print_code_blocks(text):
    # Detect code blocks (```python ... ```) and print them nicely.
    # Prints other text normally.

    code_block_pattern = r"```(?:\w+)?\n(.*?)```"
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    if matches:
        for block in matches:
            print(f"\n{green}--- {white}Code{green} ---\n{blue}")
            print(block.strip())
            print(f"\n{green}------------\n")
    else:
        print(text.strip())

clean_terminal()
print(f"{red}<3{blue} Ferret AI {yellow}(type 'exit','quit' or 'close' to quit){reset}")
print("----------")

while True:
    user_input = input(f"{magenta}>>>{reset} ")
    if user_input.lower() in ["exit", "quit", "close"]:
        print(f"{cyan}Exiting...{reset}")
        break

    # Add user message to chat history
    messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post(API_URL, json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        })

        data = response.json()
        ai_message = data.get("message", {}).get("content", "")

        # Print AI output, detecting code blocks
        print("\n")
        print_code_blocks(ai_message)
        print("\n")

        # Add AI message to chat history
        messages.append({"role": "assistant", "content": ai_message})

    except Exception as e:
        print(f"{red}Error:{reset}", e)
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
