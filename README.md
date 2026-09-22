# 小花的大宇宙 🌌

四大电影节活跃档案：戛纳、威尼斯、柏林、洛迦诺。

当前已收录四大电影节完整最高奖历史（截至 2026 年，共 345 条获奖记录）。
运行时主数据文件为 `data/records.json`，Pages 镜像为
`public/data/records.json`；两份文件在提交前必须保持一致。

- 历届作品 / 入围 / 获奖查询
- 导演中英文名
- 导演获奖次数与最高奖次数
- IMDb Technical Specifications 字段
- 豆瓣中文译名映射字段
- YouTube 官方预告字段
- 官方来源与最后核对时间
- API: /api/records, /api/health

## 本地运行
npm install
npm start

## 部署
推送到 `main` 后由 `.github/workflows/pages.yml` 自动部署到 GitHub Pages。
