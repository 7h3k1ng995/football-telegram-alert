import threading
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import os

# =========================
# FLASK SERVER (OBBLIGATORIO PER RENDER)
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot attivo"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# =========================
# SCRAPING (TEST SEMPLICE)
# =========================

def scraping_loop():
    while True:
        try:
            print("Scraping in corso...")

            url = "https://www.livescore.com/en/football/live/"
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            r = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

            print("Pagina scaricata correttamente")

        except Exception as e:
            print("Errore scraping:", e)

        time.sleep(60)  # ogni 60 secondi


# =========================
# AVVIO
# =========================

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=scraping_loop).start()
