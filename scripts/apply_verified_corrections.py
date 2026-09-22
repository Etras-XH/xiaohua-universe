#!/usr/bin/env python3
"""Apply small, explicitly verified corrections to checked-in festival records.

Keep this file conservative: every correction must be supported by an official
festival archive. It updates both runtime copies and never creates new rows.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-23"

# Official Berlinale 2002 awards PDF:
# https://www.berlinale.de/media/download/preise-jurys/52_ifb_preise_2002.pdf
# Official Cannes archive confirms the joint 1993 Palme d'Or winners:
# https://www.festival-cannes.com/en/2026/ba-wang-bie-ji-farewell-my-concubine-by-chen-kaige-when-peking-opera-was-still-alive/
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
        "technical": {
            "camera": "35 mm film", "aspect": "2.35:1", "sound": "Dolby SR",
            "source": "https://www.imdb.com/title/tt0107822/technical/",
        },
    },
    ("Cannes", 1993, "霸王别姬"): {
        "filmEn": "Farewell My Concubine", "directorEn": "Chen Kaige",
        "directorZh": "陈凯歌", "imdbId": "tt0106332",
        "technical": {
            "camera": "35 mm film", "aspect": "1.85:1", "sound": "Dolby Stereo",
            "source": "https://www.imdb.com/title/tt0106332/technical/",
        },
    },
}


def apply(path: Path) -> int:
    rows = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    seen = set()
    for row in rows:
        key = (row.get("festival"), row.get("year"), row.get("filmZh"))
        patch = CORRECTIONS.get(key)
        if not patch:
            continue
        seen.add(key)
        before = json.dumps(row, ensure_ascii=False, sort_keys=True)
        row.update(patch)
        row["checkedAt"] = CHECKED_AT
        after = json.dumps(row, ensure_ascii=False, sort_keys=True)
        changed += before != after
    missing = set(CORRECTIONS) - seen
    if missing:
        raise RuntimeError(f"expected records not found: {sorted(missing)}")
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"corrected {a} + {b} records")
