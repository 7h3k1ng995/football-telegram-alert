import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.flashscore.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_live_matches():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []

    for match in soup.select("div.event__match"):
        try:
            status = match.select_one(".event__stage").text.strip()
            if not status.isdigit():
                continue

            minute = int(status)
            if minute < 70 or minute > 90:
                continue

            home = match.select_one(".event__participant--home").text.strip()
            away = match.select_one(".event__participant--away").text.strip()

            home_score = match.select_one(".event__score--home").text.strip()
            away_score = match.select_one(".event__score--away").text.strip()

            score = f"{home_score}-{away_score}"

            if score not in ["0-0", "1-1", "2-2"]:
                continue

            matches.append(
                f"⚽ LIVE {minute}'\n{home} - {away}\nRisultato: {score}"
            )

        except Exception:
            continue

    return matches


print("🚀 Bot avviato correttamente")

while True:
    try:
        partite = get_live_matches()

        if partite:
            print("\n".join(partite))
        else:
            print("Nessuna partita valida al momento")

    except Exception as e:
        print("Errore:", e)

    # aspetta 120 secondi
    time.sleep(120)
