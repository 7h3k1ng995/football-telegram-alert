import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def test_live_matches():
    url = "https://www.scorebat.com/video-api/v3/"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return f"Errore API: {response.status_code}"

    data = response.json()

    live_matches = [
        match for match in data.get("response", [])
        if match.get("competition", {}).get("is_live") is True
    ]

    if not live_matches:
        return "Nessuna partita live trovata."

    output = []
    for m in live_matches[:5]:  # limitiamo a 5 per ora
        home = m.get("title", "N/A")
        comp = m.get("competition", {}).get("name", "N/A")
        output.append(f"{home} | {comp}")

    return "<br>".join(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
