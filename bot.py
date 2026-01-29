import os
import requests
from flask import Flask

app = Flask(__name__)

# ================== CONFIG ==================
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

API_URL = "https://v3.football.api-sports.io/fixtures?live=all"

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# ================== UTILS ==================
def country_flag(country):
    if not country:
        return "🏳️"
    return "".join(chr(127397 + ord(c)) for c in country.upper() if c.isalpha())


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)


# ================== MAIN LOGIC ==================
def check_matches():
    response = requests.get(API_URL, headers=HEADERS, timeout=15)
    data = response.json()

    for match in data.get("response", []):
        fixture = match["fixture"]
        league = match["league"]
        teams = match["teams"]
        goals = match["goals"]

        minute = fixture["status"]["elapsed"]
        home_goals = goals["home"]
        away_goals = goals["away"]

        if minute is None:
            continue

        if 70 <= minute <= 90:
            score = (home_goals, away_goals)

            if score in [(0,0), (1,1), (2,2)]:
                country = league.get("country", "")
                flag = country_flag(country)

                message = (
                    f"⚽ <b>LIVE ALERT</b>\n\n"
                    f"{flag} <b>{country}</b> – {league['name']}\n"
                    f"⏱️ <b>{minute}'</b>\n\n"
                    f"<b>{teams['home']['name']}</b> {home_goals} – {away_goals} <b>{teams['away']['name']}</b>\n"
                )

                send_telegram(message)


# ================== FLASK ==================
@app.route("/")
def home():
    check_matches()
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
