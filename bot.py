import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

THESPORTSDB_LIVE_URL = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?s=Soccer"

sent_alerts = set()  # evita doppioni


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload, timeout=10)


def check_matches():
    try:
        r = requests.get(THESPORTSDB_LIVE_URL, timeout=15)

        if r.status_code != 200:
            send_telegram("⚠️ TheSportsDB non risponde (status != 200)")
            return

        data = r.json()
        events = data.get("events")

        if not events:
            return  # nessuna partita live

        for match in events:
            try:
                minute = int(match.get("intTime", 0))
                home = match.get("strHomeTeam")
                away = match.get("strAwayTeam")
                league = match.get("strLeague")
                score_home = match.get("intHomeScore")
                score_away = match.get("intAwayScore")
                event_id = match.get("idEvent")

                if None in [score_home, score_away, event_id]:
                    continue

                score = f"{score_home}-{score_away}"

                if minute < 70 or minute > 90:
                    continue

                if score not in ["0-0", "1-1", "2-2"]:
                    continue

                if event_id in sent_alerts:
                    continue

                sent_alerts.add(event_id)

                msg = (
                    "⚽ <b>LIVE ALERT</b>\n\n"
                    f"🏆 <b>{league}</b>\n"
                    f"{home} vs {away}\n"
                    f"⏱ Minuto: {minute}\n"
                    f"📊 Risultato: <b>{score}</b>\n\n"
                    "👉 Valuta ingresso LTD"
                )

                send_telegram(msg)

            except Exception:
                continue

    except Exception as e:
        send_telegram(f"❌ Errore bot: {e}")


@app.route("/")
def home():
    return "Bot attivo", 200


@app.route("/check")
def check():
    check_matches()
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    send_telegram("✅ Bot avviato correttamente")
    app.run(host="0.0.0.0", port=10000)
