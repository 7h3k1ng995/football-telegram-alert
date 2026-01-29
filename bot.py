import requests
import time
import os
from flask import Flask
from threading import Thread

# ================= CONFIG =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SOFASCORE_LIVE_URL = "https://api.sofascore.com/api/v1/sport/football/events/live"
CHECK_INTERVAL = 600  # 10 minuti

SENT_ALERTS = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/"
}

# ================= FLASK =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot attivo OK"

# ================= TELEGRAM =================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    r = requests.post(url, json=payload, timeout=10)
    print("Telegram status:", r.status_code)

# ================= CORE =================
def check_matches():
    try:
        r = requests.get(SOFASCORE_LIVE_URL, headers=HEADERS, timeout=15)
        data = r.json()

        events = data.get("events", [])
        print(f"Partite LIVE trovate: {len(events)}")

        for match in events:
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]

            hg = match["homeScore"]["current"]
            ag = match["awayScore"]["current"]
            minute = match.get("time", {}).get("current", "?")

            score = f"{hg}-{ag}"
            if score not in ["0-0", "1-1", "2-2"]:
                continue

            match_id = match["id"]
            key = f"{match_id}-{score}"
            if key in SENT_ALERTS:
                continue

            league = match["tournament"]["name"]
            country = match["tournament"]["category"]["name"]

            msg = (
                f"⚽ <b>LIVE MATCH</b>\n"
                f"🏳️ {country}\n"
                f"🏆 {league}\n\n"
                f"{home} <b>{hg} - {ag}</b> {away}\n"
                f"⏱ Minuto: {minute}"
            )

            send_telegram(msg)
            SENT_ALERTS.add(key)

    except Exception as e:
        print("ERRORE:", e)

# ================= LOOP =================
def run_bot():
    send_telegram("✅ Bot avviato correttamente")
    while True:
        check_matches()
        time.sleep(CHECK_INTERVAL)

# ================= START =================
if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
