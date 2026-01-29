import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

URL = "https://www.livescore.com/en/football/live/"  # URL di test

@app.route("/")
def home():
    print("BOT AVVIATO")

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }

    response = requests.get(URL, headers=headers)

    print("STATUS CODE:", response.status_code)

    # 🔴 DEBUG: stampiamo HTML ricevuto
    html_preview = response.text[:2000]
    print("HTML PREVIEW ↓↓↓")
    print(html_preview)
    print("HTML PREVIEW ↑↑↑")

    soup = BeautifulSoup(response.text, "html.parser")

    # per ora NON cerchiamo partite
    print("PARSING COMPLETATO")

    return "Bot online - check logs"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
