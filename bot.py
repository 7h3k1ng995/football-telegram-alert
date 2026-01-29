import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    })

def check_matches():
    url = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            send_telegram("⚠️ TheSportsDB non risponde (status != 200)")
            return

        if not r.text.strip():
            send_telegram("⚠️ TheSportsDB risposta vuota")
            return

        data = r.json()

        events = data.get("events")
        if not events:
            send_telegram("ℹ️ Nessuna partita live ora")
            return

        for match in events:
            try:
                h = int(match["intHomeScore"])
                a = int(match["intAwayScore"])

                if (h, a) in [(0, 0), (1, 1)]:
                    msg = (
                        "⚽ MATCH LIVE\n"
                        f"{match['strHomeTeam']} vs {match['strAwayTeam']}\n"
                        f"Risultato: {h}-{a}\n"
                        f"Lega: {match.get('strLeague','?')}"
                    )
                    send_telegram(msg)
            except:
                continue

    except Exception as e:
        send_telegram(f"❌ Errore API: {e}")

@app.route("/")
def home():
    return "OK"

if __name__ == "__main__":
    send_telegram("✅ Bot avviato correttamente")
    check_matches()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
