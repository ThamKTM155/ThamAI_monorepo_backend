import os
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI

# Khởi tạo Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Cho phép tất cả domain gọi API

# Kết nối OpenAI (API key từ biến môi trường)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Route Chat (AI trả lời văn bản)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI thân thiện."},
                {"role": "user", "content": message},
            ],
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route TTS (chuyển văn bản thành giọng nói)
@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Tạo file tạm để lưu audio
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

        # Gọi OpenAI TTS và stream ra file
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",  # hoặc "gpt-4o-tts"
            voice="alloy",
            input=text,
        ) as response:
            response.stream_to_file(tmp_path)

        # Trả về file mp3
        return send_file(tmp_path, mimetype="audio/mpeg")

    except Exception as e:
        print("🔥 TTS error:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Route Transcribe (giọng nói -> văn bản)
@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            file.save(tmp.name)

            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=open(tmp.name, "rb"),
            )

            return jsonify({"text": transcript.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route test
@app.route("/", methods=["GET"])
def home():
    return "✅ ThamAI Backend đang chạy!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
