from flask import Flask, Response
import requests
import random

app = Flask(__name__)

SCOREBAT_URL = "https://www.scorebat.com/video-api/v3/"

# Risultati ammessi
ALLOWED_SCORES = ["0-0", "1-1", "2-2"]

@app.route("/")
def live_matches_test():
    try:
        r = requests.get(SCOREBAT_URL, timeout=10)
        data = r.json()

        output = []
        matches = data.get("response", [])

        for match in matches:
            home = match["title"].split(" - ")[0]
            away = match["title"].split(" - ")[1]
            competition = match["competition"]
            league = competition["name"]
            country = competition["country"]

            # 🔴 SIMULAZIONE LIVE
            minute = random.randint(70, 90)
            score = random.choice(["0-0", "1-1", "2-2", "2-1", "3-1"])

            # FILTRI
            if minute < 70 or minute > 90:
                continue
            if score not in ALLOWED_SCORES:
                continue

            msg = (
                f"⚽ LIVE {minute}'\n"
                f"{home} vs {away}\n"
                f"{league} ({country})\n"
                f"Risultato: {score}\n"
                f"------------------------"
            )

            output.append(msg)

        if not output:
            return Response(
                "Nessuna partita LIVE trovata (70–90 / 0-0 1-1 2-2)",
                mimetype="text/plain"
            )

        return Response("\n\n".join(output), mimetype="text/plain")

    except Exception as e:
        return Response(f"Errore: {e}", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
