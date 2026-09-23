#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"
OFFICIAL = "https://www.berlinale.de/media/download/preise-jurys/64_berlinale_awards.pdf"
# Chinese mappings are intentionally conservative: leave unverified mappings blank.
# Award/film/director data below is from the official Berlinale 2014 awards PDF.
ADDITIONS = [
    ("白日焰火", "Black Coal, Thin Ice", "刁亦男", "Diao Yinan", "金熊奖", "Golden Bear for Best Film"),
    ("布达佩斯大饭店", "The Grand Budapest Hotel", "韦斯·安德森", "Wes Anderson", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    ("", "Life of Riley", "", "Alain Resnais", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
    ("少年时代", "Boyhood", "理查德·林克莱特", "Richard Linklater", "最佳导演银熊奖", "Silver Bear for Best Director"),
    ("小小的家", "The Little House", "山田洋次", "Yoji Yamada", "最佳女演员银熊奖（Haru Kuroki）", "Silver Bear for Best Actress"),
    ("白日焰火", "Black Coal, Thin Ice", "刁亦男", "Diao Yinan", "最佳男演员银熊奖（Liao Fan）", "Silver Bear for Best Actor"),
    ("苦路十四站", "Stations of the Cross", "迪特里希·布鲁格曼", "Dietrich Brüggemann", "最佳编剧银熊奖（Dietrich Brüggemann, Anna Brüggemann）", "Silver Bear for Best Script"),
    ("推拿", "Blind Massage", "娄烨", "Lou Ye", "杰出艺术贡献银熊奖（摄影：Zeng Jian）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", 2014, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":2014,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":OFFICIAL,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
