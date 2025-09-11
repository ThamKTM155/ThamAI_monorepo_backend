from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# API key OpenAI (anh set trong biến môi trường hoặc .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Xin lỗi, tôi chưa nghe thấy gì."})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là ThắmAI, trợ lý AI nói tiếng Việt thân thiện."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Lỗi khi gọi AI: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
