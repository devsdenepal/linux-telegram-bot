from flask import Flask, request
from telegram import Bot

app = Flask(__name__)

TELEGRAM_TOKEN = '7768294896:AAEBtyS2YA0LOlfaCt_5vmCrXPIskw6c3gI'
CHAT_ID = 'devsdenepal'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data and 'ref' in data:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=f"New push to {data['repository']['name']}:\n{data['head_commit']['message']}\n{data['head_commit']['url']}")
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
