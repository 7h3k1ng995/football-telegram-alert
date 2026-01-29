import requests
import time
import os
from flask import Flask

# ========= CONFIG =========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SOFASCORE_LIVE_URL = "https://api.sofascore.com/api/v1/sport/football/events/live"

CHECK_INTERVAL = 600  # 10 minuti
SENT_ALERTS = set()   # evita duplicati

# ========= FLASK =========
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot live OK"

# ========= TELEGRAM =========
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload, timeout=10)

# ========= CORE LOGIC =========
def check_matches():
    try:
        r = requests.get(SOFASCORE_LIVE_URL, timeout=15)

        if r.status_code != 200:
            print("❌ Sofascore non risponde:", r.status_code)
            return

        data = r.json()
        events = data.get("events", [])

        for match in events:
            try:
                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]

                home_goals = match["homeScore"]["current"]
                away_goals = match["awayScore"]["current"]

                minute = match.get("time", {}).get("current", "?")

                score = f"{home_goals}-{away_goals}"

                if score not in ["0-0", "1-1", "2-2"]:
                    continue

                match_id = match["id"]
                alert_key = f"{match_id}-{score}"

                if alert_key in SENT_ALERTS:
                    continue

                tournament = match["tournament"]["name"]
                country = match["tournament"]["category"]["name"]

                message = (
                    f"⚽ <b>LIVE MATCH</b>\n"
                    f"🏳️ {country}\n"
                    f"🏆 {tournament}\n\n"
                    f"{home} <b>{home_goals} - {away_goals}</b> {away}\n"
                    f"⏱ Minuto: {minute}"
                )

                send_telegram(message)
                SENT_ALERTS.add(alert_key)

            except Exception as e:
                print("Errore partita:", e)

    except Exception as e:
        print("Errore generale:", e)

# ========= LOOP =========
def run_bot():
    while True:
        check_matches()
        time.sleep(CHECK_INTERVAL)

# ========= START =========
if __name__ == "__main__":
    from threading import Thread

    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
