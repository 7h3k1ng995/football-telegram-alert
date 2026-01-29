import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def check_matches():
    url = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"
    r = requests.get(url, timeout=10)
    data = r.json()

    if not data or not data.get("events"):
        return

    for match in data["events"]:
        try:
            home = int(match["intHomeScore"])
            away = int(match["intAwayScore"])

            if (home == 0 and away == 0) or (home == 1 and away == 1):
                league = match.get("strLeague", "Sconosciuto")
                country = match.get("strCountry", "")
                home_team = match["strHomeTeam"]
                away_team = match["strAwayTeam"]

                msg = (
                    "⚽ PARTITA LIVE\n"
                    f"{home_team} vs {away_team}\n"
                    f"Risultato: {home}-{away}\n"
                    f"Lega: {league} ({country})"
                )

                send_telegram(msg)
        except:
            continue

@app.route("/")
def home():
    return "OK"

if __name__ == "__main__":
    # test immediato all'avvio
    check_matches()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
