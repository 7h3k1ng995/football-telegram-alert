import time
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

URL = "https://www.livescore.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_live_matches():
    print("🔍 Scraping partite live...")

    response = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    matches = soup.select("div.event__match")

    if not matches:
        print("⚠️ Nessuna partita live trovata")
        return

    for match in matches:
        try:
            minute = match.select_one("div.event__stage")
            home = match.select_one("div.event__participant--home")
            away = match.select_one("div.event__participant--away")
            score_home = match.select_one("div.event__score--home")
            score_away = match.select_one("div.event__score--away")

            if not all([minute, home, away, score_home, score_away]):
                continue

            minute_text = minute.text.strip()

            if "'" not in minute_text:
                continue

            minute_number = int(minute_text.replace("'", ""))

            if minute_number < 70 or minute_number > 90:
                continue

            result = f"{score_home.text}-{score_away.text}"

            if result not in ["0-0", "1-1", "2-2"]:
                continue

            print("✅ TROVATA PARTITA")
            print(f"🏆 {home.text} vs {away.text}")
            print(f"⏱ Minuto: {minute_number}")
            print(f"⚽ Risultato: {result}")
            print("-" * 40)

        except Exception as e:
            print("Errore parsing:", e)

def loop():
    while True:
        scrape_live_matches()
        time.sleep(60)

@app.route("/")
def home():
    return "Bot attivo"

if __name__ == "__main__":
    import threading
    threading.Thread(target=loop).start()
    app.run(host="0.0.0.0", port=10000)
