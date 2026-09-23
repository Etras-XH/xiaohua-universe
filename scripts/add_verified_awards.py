#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/media/download/preise-jurys/65_berlinale_awards.pdf"
# Chinese mappings are intentionally conservative: leave unverified mappings blank.
# Award/film/director data below is from the official Berlinale 2015 awards PDF.
ADDITIONS = [
    ("出租车", "Taxi", "贾法·潘纳西", "Jafar Panahi", "金熊奖", "Golden Bear for Best Film"),
    ("神父俱乐部", "The Club", "帕布罗·拉雷恩", "Pablo Larraín", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("火山下的人生", "Ixcanul Volcano", "杰罗·布斯塔曼特", "Jayro Bustamante", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("喝彩！", "Aferim!", "拉杜·裘德", "Radu Jude", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("身体", "Body", "玛高扎塔·施莫夫兹卡", "Małgorzata Szumowska", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("45周年", "45 Years", "安德鲁·海格", "Andrew Haigh", "最佳女演员银熊奖（Charlotte Rampling）", "Silver Bear for Best Actress"),
    ("45周年", "45 Years", "安德鲁·海格", "Andrew Haigh", "最佳男演员银熊奖（Tom Courtenay）", "Silver Bear for Best Actor"),
    ("珍珠纽扣", "The Pearl Button", "帕特里西奥·古斯曼", "Patricio Guzmán", "最佳编剧银熊奖（Patricio Guzmán）", "Silver Bear for Best Script"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2015, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2015,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
