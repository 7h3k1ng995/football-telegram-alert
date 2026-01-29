from flask import Flask
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

@app.route("/")
def home():
    send_telegram("✅ Ping ricevuto: Render → Telegram OK")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
