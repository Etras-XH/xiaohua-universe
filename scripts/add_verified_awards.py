#!/usr/bin/env python3
"""Append only festival award rows verified against official archives."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"
SOURCES = {
    2025: "https://www.berlinale.de/media/en/download/awards-juries/berlinale-preise-2025.pdf",
    2024: "https://www.berlinale.de/media/en/download/awards-juries/berlinale-preise-2024.pdf",
    2023: "https://www.berlinale.de/media/en/download/awards-juries/berlinale-awards-2023.pdf",
    2022: "https://www.berlinale.de/en/archive/awards-juries/awards.html/a=silver-bears--all-feature-length-film/y=2021,2022/o=desc/p=1/rp=40",
    2021: "https://b2b.berlinale.de/en/partner/postings/1307-the-award-winners-of-the-competition",
}
# Award/film/director data below is from official Berlinale awards archives/PDFs.
# Chinese mappings are conservative; uncertain title/person-name mappings are left blank.
ADDITIONS = [
    (2025, "", "The Blue Trail", "", "Gabriel Mascaro", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    (2025, "", "The Message", "", "Iván Fund", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    (2025, "", "Living the Land", "霍猛", "Huo Meng", "最佳导演银熊奖", "Silver Bear for Best Director"),
    (2025, "", "If I Had Legs I'd Kick You", "", "Mary Bronstein", "最佳主角银熊奖（Rose Byrne）", "Silver Bear for Best Leading Performance"),
    (2025, "", "Blue Moon", "理查德·林克莱特", "Richard Linklater", "最佳配角银熊奖（Andrew Scott）", "Silver Bear for Best Supporting Performance"),
    (2025, "", "Kontinental '25", "拉杜·裘德", "Radu Jude", "最佳编剧银熊奖（Radu Jude）", "Silver Bear for Best Screenplay"),
    (2025, "", "The Ice Tower", "", "Lucile Hadžihalilović", "杰出艺术贡献银熊奖（创作团队）", "Silver Bear for Outstanding Artistic Contribution"),
    (2024, "", "A Traveler's Needs", "洪常秀", "Hong Sangsoo", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    (2024, "", "The Empire", "布鲁诺·杜蒙", "Bruno Dumont", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    (2024, "", "Pepe", "", "Nelson Carlos De Los Santos Arias", "最佳导演银熊奖", "Silver Bear for Best Director"),
    (2024, "", "A Different Man", "", "Aaron Schimberg", "最佳主角银熊奖（Sebastian Stan）", "Silver Bear for Best Leading Performance"),
    (2024, "", "Small Things Like These", "", "Tim Mielants", "最佳配角银熊奖（Emily Watson）", "Silver Bear for Best Supporting Performance"),
    (2024, "", "Dying", "", "Matthias Glasner", "最佳编剧银熊奖（Matthias Glasner）", "Silver Bear for Best Screenplay"),
    (2024, "", "The Devil's Bath", "", "Veronika Franz & Severin Fiala", "杰出艺术贡献银熊奖（摄影：Martin Gschlacht）", "Silver Bear for Outstanding Artistic Contribution"),
    (2023, "烈火青春", "Afire", "克里斯蒂安·佩措尔德", "Christian Petzold", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    (2023, "", "Bad Living", "", "João Canijo", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    (2023, "", "The Plough", "菲利普·加瑞尔", "Philippe Garrel", "最佳导演银熊奖", "Silver Bear for Best Director"),
    (2023, "两万种蜜蜂", "20,000 Species of Bees", "", "Estibaliz Urresola Solaguren", "最佳主角银熊奖（Sofía Otero）", "Silver Bear for Best Leading Performance"),
    (2023, "", "Till the End of the Night", "", "Christoph Hochhäusler", "最佳配角银熊奖（Thea Ehre）", "Silver Bear for Best Supporting Performance"),
    (2023, "音乐", "Music", "安格拉·夏娜莱克", "Angela Schanelec", "最佳编剧银熊奖（Angela Schanelec）", "Silver Bear for Best Screenplay"),
    (2023, "迪斯科男孩", "Disco Boy", "", "Giacomo Abbruzzese", "杰出艺术贡献银熊奖（摄影：Hélène Louvart）", "Silver Bear for Outstanding Artistic Contribution"),
    (2022, "小说家的电影", "So-seol-ga-ui yeong-hwa", "洪常秀", "Hong Sangsoo", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    (2022, "宝石长袍", "Robe of Gems", "娜塔莉亚·洛佩兹·加拉多", "Natalia López Gallardo", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    (2022, "双刃剑", "Avec amour et acharnement", "克莱尔·德尼", "Claire Denis", "最佳导演银熊奖", "Silver Bear for Best Director"),
    (2022, "库尔纳兹诉小布什", "Rabiye Kurnaz gegen George W. Bush", "安德里亚斯·德里森", "Andreas Dresen", "最佳主角银熊奖（Meltem Kaptan）", "Silver Bear for Best Leading Performance"),
    (2022, "娜娜", "Nana", "卡米拉·安迪妮", "Kamila Andini", "最佳配角银熊奖（Laura Basuki）", "Silver Bear for Best Supporting Performance"),
    (2022, "库尔纳兹诉小布什", "Rabiye Kurnaz gegen George W. Bush", "安德里亚斯·德里森", "Andreas Dresen", "最佳编剧银熊奖（Laila Stieler）", "Silver Bear for Best Screenplay"),
    (2022, "一切都会好起来", "Everything Will Be Ok", "潘礼德", "Rithy Panh", "杰出艺术贡献银熊奖（Rithy Panh、Sarit Mang）", "Silver Bear for Outstanding Artistic Contribution"),
    (2021, "倒霉性爱，发狂黄片", "Bad Luck Banging or Loony Porn", "拉杜·裘德", "Radu Jude", "金熊奖", "Golden Bear for Best Film"),
    (2021, "偶然与想象", "Wheel of Fortune and Fantasy", "滨口龙介", "Ryusuke Hamaguchi", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
    (2021, "巴赫曼先生和他的学生", "Mr Bachmann and His Class", "玛利亚·施佩特", "Maria Speth", "评审团奖银熊奖", "Silver Bear Jury Prize"),
    (2021, "自然光线", "Natural Light", "德内斯·纳吉", "Dénes Nagy", "最佳导演银熊奖", "Silver Bear for Best Director"),
    (2021, "我是你的人", "I'm Your Man", "玛丽亚·施拉德", "Maria Schrader", "最佳主角银熊奖（Maren Eggert）", "Silver Bear for Best Leading Performance"),
    (2021, "森林随处可见", "Forest - I See You Everywhere", "本斯·弗利高夫", "Bence Fliegauf", "最佳配角银熊奖（Lilla Kizlinger）", "Silver Bear for Best Supporting Performance"),
    (2021, "引见", "Introduction", "洪常秀", "Hong Sangsoo", "最佳编剧银熊奖（Hong Sangsoo）", "Silver Bear for Best Screenplay"),
    (2021, "一部警察电影", "A Cop Movie", "阿隆索·帕拉西奥斯", "Alonso Ruizpalacios", "杰出艺术贡献银熊奖（剪辑：Yibrán Asuad）", "Silver Bear for Outstanding Artistic Contribution"),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for year, film_zh, film_en, director_zh, director_en, award_zh, award_en in ADDITIONS:
        key = ("Berlin", year, film_en, award_en)
        if key in existing:
            continue
        rows.append({"festival":"Berlin","festivalZh":"柏林","year":year,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":SOURCES[year],"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
        existing.add(key); added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified award rows")
