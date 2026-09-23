#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/media/download/preise-jurys/66_berlinale_awards.pdf"
# Award/film/director data below is from the official Berlinale 2016 awards PDF.
# Chinese mappings are conservative and only included where the established title is clear.
ADDITIONS = [
    ("海上火焰", "Fire at Sea", "吉安弗兰科·罗西", "Gianfranco Rosi", "金熊奖", "Golden Bear for Best Film"),
    ("萨拉热窝之死", "Death in Sarajevo", "丹尼斯·塔诺维奇", "Danis Tanović", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("悲兮魔兽", "A Lullaby to the Sorrowful Mystery", "拉夫·迪亚兹", "Lav Diaz", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("将来的事", "Things to Come", "米娅·汉森-洛夫", "Mia Hansen-Løve", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("公社", "The Commune", "托马斯·温特伯格", "Thomas Vinterberg", "最佳女演员银熊奖（Trine Dyrholm）", "Silver Bear for Best Actress"),
    ("赫迪", "Hedi", "穆罕默德·本·阿提亚", "Mohamed Ben Attia", "最佳男演员银熊奖（Majd Mastoura）", "Silver Bear for Best Actor"),
    ("爱情合众国", "United States of Love", "托马斯·瓦希勒夫斯基", "Tomasz Wasilewski", "最佳编剧银熊奖（Tomasz Wasilewski）", "Silver Bear for Best Script"),
    ("长江图", "Crosscurrent", "杨超", "Yang Chao", "杰出艺术贡献银熊奖（摄影：李屏宾）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2016, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2016,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
