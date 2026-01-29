import time
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

URL = "https://www.espn.com/soccer/scoreboard"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_live_matches():
    print("🔍 Scraping partite live...")
    response = requests.get(URL, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        print("❌ Errore nel caricamento pagina")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    matches = soup.select("section.Scoreboard")

    if not matches:
        print("⚠️ Nessuna partita trovata")
        return

    for match in matches:
        try:
            teams = match.select("span.sb-team-short")
            score = match.select_one("span.sb-score")
            minute = match.select_one("span.sb-game-status")

            if not teams or not score or not minute:
                continue

            home = teams[0].text.strip()
            away = teams[1].text.strip()
            result = score.text.strip()
            minute_text = minute.text.strip()

            # prendiamo solo minuti tipo "78'" o "85'"
            if "'" not in minute_text:
                continue

            minute_number = int(minute_text.replace("'", ""))

            if minute_number < 70 or minute_number > 90:
                continue

            if result not in ["0-0", "1-1", "2-2"]:
                continue

            print("✅ TROVATA PARTITA")
            print(f"🏆 {home} vs {away}")
            print(f"⏱ Minuto: {minute_number}")
            print(f"⚽ Risultato: {result}")
            print("-" * 40)

        except Exception as e:
            print("Errore parsing partita:", e)

def loop():
    while True:
        scrape_live_matches()
        time.sleep(60)  # ogni 60 secondi

@app.route("/")
def home():
    return "Bot attivo"

if __name__ == "__main__":
    import threading
    threading.Thread(target=loop).start()
    app.run(host="0.0.0.0", port=10000)
