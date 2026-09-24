import fs from 'node:fs';

const source = 'https://www.berlinale.de/en/archive/awards-juries/awards.html/y=2007/o=desc/p=1/rp=40';
const checkedAt = '2026-09-24';
const base = { festival:'Berlin', festivalZh:'柏林', year:2007, section:'Competition', status:'winner', official:source, imdbId:'', doubanUrl:'', trailerUrl:'', technical:{}, checkedAt };
const rows = [
  ['图雅的婚事','Tuya de hunshi','王全安','Wang Quan’an','金熊奖','Golden Bear'],
  ['另一个','El otro','阿里尔·罗特','Ariel Rotter','评审团大奖银熊奖','Jury Grand Prix - Silver Bear'],
  ['波弗特','Beaufort','约瑟夫·斯达','Joseph Cedar','最佳导演银熊奖','Silver Bear for Best Director'],
  ['耶拉','Yella','克里斯蒂安·佩措尔德','Christian Petzold','最佳女演员银熊奖（Nina Hoss）','Silver Bear for Best Actress'],
  ['另一个','El otro','阿里尔·罗特','Ariel Rotter','最佳男演员银熊奖（Julio Chávez）','Silver Bear for Best Actor'],
  ['牧羊人','The Good Shepherd','罗伯特·德尼罗','Robert De Niro','杰出艺术贡献银熊奖（演员群体）','Silver Bear for an Outstanding Artistic Contribution'],
  ['迷幻公园','Hallam Foe','大卫·马肯兹','David Mackenzie','最佳电影音乐银熊奖','Silver Bear for Best Film Music'],
  ['机器人之恋','Saibogujiman kwenchana','朴赞郁','Park Chan-wook','阿尔弗雷德·鲍尔奖','Alfred Bauer Prize']
].map(([filmZh,filmEn,directorZh,directorEn,awardZh,awardEn])=>({...base,filmZh,filmEn,directorZh,directorEn,awardZh,awardEn}));

for (const path of ['data/records.json','public/data/records.json']) {
  const data = JSON.parse(fs.readFileSync(path,'utf8'));
  const key = r => [r.festival,r.year,r.filmEn,r.awardEn].join('|').toLowerCase();
  const seen = new Set(data.map(key));
  for (const row of rows) if (!seen.has(key(row))) { data.push(row); seen.add(key(row)); }
  data.sort((a,b)=>(b.year-a.year)||String(a.festival).localeCompare(String(b.festival))||String(a.filmEn).localeCompare(String(b.filmEn))||String(a.awardEn).localeCompare(String(b.awardEn)));
  fs.writeFileSync(path, JSON.stringify(data,null,2)+'\n');
}
