import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SPORTSDB_URL = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

SENT = set()


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload, timeout=10)


@app.route("/")
def run():
    try:
        r = requests.get(SPORTSDB_URL, timeout=15)
        data = r.json()

        if not data or "events" not in data or data["events"] is None:
            return "OK"

        for match in data["events"]:
            home = match["strHomeTeam"]
            away = match["strAwayTeam"]
            league = match["strLeague"]
            country = match.get("strCountry", "N/A")

            hs = int(match["intHomeScore"])
            as_ = int(match["intAwayScore"])

            status = match["strStatus"]
            event_id = match["idEvent"]

            if status != "Live":
                continue

            if (hs, as_) not in [(0,0), (1,1)]:
                continue

            if event_id in SENT:
                continue

            msg = (
                "🧪 TEST ALERT\n\n"
                f"🌍 {country}\n"
                f"🏆 {league}\n"
                f"{home} {hs} - {as_} {away}\n"
                "📡 LIVE"
            )

            send_telegram(msg)
            SENT.add(event_id)

        return "OK"

    except Exception as e:
        print("ERRORE:", e)
        return "OK"
