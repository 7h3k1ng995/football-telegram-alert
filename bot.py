import requests
import time
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
HEADERS = {
    "x-apisports-key": API_KEY
}

sent_matches = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

while True:
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        data = response.json()["response"]

        for match in data:
            fixture = match["fixture"]
            goals = match["goals"]
            teams = match["teams"]

            minute = fixture["status"]["elapsed"]
            home_goals = goals["home"]
            away_goals = goals["away"]

            if minute is None:
                continue

            score = f"{home_goals}-{away_goals}"

            if 70 <= minute <= 90 and score in ["0-0", "1-1", "2-2"]:
                match_id = fixture["id"]

                if match_id not in sent_matches:
                    sent_matches.add(match_id)

                    message = (
                        f"⚽ PARTITA INTERESSANTE\n\n"
                        f"{teams['home']['name']} vs {teams['away']['name']}\n"
                        f"⏱ Minuto: {minute}\n"
                        f"📊 Risultato: {score}"
                    )

                    send_telegram(message)

        time.sleep(120)

    except Exception as e:
        print("Errore:", e)
        time.sleep(120)
