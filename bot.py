import requests
from bs4 import BeautifulSoup

URL = "https://www.flashscore.it/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}

def get_live_matches():
    response = requests.get(URL, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        return "Errore nel caricare Flashscore"

    soup = BeautifulSoup(response.text, "html.parser")

    matches = soup.select("div.event__match")

    if not matches:
        return "Nessuna partita LIVE trovata"

    risultati = []

    for match in matches:
        try:
            minute = match.select_one(".event__stage").get_text(strip=True)
            home = match.select_one(".event__participant--home").get_text(strip=True)
            away = match.select_one(".event__participant--away").get_text(strip=True)
            score_home = match.select_one(".event__score--home").get_text(strip=True)
            score_away = match.select_one(".event__score--away").get_text(strip=True)

            risultati.append(
                f"⚽ LIVE {minute}\n"
                f"{home} - {away}\n"
                f"Risultato: {score_home}-{score_away}\n"
                f"---------------------"
            )

        except:
            continue

    return "\n".join(risultati) if risultati else "Nessuna partita LIVE valida"

# endpoint Render
def application(environ, start_response):
    data = get_live_matches()
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [data.encode("utf-8")]
