#!/usr/bin/env python3
"""Apply small, explicitly verified corrections to checked-in festival records.

Every correction/addition must be supported by an official festival archive.
Both runtime copies are updated together and duplicate award rows are avoided.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"

CORRECTIONS = {
    ("Berlin", 2002, "千与千寻"): {
        "filmEn": "Spirited Away", "directorEn": "Hayao Miyazaki",
        "directorZh": "宫崎骏",
    },
    ("Berlin", 2002, "血腥星期天"): {
        "filmEn": "Bloody Sunday", "directorEn": "Paul Greengrass",
        "directorZh": "保罗·格林格拉斯",
    },
    ("Cannes", 1993, "钢琴课"): {
        "filmEn": "The Piano", "directorEn": "Jane Campion",
        "directorZh": "简·坎皮恩", "imdbId": "tt0107822",
        "technical": {"camera": "35 mm film", "aspect": "2.35:1", "sound": "Dolby SR",
                      "source": "https://www.imdb.com/title/tt0107822/technical/"},
    },
    ("Cannes", 1993, "霸王别姬"): {
        "filmEn": "Farewell My Concubine", "directorEn": "Chen Kaige",
        "directorZh": "陈凯歌", "imdbId": "tt0106332",
        "technical": {"camera": "35 mm film", "aspect": "1.85:1", "sound": "Dolby Stereo",
                      "source": "https://www.imdb.com/title/tt0106332/technical/"},
    },
}

AWARD_CORRECTIONS = {
    ("Berlin", 1975, "Golden Bear"): {
        "filmZh": "领养", "filmEn": "Adoption",
        "directorZh": "梅萨罗什·玛尔塔", "directorEn": "Márta Mészáros",
        "official": "https://www.berlinale.de/de/archiv/chroniken/1975.html",
    },
}

# Official Berlinale 2011 chronicle explicitly names these International Jury awards.
# https://www.berlinale.de/de/archiv/chroniken/2011.html
ADDITIONS = [
    {
        "festival": "Berlin", "festivalZh": "柏林", "year": 2011,
        "section": "Competition", "status": "winner",
        "filmZh": "都灵之马", "filmEn": "The Turin Horse",
        "directorZh": "贝拉·塔尔", "directorEn": "Béla Tarr",
        "awardZh": "评审团大奖银熊奖", "awardEn": "Silver Bear Grand Jury Prize",
        "official": "https://www.berlinale.de/de/archiv/chroniken/2011.html",
        "imdbId": "", "doubanUrl": "", "trailerUrl": "", "technical": {},
        "checkedAt": CHECKED_AT,
    },
    {
        "festival": "Berlin", "festivalZh": "柏林", "year": 2011,
        "section": "Competition", "status": "winner",
        "filmZh": "沉睡的疾病", "filmEn": "Sleeping Sickness",
        "directorZh": "乌利胥·柯雷", "directorEn": "Ulrich Köhler",
        "awardZh": "最佳导演银熊奖", "awardEn": "Silver Bear for Best Director",
        "official": "https://www.berlinale.de/de/archiv/chroniken/2011.html",
        "imdbId": "", "doubanUrl": "", "trailerUrl": "", "technical": {},
        "checkedAt": CHECKED_AT,
    },
    {
        "festival": "Berlin", "festivalZh": "柏林", "year": 2011,
        "section": "Competition", "status": "winner",
        "filmZh": "血之救赎", "filmEn": "The Forgiveness of Blood",
        "directorZh": "乔舒亚·马斯顿", "directorEn": "Joshua Marston",
        "awardZh": "最佳编剧银熊奖", "awardEn": "Silver Bear for Best Screenplay",
        "official": "https://www.berlinale.de/de/archiv/chroniken/2011.html",
        "imdbId": "", "doubanUrl": "", "trailerUrl": "", "technical": {},
        "checkedAt": CHECKED_AT,
    },
    {
        "festival": "Berlin", "festivalZh": "柏林", "year": 2011,
        "section": "Competition", "status": "winner",
        "filmZh": "奖品", "filmEn": "The Prize",
        "directorZh": "宝拉·马可维奇", "directorEn": "Paula Markovitch",
        "awardZh": "杰出艺术贡献银熊奖", "awardEn": "Silver Bear for Outstanding Artistic Achievement",
        "official": "https://www.berlinale.de/de/archiv/chroniken/2011.html",
        "imdbId": "", "doubanUrl": "", "trailerUrl": "", "technical": {},
        "checkedAt": CHECKED_AT,
    },
]


def apply(path: Path) -> int:
    rows = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    seen = set()
    award_seen = set()
    for row in rows:
        key = (row.get("festival"), row.get("year"), row.get("filmZh"))
        patch = CORRECTIONS.get(key)
        if patch:
            seen.add(key)
        else:
            award_key = (row.get("festival"), row.get("year"), row.get("awardEn"))
            patch = AWARD_CORRECTIONS.get(award_key)
            if patch:
                award_seen.add(award_key)
        if not patch:
            continue
        before = json.dumps(row, ensure_ascii=False, sort_keys=True)
        row.update(patch)
        row["checkedAt"] = CHECKED_AT
        changed += before != json.dumps(row, ensure_ascii=False, sort_keys=True)

    missing = set(CORRECTIONS) - seen
    missing_awards = set(AWARD_CORRECTIONS) - award_seen
    if missing or missing_awards:
        raise RuntimeError(f"expected records not found: exact={sorted(missing)}, awards={sorted(missing_awards)}")

    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    for addition in ADDITIONS:
        key = (addition["festival"], addition["year"], addition["filmEn"], addition["awardEn"])
        if key not in existing:
            rows.append(addition.copy())
            existing.add(key)
            changed += 1

    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"corrected/added {a} + {b} records")
