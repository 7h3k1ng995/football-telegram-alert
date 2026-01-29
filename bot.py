import os
import time
import requests
from flask import Flask

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)

# ===== TELEGRAM =====
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Errore Telegram:", e)

# ===== TEST ALL'AVVIO =====
send_telegram_message("✅ Bot avviato correttamente!\nSto monitorando le partite live.")

# ===== LOOP DI TEST =====
def loop_test():
    while True:
        print("🔍 Controllo partite live...")
        time.sleep(60)

# ===== FLASK =====
@app.route("/")
def home():
    return "Bot attivo"

if __name__ == "__main__":
    import threading
    threading.Thread(target=loop_test).start()
    app.run(host="0.0.0.0", port=10000)
