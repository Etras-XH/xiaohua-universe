#!/usr/bin/env python3
"""Append Berlinale 2020 Competition awards verified against the official awards PDF."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
SOURCE = "https://www.berlinale.de/media/en/download/awards-juries/berlinale-awards-2020.pdf"
# Chinese mappings are conservative; uncertain mappings are left blank.
ADDITIONS = [
    ("没有邪恶", "There Is No Evil", "穆罕默德·拉索罗夫", "Mohammad Rasoulof", "金熊奖", "Golden Bear for Best Film"),
    ("从不，很少，有时，总是", "Never Rarely Sometimes Always", "伊丽莎·希特曼", "Eliza Hittman", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("逃走的女人", "The Woman Who Ran", "洪常秀", "Hong Sangsoo", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("温蒂妮", "Undine", "克里斯蒂安·佩措尔德", "Christian Petzold", "最佳女演员银熊奖（Paula Beer）", "Silver Bear for Best Actress"),
    ("我想藏起来", "Hidden Away", "乔治奥·迪里蒂", "Giorgio Diritti", "最佳男演员银熊奖（Elio Germano）", "Silver Bear for Best Actor"),
    ("烂故事", "Bad Tales", "达米亚诺·迪诺森佐 / 法比欧·迪诺森佐", "Damiano D'Innocenzo & Fabio D'Innocenzo", "最佳编剧银熊奖", "Silver Bear for Best Screenplay"),
    ("列夫·朗道：娜塔莎", "DAU. Natasha", "伊利亚·赫尔扎诺夫斯基 / 叶卡特琳娜·奥特尔", "Ilya Khrzhanovsky & Jekaterina Oertel", "杰出艺术贡献银熊奖（摄影：Jürgen Jürges）", "Silver Bear for Outstanding Artistic Contribution"),
    ("删除历史", "Delete History", "伯努瓦·德雷平 / 古斯塔弗·科文", "Benoît Delépine & Gustave Kervern", "第70届柏林电影节特别银熊奖", "70th Berlinale Silver Bear"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2020, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2020,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":SOURCE,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key)
        added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified Berlinale 2020 award rows")
