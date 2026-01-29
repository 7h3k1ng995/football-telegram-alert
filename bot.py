import os
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# ================= TELEGRAM =================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SPORTDB_URL = "https://api.sportdb.dev/football/live"

sent_matches = set()  # evita doppioni


def country_flag(country):
    if not country:
        return "🏳️"
    return "".join(chr(127397 + ord(c)) for c in country.upper() if c.isalpha())


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })


def check_time_window():
    hour = datetime.now().hour
    return true


def check_matches():
    if not check_time_window():
        return

    r = requests.get(SPORTDB_URL, timeout=15)
    data = r.json()

    for match in data.get("matches", []):
        home = match.get("home")
        away = match.get("away")
        score = match.get("score", "")

        if not home or not away or "-" not in score:
            continue

        try:
            hg, ag = map(int, score.split("-"))
        except:
            continue

        if (hg, ag) not in [(0,0), (1,1), (2,2)]:
            continue

        match_id = f"{home}-{away}-{score}"
        if match_id in sent_matches:
            continue

        league = match.get("competition", "Unknown League")
        country = match.get("country", "")
        flag = country_flag(country)

        message = (
            f"⚽ LIVE ALERT\n\n"
            f"{flag} {country} – {league}\n"
            f"⏱️ LIVE\n\n"
            f"{home} {hg} – {ag} {away}"
        )

        send_telegram(message)
        sent_matches.add(match_id)


@app.route("/")
def home():
    check_matches()
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
