# ur own privaty AI, made by GitHub: https://github.com/PinkMath
import json
import requests
import uuid
import os
from flask import Flask, render_template, request, Response, stream_with_context, session, jsonify
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ferret_secret_key_99"

# --- CONFIGURATION ---
API_URL = "http://localhost:11434/api/chat"
MODEL = "deepseek-coder:6.7b"

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
LOG_DIR.mkdir(parents=True, exist_ok=True)

# --- PERSONA CONFIG ---
PERSONAS = {
    "default": "Senior Software Engineer Assistant. Pt-br/En-us. No GIFs/Markdown images.",
    "friendly": "Friendly AI Assistant. Cheerful tone, Pt-br/En-us.",
    "concise": "Concise and straight to the point AI. Pt-br/En-us."
}

DEFAULT_PERSONA = {
    "role": "system",
    "content": PERSONAS["default"]
}

# --- SESSION STORAGE ---
sessions_db = {}  # key: session_id, value: messages list

# --- LOGGING FUNCTION ---
def write_to_log(session_id: str, user_text: str, ai_text: str):
    filename = f"chat_{datetime.now().strftime('%Y%m%d')}.txt"
    file_path = LOG_DIR / filename
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] SESSION: {session_id}\n")
        f.write(f"[{timestamp}] USER: {user_text}\n")
        f.write(f"[{timestamp}] AI: {ai_text}\n{'-'*40}\n")

# --- SESSION MANAGEMENT ---
@app.before_request
def ensure_session():
    """Ensure each client has a unique session ID and session history."""
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    if session['sid'] not in sessions_db:
        # Start with default persona
        sessions_db[session['sid']] = [DEFAULT_PERSONA.copy()]

# --- ROUTES ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle incoming chat messages from the client.
    Streams AI response back to client via Server-Sent Events (SSE).
    """
    sid = session.get('sid')
    user_input = request.json.get("message", "").strip()

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
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        # Strip images/GIFs if present
                        content = content.replace("![", "").replace("](", "").replace(")", "")
                        full_ai_response += content
                        # Stream chunk to client
                        yield f"data: {json.dumps({'content': content})}\n\n"
                except json.JSONDecodeError:
                    continue

            # Save AI response to session and log
            sessions_db[sid].append({"role": "assistant", "content": full_ai_response})
            write_to_log(sid, user_input, full_ai_response)

        except requests.exceptions.RequestException as e:
            yield f"data: {json.dumps({'error': f'Network error: {e}'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

# --- OPTIONAL: CHANGE PERSONA PER SESSION ---
@app.route("/persona", methods=["POST"])
def change_persona():
    sid = session.get('sid')
    persona_key = request.json.get("persona", "default").lower()
    content = PERSONAS.get(persona_key, PERSONAS["default"])
    sessions_db[sid] = [{"role": "system", "content": content}]
    return jsonify({"status": "ok", "persona": content})

# --- MAIN ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print(f" Ferret AI Web is starting!")
    print(f" Logs are being saved to: {LOG_DIR}")
    print("="*50 + "\n")
    app.run(port=5000, debug=True)
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
