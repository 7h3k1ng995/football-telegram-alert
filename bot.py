import requests
import time
import os

# ====== CONFIG ======
TELEGRAM_TOKEN = "INSERISCI_TOKEN"
CHAT_ID = "INSERISCI_CHAT_ID"
# ====================

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    send_telegram_message("✅ Test OK: bot Render + Telegram funzionano!")
    time.sleep(5)
