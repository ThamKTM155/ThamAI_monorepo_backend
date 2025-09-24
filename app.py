from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép tất cả domain gọi API

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Trả lời giả lập (anh có thể thay bằng gọi OpenAI API sau này)
    if user_message.strip() == "":
        reply_text = "Bạn chưa nhập nội dung."
    else:
        reply_text = f"Bot nhận được: {user_message}"

    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
