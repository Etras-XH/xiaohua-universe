#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
OFFICIAL = "https://www.berlinale.de/en/archive/awards-juries/awards.html/a=silver-bears--all-feature-length-film/y=2021,2022/o=desc/p=1/rp=40"
# Award/film/director data below is from the official Berlinale 2022 archive.
# Chinese mappings are conservative and only included where an established title is clear.
ADDITIONS = [
    ("小说家的电影", "The Novelist's Film", "洪常秀", "Hong Sangsoo", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("宝石长袍", "Robe of Gems", "娜塔莉亚·洛佩兹·加拉多", "Natalia López Gallardo", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    ("双刃剑", "Both Sides of the Blade", "克莱尔·德尼", "Claire Denis", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("库尔纳兹诉小布什", "Rabiye Kurnaz vs. George W. Bush", "安德里亚斯·德里森", "Andreas Dresen", "最佳主角银熊奖（Meltem Kaptan）", "Silver Bear for Best Leading Performance"),
    ("娜娜", "Nana", "卡米拉·安迪妮", "Kamila Andini", "最佳配角银熊奖（Laura Basuki）", "Silver Bear for Best Supporting Performance"),
    ("库尔纳兹诉小布什", "Rabiye Kurnaz vs. George W. Bush", "安德里亚斯·德里森", "Andreas Dresen", "最佳编剧银熊奖（Laila Stieler）", "Silver Bear for Best Screenplay"),
    ("一切都会好起来", "Everything Will Be Ok", "潘礼德", "Rithy Panh", "杰出艺术贡献银熊奖（Rithy Panh、Sarit Mang）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2022, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2022,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
