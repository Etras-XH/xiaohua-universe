#!/usr/bin/env python3
"""Append Berlinale 2019 Competition awards verified against the official awards PDF."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
SOURCE = "https://www.berlinale.de/media/download/preise-jurys/69_berlinale_awards.pdf"
# Chinese mappings are conservative; uncertain mappings are left blank.
ADDITIONS = [
    ("同义词", "Synonyms", "那达夫·拉皮德", "Nadav Lapid", "金熊奖", "Golden Bear for Best Film"),
    ("感谢上帝", "By the Grace of God", "弗朗索瓦·欧容", "François Ozon", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("系统破坏者", "System Crasher", "诺拉·芬沙伊德", "Nora Fingscheidt", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("我离家了，但……", "I Was at Home, But", "安格拉·夏娜莱克", "Angela Schanelec", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("地久天长", "So Long, My Son", "王小帅", "Wang Xiaoshuai", "最佳女演员银熊奖（咏梅）", "Silver Bear for Best Actress"),
    ("地久天长", "So Long, My Son", "王小帅", "Wang Xiaoshuai", "最佳男演员银熊奖（王景春）", "Silver Bear for Best Actor"),
    ("少年黑手党", "Piranhas", "克劳迪欧·吉瓦内斯", "Claudio Giovannesi", "最佳编剧银熊奖", "Silver Bear for Best Screenplay"),
    ("外出偷马", "Out Stealing Horses", "汉斯·皮特·莫朗", "Hans Petter Moland", "杰出艺术贡献银熊奖（摄影：Rasmus Videbæk）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2019, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2019,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":SOURCE,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key)
        added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified Berlinale 2019 award rows")
