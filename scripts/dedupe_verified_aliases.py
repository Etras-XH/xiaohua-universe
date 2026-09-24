#!/usr/bin/env python3
"""Remove verified duplicate award rows caused by alternate/transliterated film titles.

This intentionally uses a small explicit canonical map rather than fuzzy matching.
The affected awards were cross-checked against Berlinale's official archive.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (festival, year, award) -> canonical English title to retain.
CANONICAL = {
    ("Berlin", 2022, "Silver Bear for Best Director"): "Both Sides of the Blade",
    ("Berlin", 2022, "Silver Bear for Best Supporting Performance"): "Before, Now & Then",
    ("Berlin", 2022, "Silver Bear for Best Leading Performance"): "Rabiye Kurnaz vs. George W. Bush",
    ("Berlin", 2022, "Silver Bear for Best Screenplay"): "Rabiye Kurnaz vs. George W. Bush",
    ("Berlin", 2022, "Silver Bear Grand Jury Prize"): "The Novelist's Film",
    ("Berlin", 2021, "Golden Bear"): "Bad Luck Banging or Loony Porn",
    ("Berlin", 2020, "Silver Bear for Best Screenplay"): "Bad Tales",
    ("Berlin", 2020, "70th Berlinale Silver Bear"): "Delete History",
    ("Berlin", 2020, "Silver Bear for Best Director"): "The Woman Who Ran",
    ("Berlin", 2020, "Silver Bear for Best Actor"): "Hidden Away",
    ("Berlin", 2020, "Golden Bear for Best Film"): "There Is No Evil",
    ("Berlin", 2017, "Golden Bear for Best Film"): "On Body and Soul",
    ("Berlin", 2016, "Golden Bear for Best Film"): "Fire at Sea",
    ("Berlin", 2015, "Golden Bear for Best Film"): "Taxi",
    ("Berlin", 2014, "Golden Bear for Best Film"): "Black Coal, Thin Ice",
}

# Older rows sometimes use a shorter award label for the same prize.
EQUIVALENT_AWARDS = {
    ("Berlin", 2021, "Golden Bear for Best Film"): ("Golden Bear", "Bad Luck Banging or Loony Porn"),
    ("Berlin", 2020, "Golden Bear"): ("Golden Bear for Best Film", "There Is No Evil"),
    ("Berlin", 2020, "Silver Bear - 70th Berlinale"): ("70th Berlinale Silver Bear", "Delete History"),
    ("Berlin", 2017, "Golden Bear"): ("Golden Bear for Best Film", "On Body and Soul"),
    ("Berlin", 2016, "Golden Bear"): ("Golden Bear for Best Film", "Fire at Sea"),
    ("Berlin", 2015, "Golden Bear"): ("Golden Bear for Best Film", "Taxi"),
    ("Berlin", 2014, "Golden Bear"): ("Golden Bear for Best Film", "Black Coal, Thin Ice"),
}


def apply(path: Path) -> int:
    rows = json.loads(path.read_text(encoding="utf-8"))
    removed = 0
    out = []
    for row in rows:
        festival, year = row.get("festival"), row.get("year")
        award, film = row.get("awardEn"), row.get("filmEn")
        eq = EQUIVALENT_AWARDS.get((festival, year, award))
        if eq:
            target_award, canonical_film = eq
            # Drop this alias row only when the canonical target exists in the dataset.
            if any(r.get("festival") == festival and r.get("year") == year and r.get("awardEn") == target_award and r.get("filmEn") == canonical_film for r in rows):
                removed += 1
                continue
        canonical = CANONICAL.get((festival, year, award))
        if canonical and film != canonical:
            # Alternate-title rows for the same verified award are duplicates.
            if any(r.get("festival") == festival and r.get("year") == year and r.get("awardEn") == award and r.get("filmEn") == canonical for r in rows):
                removed += 1
                continue
        out.append(row)

    out.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return removed


if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"removed {a} + {b} verified alias duplicates")
