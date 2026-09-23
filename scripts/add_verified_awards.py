#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/en/archive/awards-juries/awards.html/y=2021/o=desc/p=1/rp=40"
# Award/film/director data below is from the official Berlinale 2021 archive.
# Chinese mappings are conservative and only included where the established title is clear.
ADDITIONS = [
    ("倒霉性爱，发狂黄片", "Bad Luck Banging or Loony Porn", "拉杜·裘德", "Radu Jude", "金熊奖", "Golden Bear for Best Film"),
    ("偶然与想象", "Wheel of Fortune and Fantasy", "滨口龙介", "Ryusuke Hamaguchi", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("巴赫曼先生和他的学生", "Mr Bachmann and His Class", "玛利亚·施佩特", "Maria Speth", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    ("自然光线", "Natural Light", "德内斯·纳吉", "Dénes Nagy", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("我是你的人", "I'm Your Man", "玛丽亚·施拉德", "Maria Schrader", "最佳主角银熊奖（Maren Eggert）", "Silver Bear for Best Leading Performance"),
    ("森林随处可见", "Forest - I See You Everywhere", "本尼德克·菲利格夫", "Bence Fliegauf", "最佳配角银熊奖（Lilla Kizlinger）", "Silver Bear for Best Supporting Performance"),
    ("引见", "Introduction", "洪常秀", "Hong Sangsoo", "最佳编剧银熊奖（洪常秀）", "Silver Bear for Best Screenplay"),
    ("一部警察电影", "A Cop Movie", "阿隆索·帕拉西奥斯", "Alonso Ruizpalacios", "杰出艺术贡献银熊奖（剪辑：Yibrán Asuad）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2021, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2021,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
