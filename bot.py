import requests
import os
from flask import Flask

app = Flask(__name__)

API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
HEADERS = {
    "x-apisports-key": API_KEY
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload, timeout=10)

@app.route("/")
def check_matches():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        data = response.json().get("response", [])

        for match in data:
            fixture = match["fixture"]
            goals = match["goals"]
            teams = match["teams"]

            minute = fixture["status"]["elapsed"]
            if minute is None:
                continue

            home_goals = goals["home"]
            away_goals = goals["away"]

            if 70 <= minute <= 90 and (home_goals, away_goals) in [(0,0), (1,1), (2,2)]:
                message = (
                    f"⚽ PARTITA INTERESSANTE\n\n"
                    f"{teams['home']['name']} vs {teams['away']['name']}\n"
                    f"⏱ Minuto: {minute}\n"
                    f"📊 Risultato: {home_goals}-{away_goals}"
                )
                send_telegram(message)

        return "OK"

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
