from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép frontend gọi API từ domain khác

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Trả lời giả lập (có thể thay bằng AI sau này)
    bot_reply = f"Bot nhận được: {user_message}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
