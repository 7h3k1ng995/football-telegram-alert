import requests
from flask import Flask

TELEGRAM_TOKEN = "INSERISCI_TOKEN"
CHAT_ID = "INSERISCI_CHAT_ID"

app = Flask(__name__)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    r = requests.post(url, json=payload)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

@app.route("/")
def home():
    return "Bot attivo", 200

if __name__ == "__main__":
    print("Avvio bot...")
    send_telegram_message("🚀 Test Render → Telegram")
    app.run(host="0.0.0.0", port=10000)
