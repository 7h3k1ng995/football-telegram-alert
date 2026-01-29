import requests
from bs4 import BeautifulSoup

URL = "https://www.livescore.in/it/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def test_scraping():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    print("STATUS CODE:", r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("div.event__match")
    print("PARTITE TROVATE:", len(rows))

    for row in rows[:5]:
        home = row.select_one(".event__participant--home")
        away = row.select_one(".event__participant--away")
        score = row.select_one(".event__score")
        minute = row.select_one(".event__stage")

        if home and away and score and minute:
            print(
                f"{minute.text.strip()} | "
                f"{home.text.strip()} {score.text.strip()} {away.text.strip()}"
            )

if __name__ == "__main__":
    test_scraping()
