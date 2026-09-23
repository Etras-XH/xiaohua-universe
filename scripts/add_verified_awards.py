#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/media/download/preise-jurys/63_berlinale_awards.pdf"
# Chinese mappings are intentionally conservative: leave unverified mappings blank
# rather than inventing a title. English titles/directors and awards come from the
# official Berlinale 2013 International Jury awards PDF.
ADDITIONS = [
    ("", "Child's Pose", "", "Călin Peter Netzer", "金熊奖", "Golden Bear"),
    ("", "An Episode in the Life of an Iron Picker", "", "Danis Tanović", "评审团大奖银熊奖", "Jury Grand Prix - Silver Bear"),
    ("", "Vic+Flo Saw a Bear", "", "Denis Côté", "阿尔弗雷德·鲍尔银熊奖", "Alfred Bauer Prize - Silver Bear"),
    ("", "Prince Avalanche", "", "David Gordon Green", "最佳导演银熊奖", "Award for Best Director - Silver Bear"),
    ("", "Gloria", "", "Sebastián Lelio", "最佳女演员银熊奖（Paulina García）", "Award for Best Actress - Silver Bear"),
    ("", "An Episode in the Life of an Iron Picker", "", "Danis Tanović", "最佳男演员银熊奖（Nazif Mujić）", "Award for Best Actor - Silver Bear"),
    ("", "Closed Curtain", "", "Jafar Panahi, Kamboziya Partovi", "最佳编剧银熊奖（Jafar Panahi）", "Award for Best Script - Silver Bear"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2013, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2013,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
