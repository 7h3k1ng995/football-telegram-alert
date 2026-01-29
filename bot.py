from flask import Flask
import requests

app = Flask(__name__)

SCOREBAT_LIVE_URL = "https://www.scorebat.com/video-api/v3/feed/?token=demo"

@app.route("/")
def home():
    try:
        r = requests.get(SCOREBAT_LIVE_URL, timeout=10)
        data = r.json()

        matches = data.get("response", [])

        output = ""

        for match in matches:
            if match.get("side1") is None or match.get("side2") is None:
                continue

            # Minuto
            minute = match.get("minute")
            if minute is None:
                continue

            try:
                minute = int(minute)
            except:
                continue

            if minute < 70 or minute > 90:
                continue

            # Risultato
            score = match.get("score", "")
            if score not in ["0-0", "1-1", "2-2"]:
                continue

            home = match["side1"]["name"]
            away = match["side2"]["name"]

            competition = match.get("competition", {})
            league = competition.get("name", "Campionato sconosciuto")
            country = competition.get("country", "Nazione sconosciuta")

            output += f"""⚽ LIVE {minute}'
🏆 {league} ({country})
{home} - {away}
Risultato: {score}
------------------------
"""

        if output == "":
            return "Nessuna partita LIVE valida al momento"

        return output

    except Exception as e:
        return f"Errore: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
