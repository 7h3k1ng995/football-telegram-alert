import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask

# =========================
# CONFIG
# =========================
TELEGRAM_BOT_TOKEN = "INSERISCI_TOKEN_TELEGRAM"
TELEGRAM_CHAT_ID = "INSERISCI_CHAT_ID"

URL = "https://m.livescore.in/it/"
CHECK_INTERVAL = 300  # 5 minuti

# =========================
# FLASK (keep alive Render)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot attivo"

# =========================
# TELEGRAM
# =========================
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Errore Telegram:", e)

# =========================
# SCRAPING
# =========================
def scrape_live_matches():
    print("🔍 Scraping partite live...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(URL, headers=headers, timeout=15)
    except Exception as e:
        print("Errore richiesta:", e)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    matches = soup.select("div.row-gray, div.row-white")

    for match in matches:
        try:
            teams = match.select_one(".ply").get_text(" ", strip=True)
            score = match.select_one(".sco").get_text(strip=True)

            if score in ["0-0", "1-1", "2-2"]:
                message = (
                    "⚽ PARTITA LIVE\n"
                    f"{teams}\n"
                    f"Risultato: {score}"
                )
                print("✅ MATCH TROVATO:", teams, score)
                send_telegram_message(message)

        except Exception:
            continue

# =========================
# LOOP
# =========================
def loop():
    while True:
        scrape_live_matches()
        time.sleep(CHECK_INTERVAL)

# =========================
# START
# =========================
if __name__ == "__main__":
    t = threading.Thread(target=loop)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=10000)
