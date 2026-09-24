#!/usr/bin/env python3
"""Append Berlinale Competition awards verified against official Berlinale award PDFs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED_AT = "2026-09-24"

BATCHES = [
    (2016, "https://www.berlinale.de/media/download/preise-jurys/66_berlinale_awards.pdf", [
        ("海上火焰", "Fire at Sea", "吉安弗兰科·罗西", "Gianfranco Rosi", "金熊奖", "Golden Bear"),
        ("萨拉热窝之死", "Death in Sarajevo", "丹尼斯·塔诺维奇", "Danis Tanović", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
        ("悲伤秘密的摇篮曲", "A Lullaby to the Sorrowful Mystery", "拉夫·迪亚兹", "Lav Diaz", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
        ("将来的事", "Things to Come", "米娅·汉森-洛夫", "Mia Hansen-Løve", "最佳导演银熊奖", "Silver Bear for Best Director"),
        ("公社", "The Commune", "托马斯·温特伯格", "Thomas Vinterberg", "最佳女演员银熊奖（Trine Dyrholm）", "Silver Bear for Best Actress"),
        ("赫迪", "Hedi", "穆罕默德·本·阿提亚", "Mohamed Ben Attia", "最佳男演员银熊奖（Majd Mastoura）", "Silver Bear for Best Actor"),
        ("爱情合众国", "United States of Love", "托马斯·瓦希勒夫斯基", "Tomasz Wasilewski", "最佳编剧银熊奖（Tomasz Wasilewski）", "Silver Bear for Best Script"),
        ("长江图", "Crosscurrent", "杨超", "Yang Chao", "杰出艺术贡献银熊奖（摄影：李屏宾）", "Silver Bear for Outstanding Artistic Contribution"),
    ]),
    (2015, "https://www.berlinale.de/media/download/preise-jurys/65_berlinale_awards.pdf", [
        ("出租车", "Taxi", "贾法·帕纳西", "Jafar Panahi", "金熊奖", "Golden Bear"),
        ("神父俱乐部", "The Club", "帕布罗·拉雷恩", "Pablo Larraín", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
        ("火山下的人生", "Ixcanul Volcano", "杰罗·布斯塔曼特", "Jayro Bustamante", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
        ("喝彩！", "Aferim!", "拉杜·裘德", "Radu Jude", "最佳导演银熊奖（并列）", "Silver Bear for Best Director"),
        ("身体", "Body", "玛高扎塔·施莫夫兹卡", "Małgorzata Szumowska", "最佳导演银熊奖（并列）", "Silver Bear for Best Director"),
        ("四十五周年", "45 Years", "安德鲁·海格", "Andrew Haigh", "最佳女演员银熊奖（Charlotte Rampling）", "Silver Bear for Best Actress"),
        ("四十五周年", "45 Years", "安德鲁·海格", "Andrew Haigh", "最佳男演员银熊奖（Tom Courtenay）", "Silver Bear for Best Actor"),
        ("珍珠纽扣", "The Pearl Button", "帕特里西奥·古斯曼", "Patricio Guzmán", "最佳编剧银熊奖（Patricio Guzmán）", "Silver Bear for Best Script"),
        ("维多利亚", "Victoria", "塞巴斯蒂安·施普尔", "Sebastian Schipper", "杰出艺术贡献银熊奖（摄影：Sturla Brandth Grøvlen）", "Silver Bear for Outstanding Artistic Contribution"),
    ]),
    (2014, "https://www.berlinale.de/media/download/preise-jurys/64_berlinale_awards.pdf", [
        ("白日焰火", "Black Coal, Thin Ice", "刁亦男", "Diao Yinan", "金熊奖", "Golden Bear"),
        ("布达佩斯大饭店", "The Grand Budapest Hotel", "韦斯·安德森", "Wes Anderson", "评审团大奖银熊奖", "Silver Bear Grand Jury Prize"),
        ("纵情一曲", "Life of Riley", "阿伦·雷乃", "Alain Resnais", "阿尔弗雷德·鲍尔银熊奖", "Silver Bear Alfred Bauer Prize"),
        ("少年时代", "Boyhood", "理查德·林克莱特", "Richard Linklater", "最佳导演银熊奖", "Silver Bear for Best Director"),
        ("小小的家", "The Little House", "山田洋次", "Yoji Yamada", "最佳女演员银熊奖（黑木华）", "Silver Bear for Best Actress"),
        ("白日焰火", "Black Coal, Thin Ice", "刁亦男", "Diao Yinan", "最佳男演员银熊奖（廖凡）", "Silver Bear for Best Actor"),
        ("苦路十四站", "Stations of the Cross", "迪特里希·布鲁格曼", "Dietrich Brüggemann", "最佳编剧银熊奖（Dietrich Brüggemann、Anna Brüggemann）", "Silver Bear for Best Script"),
        ("推拿", "Blind Massage", "娄烨", "Lou Ye", "杰出艺术贡献银熊奖（摄影：曾剑）", "Silver Bear for Outstanding Artistic Contribution"),
    ]),
    (2013, "https://www.berlinale.de/media/download/preise-jurys/63_berlinale_awards.pdf", [
        ("孩童姿势", "Child's Pose", "卡林·皮特·内策尔", "Călin Peter Netzer", "金熊奖", "Golden Bear"),
        ("渺生一页", "An Episode in the Life of an Iron Picker", "丹尼斯·塔诺维奇", "Danis Tanović", "评审团大奖银熊奖", "Jury Grand Prix (Silver Bear)"),
        ("维克多和弗洛伦斯看见一只熊", "Vic+Flo Saw a Bear", "丹尼斯·科泰", "Denis Côté", "阿尔弗雷德·鲍尔银熊奖", "Alfred Bauer Prize (Silver Bear)"),
        ("雪崩王子", "Prince Avalanche", "大卫·戈登·格林", "David Gordon Green", "最佳导演银熊奖", "Silver Bear for Best Director"),
        ("葛洛莉亚", "Gloria", "塞巴斯蒂安·莱里奥", "Sebastián Lelio", "最佳女演员银熊奖（Paulina García）", "Silver Bear for Best Actress"),
        ("渺生一页", "An Episode in the Life of an Iron Picker", "丹尼斯·塔诺维奇", "Danis Tanović", "最佳男演员银熊奖（Nazif Mujić）", "Silver Bear for Best Actor"),
        ("闭幕", "Closed Curtain", "贾法·帕纳西 / 坎布兹亚·帕托维", "Jafar Panahi / Kamboziya Partovi", "最佳编剧银熊奖（Jafar Panahi）", "Silver Bear for Best Script"),
        ("和谐课程", "Harmony Lessons", "埃米尔·拜加津", "Emir Baigazin", "杰出艺术贡献银熊奖（摄影：Aziz Zhambakiyev）", "Silver Bear for Outstanding Artistic Contribution"),
    ]),
    (2011, "https://www.berlinale.de/media/download/preise-jurys/61_ifb_awards_2011.pdf", [
        ("一次别离", "A Separation", "阿斯哈·法哈蒂", "Asghar Farhadi", "最佳女演员银熊奖（女演员群像）", "Silver Bear for Best Actress"),
        ("一次别离", "A Separation", "阿斯哈·法哈蒂", "Asghar Farhadi", "最佳男演员银熊奖（男演员群像）", "Silver Bear for Best Actor"),
        ("如果我们生活在一起", "If Not Us, Who", "安德烈斯·凡伊尔", "Andres Veiel", "阿尔弗雷德·鲍尔奖", "Alfred Bauer Prize"),
    ]),
]

def apply(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    existing = {(r.get("festival"), r.get("year"), r.get("filmEn"), r.get("awardEn")) for r in rows}
    added = 0
    for year, source, additions in BATCHES:
        for film_zh, film_en, director_zh, director_en, award_zh, award_en in additions:
            key = ("Berlin", year, film_en, award_en)
            if key in existing:
                continue
            rows.append({"festival":"Berlin","festivalZh":"柏林","year":year,"section":"Competition","status":"winner","filmZh":film_zh,"filmEn":film_en,"directorZh":director_zh,"directorEn":director_en,"awardZh":award_zh,"awardEn":award_en,"official":source,"imdbId":"","doubanUrl":"","trailerUrl":"","technical":{},"checkedAt":CHECKED_AT})
            existing.add(key)
            added += 1
    rows.sort(key=lambda r: (-int(r.get("year", 0)), r.get("festival", ""), r.get("filmEn", ""), r.get("awardEn", "")))
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added

if __name__ == "__main__":
    a = apply(ROOT / "data/records.json")
    b = apply(ROOT / "public/data/records.json")
    print(f"added {a} + {b} verified Berlinale award rows")
