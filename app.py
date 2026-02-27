# ur own privaty AI, made by GitHub: https://github.com/PinkMath
import json
import requests
import uuid
import os
from flask import Flask, render_template, request, Response, stream_with_context, jsonify, session
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ferret_secret_key_99"

# --- CONFIGURATION ---
API_URL = "http://localhost:11434/api/chat"
MODEL = "deepseek-coder:6.7b"

LOG_DIR = Path.home() / "logs_App"
LOG_DIR.mkdir(exist_ok=True)

PERSONA = {
    "role": "system", 
    "content": "Senior Software Engineer Assistant. Pt-br/En-us. No GIFs/Markdown images."
}

sessions_db = {}

def write_to_log(user_text: str, ai_text: str):
    filename = f"chat_{datetime.now().strftime('%Y%m%d')}.txt"
    file_path = LOG_DIR / filename
    
    with open(file_path, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%H:%M:%S")
        f.write(f"[{timestamp}] USER: {user_text}\n")
        f.write(f"[{timestamp}] AI: {ai_text}\n")
        f.write(f"{'-'*30}\n")

@app.before_request
def ensure_session():
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    if session['sid'] not in sessions_db:
        sessions_db[session['sid']] = [PERSONA]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    sid = session.get('sid')
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    sessions_db[sid].append({"role": "user", "content": user_input})

    @stream_with_context
    def generate():
        full_ai_response = ""
        try:
            response = requests.post(
                API_URL,
                json={"model": MODEL, "messages": sessions_db[sid], "stream": True},
                stream=True,
                timeout=30
            )
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        full_ai_response += content
                        yield f"data: {json.dumps({'content': content})}\n\n"

            sessions_db[sid].append({"role": "assistant", "content": full_ai_response})
            write_to_log(user_input, full_ai_response)

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    print("\n" + "="*50)
    print(f" Ferret AI Web is starting!")
    print(f" Logs are being saved to: {LOG_DIR}")
    print("="*50 + "\n")
    
    app.run(port=5000, debug=True)
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
