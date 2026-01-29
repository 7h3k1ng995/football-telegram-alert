import os
import requests
from flask import Flask

app = Flask(__name__)

# ====== VARIABILI AMBIENTE ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ====== FUNZIONE TELEGRAM ======
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# ====== TEST BOT ======
def check_matches():
    send_telegram("✅ TEST OK\nIl bot è attivo e risponde alle richieste.")

# ====== ROUTE WEB ======
@app.route("/")
def home():
    check_matches()
    return "Bot is running"

# ====== AVVIO ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
