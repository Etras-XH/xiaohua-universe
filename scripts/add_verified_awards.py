#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/media/download/preise-jurys/67_berlinale_awards.pdf"
# Award/film/director data below is from the official Berlinale 2017 awards PDF.
# Chinese mappings are conservative and only included where the established title is clear.
ADDITIONS = [
    ("肉与灵", "On Body and Soul", "伊尔蒂科·茵叶蒂", "Ildikó Enyedi", "金熊奖", "Golden Bear for Best Film"),
    ("菲丽希缇", "Félicité", "阿兰·戈米斯", "Alain Gomis", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("糜骨之壤", "Spoor", "阿格涅丝卡·霍兰", "Agnieszka Holland", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("希望的另一面", "The Other Side of Hope", "阿基·考里斯马基", "Aki Kaurismäki", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("独自在夜晚的海边", "On the Beach at Night Alone", "洪常秀", "Hong Sangsoo", "最佳女演员银熊奖（金敏喜）", "Silver Bear for Best Actress"),
    ("明亮的夜", "Bright Nights", "托马斯·阿斯兰", "Thomas Arslan", "最佳男演员银熊奖（Georg Friedrich）", "Silver Bear for Best Actor"),
    ("普通女人", "A Fantastic Woman", "塞巴斯蒂安·莱里奥", "Sebastián Lelio", "最佳编剧银熊奖（Sebastián Lelio、Gonzalo Maza）", "Silver Bear for Best Screenplay"),
    ("安娜，我的爱", "Ana, mon amour", "卡林·皮特·内策尔", "Călin Peter Netzer", "杰出艺术贡献银熊奖（剪辑：Dana Bunescu）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2017, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2017,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
