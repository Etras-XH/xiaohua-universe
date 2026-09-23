#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
OFFICIAL = "https://www.berlinale.de/media/en/download/awards-juries/berlinale-preise-2024.pdf"
# Award/film/director data below is from the official Berlinale 2024 awards PDF.
# Chinese mappings are conservative; uncertain person-name mappings are left blank.
ADDITIONS = [
    ("旅行者的需求", "A Traveler's Needs", "洪常秀", "Hong Sangsoo", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("帝国", "The Empire", "布鲁诺·杜蒙", "Bruno Dumont", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    ("佩佩", "Pepe", "", "Nelson Carlos De Los Santos Arias", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("不同的男人", "A Different Man", "亚伦·施密伯格", "Aaron Schimberg", "最佳主角银熊奖（Sebastian Stan）", "Silver Bear for Best Leading Performance"),
    ("像这样的小事", "Small Things Like These", "蒂姆·米兰特斯", "Tim Mielants", "最佳配角银熊奖（Emily Watson）", "Silver Bear for Best Supporting Performance"),
    ("死亡乐章", "Dying", "马蒂亚斯·格拉斯纳", "Matthias Glasner", "最佳编剧银熊奖（Matthias Glasner）", "Silver Bear for Best Screenplay"),
    ("恶魔之浴", "The Devil's Bath", "维罗妮卡·弗兰茨 / 赛佛林·费奥拉", "Veronika Franz & Severin Fiala", "杰出艺术贡献银熊奖（摄影：Martin Gschlacht）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2024, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2024,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
