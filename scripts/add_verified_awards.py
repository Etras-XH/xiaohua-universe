#!/usr/bin/env python3
"""Append Berlinale 2018 Competition awards verified against the official Berlinale archive."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
SOURCE = "https://www.berlinale.de/en/archive/awards-juries/awards.html/y=2018/o=desc/p=1/rp=40"
# Chinese mappings are conservative; uncertain mappings are left blank.
ADDITIONS = [
    ("不要碰我", "Touch Me Not", "阿迪娜·平蒂列", "Adina Pintilie", "金熊奖", "Golden Bear"),
    ("面目", "Twarz", "玛高扎塔·施莫夫兹卡", "Małgorzata Szumowska", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("女继承者", "Las herederas", "马塞洛·马蒂内斯", "Marcelo Martinessi", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("犬之岛", "Isle of Dogs", "韦斯·安德森", "Wes Anderson", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("女继承者", "Las herederas", "马塞洛·马蒂内斯", "Marcelo Martinessi", "最佳女演员银熊奖（Ana Brun）", "Silver Bear for Best Actress"),
    ("祈祷", "La prière", "塞德里克·康", "Cédric Kahn", "最佳男演员银熊奖（Anthony Bajon）", "Silver Bear for Best Actor"),
    ("博物馆", "Museo", "阿隆索·帕拉西奥斯", "Alonso Ruizpalacios", "最佳编剧银熊奖", "Silver Bear for Best Screenplay"),
    ("多甫拉托夫", "Dovlatov", "小阿列克谢·日耳曼", "Alexey German Jr.", "杰出艺术贡献银熊奖（服装与美术设计：Elena Okopnaya）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2018, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2018,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":SOURCE,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key)
        added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified Berlinale 2018 award rows")
