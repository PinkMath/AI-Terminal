# ur own privaty AI, made by GitHub: https://github.com/PinkMath
import json
import uuid
import requests
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, Response, stream_with_context, session, jsonify

# =====================================================
# APP CONFIG
# =====================================================

app = Flask(__name__)
app.secret_key = "ferret_secret_key_99"

API_URL = "http://localhost:11434/api/chat"
MODEL = "deepseek-coder:6.7b"
MAX_LOG_CHARS = 12000

# =====================================================
# LOG DIRECTORY
# =====================================================

def get_log_directory() -> Path:
    for base in (Path.home() / "OneDrive" / "Desktop", Path.home() / "Desktop"):
        if base.exists():
            log_dir = base / "logs_Ferret"
            log_dir.mkdir(parents=True, exist_ok=True)
            return log_dir

    log_dir = Path.home() / "logs_Ferret"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


LOG_DIR = get_log_directory()

# =====================================================
# DEFAULT SYSTEM MESSAGE
# =====================================================

DEFAULT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Senior Software Engineer Assistant. Pt-br/En-us. "
        "No GIFs or Markdown images. Emojis allowed."
    ),
}

# =====================================================
# IN-MEMORY SESSION STORE
# =====================================================

sessions_db = {}

# =====================================================
# LOGGING
# =====================================================

def write_to_log(session_id: str, user_text: str, ai_text: str):
    filename = f"chat_app_{datetime.now():%Y%m%d}.txt"
    file_path = LOG_DIR / filename
    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] USER: {user_text}\n"
            f"[{timestamp}] AI: {ai_text}\n"
            + "-" * 40 + "\n"
        )


def read_log_file(filename: str):
    if not filename.endswith(".txt"):
        return None, "Only .txt files are allowed."

    safe_path = (LOG_DIR / filename).resolve()

    if not str(safe_path).startswith(str(LOG_DIR.resolve())):
        return None, "Invalid file path."

    if not safe_path.exists():
        return None, "Log file not found."

    try:
        return safe_path.read_text(encoding="utf-8"), None
    except Exception as e:
        return None, str(e)

# =====================================================
# SESSION MANAGEMENT
# =====================================================

@app.before_request
def ensure_session():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())

    if session["sid"] not in sessions_db:
        sessions_db[session["sid"]] = [DEFAULT_SYSTEM_MESSAGE.copy()]

# =====================================================
# MODEL STREAMING (REUSABLE)
# =====================================================

def stream_model(messages, timeout=30, save_to_session=False, sid=None, user_input=None):
    @stream_with_context
    def generate():
        full_response = ""

        try:
            response = requests.post(
                API_URL,
                json={"model": MODEL, "messages": messages, "stream": True},
                stream=True,
                timeout=timeout,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    chunk = json.loads(line.decode("utf-8"))
                    content = chunk.get("message", {}).get("content", "")

                    if content:
                        content = content.replace("![", "").replace("](", "").replace(")", "")
                        full_response += content
                        yield f"data: {json.dumps({'content': content})}\n\n"

                except json.JSONDecodeError:
                    continue

            if save_to_session and sid:
                sessions_db[sid].append({"role": "assistant", "content": full_response})
                write_to_log(sid, user_input, full_response)

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype="text/event-stream")

# =====================================================
# COMMAND HANDLER
# =====================================================

def handle_log_command(user_input: str, sid: str):
    parts = user_input.strip().split(maxsplit=1)

    # /log → list files
    if len(parts) == 1:
        logs = sorted(f.name for f in LOG_DIR.glob("*.txt"))
        if not logs:
            return jsonify({"type": "system", "content": "No log files found."})
        return jsonify({
            "type": "system",
            "content": "Available logs:\n" + "\n".join(logs),
        })

    # /log filename.txt
    filename = parts[1]
    log_content, error = read_log_file(filename)

    if error:
        return jsonify({"type": "system", "content": f"Error: {error}"})

    log_content = log_content[-MAX_LOG_CHARS:]

    temp_messages = [
        *sessions_db[sid],
        {
            "role": "system",
            "content": (
                "Analyze this application log. "
                "Summarize key events, detect errors, and highlight patterns."
            ),
        },
        {"role": "user", "content": log_content},
    ]

    return stream_model(temp_messages, timeout=60)

# =====================================================
# ROUTES
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    sid = session.get("sid")
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    # -------- /log command --------
    if user_input.lower().startswith("/log"):
        return handle_log_command(user_input, sid)

    # -------- Normal Chat --------
    sessions_db[sid].append({"role": "user", "content": user_input})

    return stream_model(
        sessions_db[sid],
        timeout=30,
        save_to_session=True,
        sid=sid,
        user_input=user_input,
    )

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(" Ferret AI Web is starting!")
    print(f" Logs directory: {LOG_DIR}")
    print("=" * 50 + "\n")

    app.run(port=5000, debug=True)
# ur own privaty AI, made by GitHub: https://github.com/PinkMath
