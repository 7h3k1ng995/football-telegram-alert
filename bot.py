import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def test_api():
    url = "https://www.scorebat.com/video-api/v3/"

    r = requests.get(url, timeout=10)
    data = r.json()

    matches = data.get("response", [])

    if not matches:
        return "Nessuna partita trovata"

    output = []
    for m in matches[:10]:
        title = m.get("title", "N/A")
        competition = m.get("competition", "N/A")
        date = m.get("date", "N/A")

        output.append(f"{title} | {competition} | {date}")

    return "<br>".join(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
