import fs from 'node:fs';

const source = 'https://www.berlinale.de/en/archive/awards-juries/awards.html/y=2008/o=desc/p=1/rp=40';
const checkedAt = '2026-09-24';
const base = { festival:'Berlin', festivalZh:'柏林', year:2008, section:'Competition', status:'winner', official:source, imdbId:'', doubanUrl:'', trailerUrl:'', technical:{}, checkedAt };
const rows = [
  ['精英部队','Tropa de elite','若泽·帕迪里亚','José Padilha','金熊奖','Golden Bear for Best Film'],
  ['标准操作程序','Standard Operating Procedure','埃罗尔·莫里斯','Errol Morris','评审团大奖银熊奖','Jury Grand Prix (Silver Bear)'],
  ['血色将至','There Will Be Blood','保罗·托马斯·安德森','Paul Thomas Anderson','最佳导演银熊奖','Silver Bear for Best Director'],
  ['无忧无虑','Happy-Go-Lucky','迈克·李','Mike Leigh','最佳女演员银熊奖（Sally Hawkins）','Silver Bear for Best Actress'],
  ['麻雀之歌','Avaze Gonjeshk-ha','马基德·马基迪','Majid Majidi','最佳男演员银熊奖（Reza Najie）','Silver Bear for Best Actor'],
  ['左右','Zou You','王小帅','Wang Xiaoshuai','最佳编剧银熊奖（Wang Xiaoshuai）','Silver Bear for Best Script'],
  ['血色将至','There Will Be Blood','保罗·托马斯·安德森','Paul Thomas Anderson','杰出艺术贡献银熊奖（音乐：Jonny Greenwood）','Silver Bear for an Outstanding Artistic Contribution (Music)'],
  ['太浩湖','Lake Tahoe','费尔南多·埃姆克','Fernando Eimbcke','阿尔弗雷德·鲍尔奖','Alfred Bauer Prize']
].map(([filmZh,filmEn,directorZh,directorEn,awardZh,awardEn])=>({...base,filmZh,filmEn,directorZh,directorEn,awardZh,awardEn}));

for (const path of ['data/records.json','public/data/records.json']) {
  const data = JSON.parse(fs.readFileSync(path,'utf8'));
  const key = r => [r.festival,r.year,r.filmEn,r.awardEn].join('|').toLowerCase();
  const seen = new Set(data.map(key));
  for (const row of rows) if (!seen.has(key(row))) { data.push(row); seen.add(key(row)); }
  data.sort((a,b)=>(b.year-a.year)||String(a.festival).localeCompare(String(b.festival))||String(a.filmEn).localeCompare(String(b.filmEn))||String(a.awardEn).localeCompare(String(b.awardEn)));
  fs.writeFileSync(path, JSON.stringify(data,null,2)+'\n');
}
