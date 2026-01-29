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

sent_matches = set()

# =========================
# FLASK
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
    print("🔍 Controllo partite live...")

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
            minute = match.select_one(".min").get_text(strip=True)

            if "'" not in minute:
                continue

            minute_number = int(minute.replace("'", ""))

            if minute_number < 70:
                continue

            if score not in ["0-0", "1-1", "2-2"]:
                continue

            match_id = f"{teams}-{score}"

            if match_id in sent_matches:
                continue

            sent_matches.add(match_id)

            message = (
                "⚽ POSSIBILE GOL!\n\n"
                f"{teams}\n"
                f"Risultato: {score}\n"
                f"Minuto: {minute_number}'"
            )

            print("✅ ALERT:", teams, score, minute_number)
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
