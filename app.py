from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        # Gọi OpenAI GPT
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # có thể nâng lên gpt-4o-mini khi cần
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI tên Thắm AI, nói chuyện thân thiện và hữu ích."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = completion.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Lỗi backend: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
