#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/en/archive/awards-juries/awards.html/a=silver-bears--all-feature-length-film/y=2012/o=desc/p=1/rp=40"
ADDITIONS = [
    ("只是风", "Csak a szél", "本斯·弗利高夫", "Bence Fliegauf", "评审团大奖银熊奖", "Jury Grand Prix - Silver Bear"),
    ("芭芭拉", "Barbara", "克里斯蒂安·佩措尔德", "Christian Petzold", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("战地巫师", "Rebelle", "金·诺古依", "Kim Nguyen", "最佳女演员银熊奖（Rachel Mwanza）", "Silver Bear for Best Actress"),
    ("皇室风流史", "En kongelig affære", "尼科莱·阿尔赛", "Nikolaj Arcel", "最佳男演员银熊奖（Mikkel Boe Følsgaard）", "Silver Bear for Best Actor"),
    ("皇室风流史", "En kongelig affære", "尼科莱·阿尔赛", "Nikolaj Arcel", "最佳编剧银熊奖", "Silver Bear for Best Script"),
    ("白鹿原", "Bai lu yuan", "王全安", "Wang Quan'an", "杰出艺术贡献银熊奖（摄影：Lutz Reitemeier）", "Silver Bear for Outstanding Artistic Contribution"),
    ("山上的孩子", "L’enfant d’en haut", "乌苏拉·梅尔", "Ursula Meier", "特别银熊奖", "Special Award Silver Bear"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    # Repair a previously staged title if a workflow raced this correction.
    for r in rows:
        if r.get("festival") == "Berlin" and r.get("year") == 2012 and r.get("filmEn") == "Csak a szél":
            r["filmZh"] = "只是风"
            r["checkedAt"] = CHECKED_AT
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2012, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2012,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
