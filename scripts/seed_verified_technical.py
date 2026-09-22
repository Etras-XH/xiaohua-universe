import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / "data/records.json").read_text())
known = {
    "Farewell My Concubine": {
        "camera": "35 mm film",
        "aspect": "1.85:1",
        "sound": "Dolby Stereo",
        "source": "https://www.imdb.com/title/tt0106332/technical/",
    },
    "The Piano": {
        "camera": "35 mm film",
        "aspect": "2.35:1",
        "sound": "Dolby SR",
        "source": "https://www.imdb.com/title/tt0107822/technical/",
    },
    "Parasite §": {
        "camera": "ARRI Alexa 65",
        "aspect": "2.39:1",
        "sound": "Dolby Atmos",
        "source": "https://www.imdb.com/title/tt6751668/technical/",
    },
}
for row in rows:
    if row.get("filmEn") in known:
        row["technical"] = known[row["filmEn"]]
        row["imdbId"] = row["imdbId"] or known[row["filmEn"]]["source"].split("/title/")[1].split("/")[0]
payload = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
(root / "data/records.json").write_text(payload)
(root / "public/data/records.json").write_text(payload)
print("seeded", sum(bool(r.get("technical")) for r in rows), "verified technical records")
