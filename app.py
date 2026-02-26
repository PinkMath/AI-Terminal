# ur own privaty AI, made by GitHub: https://github.com/PinkMath
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "http://localhost:11434/api/chat"
MODEL = "deepseek-coder:6.7b"

messages = [
    {
        "role": "system",
        "content": "You are a senior software engineer assistant."
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    messages.append({"role": "user", "content": user_input})

    response = requests.post(API_URL, json={
        "model": MODEL,
        "messages": messages,
        "stream": False
    })

    data = response.json()
    ai_message = data["message"]["content"]

    messages.append({"role": "assistant", "content": ai_message})

    return jsonify({"response": ai_message})

if __name__ == "__main__":
    app.run(debug=True)
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
