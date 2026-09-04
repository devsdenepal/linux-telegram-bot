import os

from flask import Flask, jsonify, request
from telegram import Bot

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


@app.route("/webhook", methods=["POST"])
def webhook():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return jsonify({"error": "TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set"}), 500
    data = request.json
    if data and "ref" in data and data.get("head_commit"):
        repo = data["repository"]["name"]
        commit = data["head_commit"]
        bot = Bot(token=TELEGRAM_TOKEN)
        text = (
            f"New push to {repo}:\n{commit.get('message', '')}\n{commit.get('url', '')}"
        )
        bot.send_message(chat_id=CHAT_ID, text=text)
    return "", 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "token_configured": bool(TELEGRAM_TOKEN)})


if __name__ == "__main__":
    if not TELEGRAM_TOKEN:
        print("Warning: TELEGRAM_TOKEN is not set.")
    app.run(port=os.environ.get("PORT", 5000))
