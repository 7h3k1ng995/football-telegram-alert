import os
import time
import threading
import requests
from flask import Flask

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SPORTSDB_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?s=Soccer"

app = Flask(__name__)
already_sent = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

def check_matches():
    while True:
        try:
            r = requests.get(SPORTSDB_URL, timeout=10)

            if r.status_code != 200 or not r.text.strip():
                print("Risposta API vuota")
                time.sleep(600)
                continue

            data = r.json()
            events = data.get("events")

            if not events:
                print("Nessun evento")
                time.sleep(600)
                continue

            for e in events:
                home = e.get("strHomeTeam")
                away = e.get("strAwayTeam")
                home_goals = e.get("intHomeScore")
                away_goals = e.get("intAwayScore")
                event_id = e.get("idEvent")

                if home_goals is None or away_goals is None:
                    continue

                if event_id in already_sent:
                    continue

                if (
                    (home_goals == "0" and away_goals == "0") or
                    (home_goals == "1" and away_goals == "1")
                ):
                    msg = (
                        f"⚽ PARTITA LIVE\n"
                        f"{home} {home_goals} - {away_goals} {away}"
                    )
                    send_telegram(msg)
                    already_sent.add(event_id)

            time.sleep(600)

        except Exception as e:
            print("Errore:", e)
            time.sleep(600)

@app.route("/")
def home():
    return "OK"

if __name__ == "__main__":
    threading.Thread(target=check_matches, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
