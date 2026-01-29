import requests
from flask import Flask
from datetime import datetime
import os

app = Flask(__name__)

# =======================
# CONFIG
# =======================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

SPORTDB_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?s=Soccer"

# =======================
# UTILS
# =======================
def check_time_window():
    now = datetime.now().hour
    return 13 <= now <= 23  # 13:00 -> 23:59


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload, timeout=10)


def get_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"{SPORTDB_URL}&d={today}", timeout=15)
    data = response.json()
    return data.get("events", [])


def check_matches():
    matches = get_matches()

    for match in matches:
        try:
            minute = match.get("intTime")
            score_home = match.get("intHomeScore")
            score_away = match.get("intAwayScore")

            if not minute or not score_home or not score_away:
                continue

            minute = int(minute)
            score_home = int(score_home)
            score_away = int(score_away)

            if minute < 70 or minute > 90:
                continue

            if score_home == score_away and score_home in [0, 1, 2]:
                league = match.get("strLeague", "Campionato sconosciuto")
                country = match.get("strCountry", "Nazione sconosciuta")
                home = match.get("strHomeTeam")
                away = match.get("strAwayTeam")

                message = (
                    "⚽ PARTITA BLOCCATA\n\n"
                    f"🏳️ {country}\n"
                    f"🏆 {league}\n"
                    f"{home} vs {away}\n"
                    f"⏱ Minuto: {minute}\n"
                    f"📊 Risultato: {score_home}-{score_away}"
                )

                send_telegram(message)

        except Exception as e:
            print("Errore match:", e)


# =======================
# ROUTE
# =======================
@app.route("/")
def home():
    try:
        if not check_time_window():
            return "OK"

        check_matches()
        return "OK"

    except Exception as e:
        print("ERRORE GENERALE:", e)
        return "OK"


# =======================
# START
# =======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
