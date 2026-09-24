#!/usr/bin/env python3
"""Append 2012 Berlinale Competition awards verified against the official Berlinale archive."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.berlinale.de/en/archive/awards-juries/awards.html/a=silver-bears--all-feature-length-film/y=2012/o=desc/p=1/rp=40"
CHECKED_AT = "2026-09-24"

AWARDS = [
    ("凯撒必须死", "Caesar Must Die", "保罗·塔维亚尼 / 维托里奥·塔维亚尼", "Paolo Taviani / Vittorio Taviani", "金熊奖", "Golden Bear"),
    ("只是风", "Just the Wind", "本斯·弗利高夫", "Bence Fliegauf", "评审团大奖银熊奖", "Jury Grand Prix - Silver Bear"),
    ("芭芭拉", "Barbara", "克里斯蒂安·佩措尔德", "Christian Petzold", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("战地巫师", "War Witch", "阮金", "Kim Nguyen", "最佳女演员银熊奖（Rachel Mwanza）", "Silver Bear for Best Actress"),
    ("皇室风流史", "A Royal Affair", "尼科莱·阿尔赛", "Nikolaj Arcel", "最佳男演员银熊奖（Mikkel Boe Følsgaard）", "Silver Bear for Best Actor"),
    ("皇室风流史", "A Royal Affair", "尼科莱·阿尔赛", "Nikolaj Arcel", "最佳编剧银熊奖（Nikolaj Arcel、Rasmus Heisterberg）", "Silver Bear for Best Script"),
    ("白鹿原", "White Deer Plain", "王全安", "Wang Quan'an", "杰出艺术贡献银熊奖（摄影：Lutz Reitemeier）", "Silver Bear for Outstanding Artistic Contribution"),
    ("山上的孩子", "Sister", "乌苏拉·梅尔", "Ursula Meier", "特别银熊奖", "Special Award Silver Bear"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in AWARDS:
        key = ("Berlin", 2012, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2012,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":SOURCE,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key)
        added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified Berlinale 2012 award rows")
