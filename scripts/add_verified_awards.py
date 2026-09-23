#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
OFFICIAL = "https://www.berlinale.de/media/en/download/awards-juries/berlinale-awards-2023.pdf"
# Award/film/director data below is from the official Berlinale 2023 awards PDF.
# Chinese mappings are conservative and only included where an established title is clear.
ADDITIONS = [
    ("红色天空", "Afire", "克里斯蒂安·佩措尔德", "Christian Petzold", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("", "Bad Living", "", "João Canijo", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    ("北斗七星", "The Plough", "菲利普·加瑞尔", "Philippe Garrel", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("两万种蜜蜂", "20,000 Species of Bees", "", "Estibaliz Urresola Solaguren", "最佳主角银熊奖（Sofía Otero）", "Silver Bear for Best Leading Performance"),
    ("直到夜尽头", "Till the End of the Night", "", "Christoph Hochhäusler", "最佳配角银熊奖（Thea Ehre）", "Silver Bear for Best Supporting Performance"),
    ("音乐", "Music", "安格拉·夏娜莱克", "Angela Schanelec", "最佳编剧银熊奖（Angela Schanelec）", "Silver Bear for Best Screenplay"),
    ("迪斯科男孩", "Disco Boy", "", "Giacomo Abbruzzese", "杰出艺术贡献银熊奖（摄影：Hélène Louvart）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2023, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2023,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
