import os
import time
import requests
from flask import Flask

# ================= CONFIG =================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# TheSportsDB - LIVE EVENTS (Soccer)
URL_LIVE = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

CHECK_INTERVAL = 600  # 10 minuti

sent_alerts = set()

app = Flask(__name__)

# ================= TELEGRAM =================

def send_telegram(text):
    try:
        requests.post(
            TELEGRAM_URL,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=10
        )
    except:
        pass

# ================= MATCH CHECK =================

def check_matches():
    try:
        r = requests.get(URL_LIVE, timeout=15)

        if r.status_code != 200:
            send_telegram("⚠️ TheSportsDB non risponde (status != 200)")
            return

        data = r.json()
        events = data.get("events")

        if not events:
            return

        for m in events:
            try:
                hs = m.get("intHomeScore")
                as_ = m.get("intAwayScore")
                event_id = m.get("idEvent")

                if None in [hs, as_, event_id]:
                    continue

                score = f"{hs}-{as_}"

                if score not in ["0-0", "1-1", "2-2"]:
                    continue

                if event_id in sent_alerts:
                    continue

                sent_alerts.add(event_id)

                msg = (
                    "⚽ <b>LIVE ALERT</b>\n\n"
                    f"🏆 {m.get('strLeague')}\n"
                    f"{m.get('strHomeTeam')} vs {m.get('strAwayTeam')}\n"
                    f"📊 Risultato: <b>{score}</b>\n\n"
                    "👉 Valuta ingresso LTD"
                )

                send_telegram(msg)

            except:
                continue

    except:
        pass

# ================= LOOP =================

def loop():
    send_telegram("✅ Bot avviato correttamente")
    while True:
        check_matches()
        time.sleep(CHECK_INTERVAL)

# ================= FLASK =================

@app.route("/")
def home():
    return "Bot attivo"

if __name__ == "__main__":
    import threading
    threading.Thread(target=loop).start()
    app.run(host="0.0.0.0", port=10000)
