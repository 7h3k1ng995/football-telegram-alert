from flask import Flask
import requests

app = Flask(__name__)

URL = "https://www.scorebat.com/video-api/v3/feed/?token=demo"

@app.route("/")
def home():
    try:
        r = requests.get(URL, timeout=10)
        data = r.json()

        matches = data.get("response", [])

        if not matches:
            return "Nessuna partita trovata"

        output = ""

        for match in matches:
            home = match.get("side1", {}).get("name", "N/A")
            away = match.get("side2", {}).get("name", "N/A")
            score = match.get("score", "N/A")
            minute = match.get("minute", "N/A")

            competition = match.get("competition", {})
            league = competition.get("name", "Sconosciuto")
            country = competition.get("country", "Sconosciuto")

            output += f"""⚽ LIVE
🏆 {league} ({country})
{home} - {away}
Minuto: {minute}
Risultato: {score}
----------------------
"""

        return output

    except Exception as e:
        return f"Errore: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
