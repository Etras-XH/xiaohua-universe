import fs from 'node:fs';

const source = 'https://www.berlinale.de/en/archive/awards-juries/awards.html/y=2009/o=desc/p=1/rp=40';
const checkedAt = '2026-09-24';
const base = { festival:'Berlin', festivalZh:'柏林', year:2009, section:'Competition', status:'winner', official:source, imdbId:'', doubanUrl:'', trailerUrl:'', technical:{}, checkedAt };
const rows = [
  ['伤心的奶水','The Milk of Sorrow','克劳迪娅·略萨','Claudia Llosa','金熊奖','Golden Bear'],
  ['其他人','Everyone Else','玛伦·阿德','Maren Ade','评审团大奖银熊奖','Jury Grand Prix - Silver Bear'],
  ['关于伊丽','About Elly','阿斯哈·法哈蒂','Asghar Farhadi','最佳导演银熊奖','Silver Bear for Best Director'],
  ['其他人','Everyone Else','玛伦·阿德','Maren Ade','最佳女演员银熊奖（Birgit Minichmayr）','Silver Bear for Best Actress'],
  ['伦敦河','London River','拉契得·波查拉','Rachid Bouchareb','最佳男演员银熊奖（Sotigui Kouyaté）','Silver Bear for Best Actor'],
  ['信使','The Messenger','奥伦·穆弗曼','Oren Moverman','最佳编剧银熊奖（Oren Moverman / Alessandro Camon）','Silver Bear for Best Script'],
  ['卡塔林·瓦嘉','Katalin Varga','彼得·斯崔克兰德','Peter Strickland','杰出艺术贡献银熊奖（声音：Gábor Erdély / Tamás Székely）','Silver Bear for Outstanding Artistic Contribution'],
  ['巨人','Gigante','阿德里安·比涅斯','Adrián Biniez','阿尔弗雷德·鲍尔奖','Alfred Bauer Prize']
].map(([filmZh,filmEn,directorZh,directorEn,awardZh,awardEn])=>({...base,filmZh,filmEn,directorZh,directorEn,awardZh,awardEn}));

for (const path of ['data/records.json','public/data/records.json']) {
  const data = JSON.parse(fs.readFileSync(path,'utf8'));
  const key = r => [r.festival,r.year,r.filmEn,r.awardEn].join('|').toLowerCase();
  const seen = new Set(data.map(key));
  for (const row of rows) if (!seen.has(key(row))) { data.push(row); seen.add(key(row)); }
  data.sort((a,b)=>(b.year-a.year)||String(a.festival).localeCompare(String(b.festival))||String(a.filmEn).localeCompare(String(b.filmEn))||String(a.awardEn).localeCompare(String(b.awardEn)));
  fs.writeFileSync(path, JSON.stringify(data,null,2)+'\n');
}
