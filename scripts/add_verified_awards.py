#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
OFFICIAL = "https://www.berlinale.de/media/en/download/awards-juries/berlinale-preise-2025.pdf"
# Award/film/director data below is from the official Berlinale 2025 awards PDF.
# Chinese mappings are conservative; uncertain title/person-name mappings are left blank.
ADDITIONS = [
    ("", "The Blue Trail", "", "Gabriel Mascaro", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("", "The Message", "", "Iván Fund", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    ("", "Living the Land", "霍猛", "Huo Meng", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("", "If I Had Legs I'd Kick You", "", "Mary Bronstein", "最佳主角银熊奖（Rose Byrne）", "Silver Bear for Best Leading Performance"),
    ("", "Blue Moon", "理查德·林克莱特", "Richard Linklater", "最佳配角银熊奖（Andrew Scott）", "Silver Bear for Best Supporting Performance"),
    ("", "Kontinental '25", "拉杜·裘德", "Radu Jude", "最佳编剧银熊奖（Radu Jude）", "Silver Bear for Best Screenplay"),
    ("", "The Ice Tower", "", "Lucile Hadžihalilović", "杰出艺术贡献银熊奖（创作团队）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2025, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2025,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
