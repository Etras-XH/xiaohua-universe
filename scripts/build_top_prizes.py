#!/usr/bin/env python3
"""Build a normalized four-festival top-prize history from archival tables.

The checked-in JSON remains the runtime source. This importer is retained so the
historical batch can be audited and regenerated; each row points to the relevant
festival's official archive as its primary provenance.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-23"

CONFIG = {
    "Cannes": {
        "zh": "/tmp/cannes-zhcn.html", "en": "/tmp/cannes.html", "zh_table": 1,
        "festivalZh": "戛纳", "awardZh": "金棕榈", "awardEn": "Palme d'Or",
        "official": "https://www.festival-cannes.com/en/retrospective/{year}/awards/",
    },
    "Venice": {
        "zh": "/tmp/venice-zhcn.html", "en": "/tmp/venice.html", "zh_table": 1,
        "festivalZh": "威尼斯", "awardZh": "金狮奖", "awardEn": "Golden Lion",
        "official": "https://www.labiennale.org/en/history/recent-years",
    },
    "Berlin": {
        "zh": "/tmp/berlin-zhcn.html", "en": "/tmp/berlin.html", "zh_table": 2,
        "festivalZh": "柏林", "awardZh": "金熊奖", "awardEn": "Golden Bear",
        "official": "https://www.berlinale.de/en/archive/awards-juries/awards.html/y={year}/o=desc/p=1/rp=40",
    },
    "Locarno": {
        "zh": "/tmp/locarno-zhcn.html", "en": "/tmp/locarno.html", "zh_table": 1,
        "festivalZh": "洛迦诺", "awardZh": "金豹奖", "awardEn": "Pardo d'Oro / Golden Leopard",
        "official": "https://www.locarnofestival.ch/festival/program-archive.html",
    },
}

# Chinese and English archival tables occasionally list ex-aequo winners in a
# different order. Pairing them by row position silently cross-wires films and
# directors. These Berlin ties were checked against the Berlinale year archive
# and are pinned here so regeneration cannot reintroduce those bad mappings.
BERLIN_TIE_OVERRIDES = {
    (1990, "Larks on a String"): ("Jiří Menzel",),
    (1990, "Music Box"): ("Costa-Gavras",),
    (1985, "The Woman and the Stranger"): ("Rainer Simon",),
    (1985, "Wetherby"): ("David Hare",),
    (1983, "Ascendancy"): ("Edward Bennett",),
    (1983, "La colmena"): ("Mario Camus",),
    # Berlinale's official 1978 award archive lists three Golden Bears.
    (1978, "Las palabras de Max"): ("Emilio Martínez Lázaro",),
    (1978, "Las Truchas"): ("José Luis García Sánchez",),
    (1978, "Ascensor"): ("Tomás Muñoz",),
    (1963, "Bushido, Samurai Saga"): ("Tadashi Imai",),
    (1963, "To Bed or Not to Bed"): ("Gian Luigi Polidoro",),
}


def year_of(value: object) -> int | None:
    match = re.match(r"^\s*((?:19|20)\d{2})", str(value))
    return int(match.group(1)) if match else None


def clean_zh(value: object) -> str:
    text = str(value).replace("《", "").replace("》", "")
    text = re.sub(r"（(?:英语|法语|德语|意大利语|西班牙语|俄语|日语|丹麦语|瑞典语|"
                  r"土耳其语|葡萄牙语|波兰语|匈牙利语|捷克语|斯洛文尼亚语|印地语|"
                  r"孟加拉语|旁遮普语|荷兰语|挪威语|芬兰语|希腊语|罗马尼亚语|"
                  r"塞尔维亚语|克罗地亚语|冰岛语|波斯语|阿拉伯语)：[^）]+）", "", text)
    return re.sub(r"\[\d+\]", "", text).strip()


def usable(text: object) -> bool:
    value = str(text)
    return not any(token in value for token in ("未颁发", "没有颁", "未举办", "取消", "No award"))


def english_rows(path: str) -> dict[int, list[tuple[str, str]]]:
    by_year: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for table in pd.read_html(path):
        cols = {str(c).lower(): c for c in table.columns}
        year_col = next((c for k, c in cols.items() if k == "year"), None)
        title_col = next((c for k, c in cols.items() if "english title" in k or k == "title"), None)
        director_col = next((c for k, c in cols.items() if "director" in k or "recipient" in k), None)
        if year_col is None or title_col is None or director_col is None:
            continue
        for _, row in table.iterrows():
            year = year_of(row[year_col])
            if year and usable(row[title_col]):
                by_year[year].append((str(row[title_col]).strip(), str(row[director_col]).strip()))
    return by_year


def build() -> list[dict]:
    records: list[dict] = []
    for festival, cfg in CONFIG.items():
        zh = pd.read_html(cfg["zh"])[cfg["zh_table"]]
        en = english_rows(cfg["en"])
        positions: dict[int, int] = defaultdict(int)
        for _, row in zh.iterrows():
            year = year_of(row.iloc[0])
            if not year or not usable(row.iloc[1]):
                continue
            pos = positions[year]
            positions[year] += 1
            film_zh, director_zh = clean_zh(row.iloc[1]), clean_zh(row.iloc[3])
            film_en, director_en = en.get(year, [("", "")])[pos] if pos < len(en.get(year, [])) else ("", "")
            film_en = film_en or clean_zh(row.iloc[2])
            director_en = director_en or director_zh
            if festival == "Berlin" and (year, film_en) in BERLIN_TIE_OVERRIDES:
                director_en = BERLIN_TIE_OVERRIDES[(year, film_en)][0]
            if film_zh == "nan" or director_zh == "nan":
                continue
            tie = len([r for r in zh.itertuples(index=False) if year_of(r[0]) == year and usable(r[1])]) > 1
            records.append({
                "festival": festival, "festivalZh": cfg["festivalZh"], "year": year,
                "section": "Competition", "status": "winner", "filmZh": film_zh,
                "filmEn": film_en, "directorZh": director_zh, "directorEn": director_en,
                "awardZh": cfg["awardZh"] + ("（并列）" if tie else ""),
                "awardEn": cfg["awardEn"] + (" (Ex-aequo)" if tie else ""),
                "official": cfg["official"].format(year=year), "imdbId": "", "doubanUrl": "",
                "trailerUrl": "", "technical": {}, "checkedAt": TODAY,
            })
    return sorted(records, key=lambda r: (r["festival"], -r["year"], r["filmEn"]))


if __name__ == "__main__":
    old = json.loads((ROOT / "data/records.json").read_text())
    enriched = {(r["festival"], r["year"], r["filmEn"]): r for r in old if r["status"] == "winner"}
    rows = build()
    for row in rows:
        previous = enriched.get((row["festival"], row["year"], row["filmEn"]))
        if previous:
            for field in ("imdbId", "doubanUrl", "trailerUrl", "technical"):
                row[field] = previous.get(field, row[field])
    payload = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "data/records.json").write_text(payload)
    (ROOT / "public/data/records.json").write_text(payload)
    print(f"wrote {len(rows)} complete top-prize records")
