from flask import Flask, Response
import requests
import random

app = Flask(__name__)

SCOREBAT_URL = "https://www.scorebat.com/video-api/v3/"
ALLOWED_SCORES = ["0-0", "1-1", "2-2"]

@app.route("/")
def test_live_matches():
    try:
        r = requests.get(SCOREBAT_URL, timeout=10)
        data = r.json()

        matches = data.get("response", [])
        output = []

        for match in matches:
            title = match.get("title", "Unknown match")

            # 🔴 SIMULAZIONE LIVE
            minute = random.randint(70, 90)
            score = random.choice(["0-0", "1-1", "2-2", "2-1", "3-0"])

            if score not in ALLOWED_SCORES:
                continue

            msg = (
                f"⚽ LIVE {minute}'\n"
                f"{title}\n"
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
