import fs from 'node:fs';

const source = 'https://www.berlinale.de/media/download/preise-jurys/60_ifb_preise.pdf';
const checkedAt = '2026-09-24';
const base = { festival:'Berlin', festivalZh:'柏林', year:2010, section:'Competition', status:'winner', official:source, imdbId:'', doubanUrl:'', trailerUrl:'', technical:{}, checkedAt };
const rows = [
  ['蜂蜜','Honey','塞米赫·卡普兰奥卢','Semih Kaplanoglu','金熊奖','Golden Bear'],
  ['如果我想吹口哨，我就吹','If I Want To Whistle, I Whistle','弗洛林·谢尔班','Florin Serban','评审团大奖银熊奖','Jury Grand Prix - Silver Bear'],
  ['影子写手','The Ghost Writer','罗曼·波兰斯基','Roman Polanski','最佳导演银熊奖','Silver Bear for Best Director'],
  ['芋虫','Caterpillar','若松孝二','Koji Wakamatsu','最佳女演员银熊奖（寺岛忍）','Silver Bear for Best Actress'],
  ['我是怎样度过这个夏天','How I Ended This Summer','阿列克谢·波波格列布斯基','Alexei Popogrebsky','最佳男演员银熊奖（Grigori Dobrygin / Sergei Puskepalis）','Silver Bear for Best Actor'],
  ['我是怎样度过这个夏天','How I Ended This Summer','阿列克谢·波波格列布斯基','Alexei Popogrebsky','杰出艺术贡献银熊奖（摄影：Pavel Kostomarov）','Silver Bear for Outstanding Artistic Contribution'],
  ['团圆','Apart Together','王全安','Wang Quan’an','最佳编剧银熊奖（王全安 / Na Jin）','Silver Bear for Best Script'],
  ['如果我想吹口哨，我就吹','If I Want To Whistle, I Whistle','弗洛林·谢尔班','Florin Serban','阿尔弗雷德·鲍尔奖','Alfred Bauer Prize']
].map(([filmZh,filmEn,directorZh,directorEn,awardZh,awardEn])=>({...base,filmZh,filmEn,directorZh,directorEn,awardZh,awardEn}));

for (const path of ['data/records.json','public/data/records.json']) {
  const data = JSON.parse(fs.readFileSync(path,'utf8'));
  const key = r => [r.festival,r.year,r.filmEn,r.awardEn].join('|').toLowerCase();
  const seen = new Set(data.map(key));
  for (const row of rows) if (!seen.has(key(row))) { data.push(row); seen.add(key(row)); }
  data.sort((a,b)=>(b.year-a.year)||String(a.festival).localeCompare(String(b.festival))||String(a.filmEn).localeCompare(String(b.filmEn))||String(a.awardEn).localeCompare(String(b.awardEn)));
  fs.writeFileSync(path, JSON.stringify(data,null,2)+'\n');
}
