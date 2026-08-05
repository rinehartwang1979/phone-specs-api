# 部署指南 — 电子产品规格 API 数据服务

## 方式1：Railway 部署（推荐，免费层够用）

### 本地已就绪
- ✅ API 代码: `api/main.py`
- ✅ 数据文件: `data/phones.json` (10条种子数据)
- ✅ 依赖: FastAPI + Uvicorn + Pydantic

### 部署步骤（需你手动操作 5 分钟）

1. 访问 https://railway.app → 用 GitHub 登录
2. New Project → Deploy from GitHub repo
3. Railway 自动检测 Python + requirements.txt，部署
4. 在 Settings → Domains 获取你的 URL（如 `xxx.up.railway.app`）

### RapidAPI 上架步骤

1. 注册 https://rapidapi.com/provider
2. Add API → 填入 railway URL
3. 粘贴 `deploy/rapidapi-listing.json` 中的端点描述
4. 设置定价计划（免费层 1000次/月作为种子流量）

---

## 方式2：Vercel Serverless（备选）

```json
// vercel.json
{
  "builds": [{"src": "api/main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/api/(.*)", "dest": "api/main.py"}]
}
```

限制：冷启动延迟 1-2 秒，不适合高频调用。

---

## 流量获取

| 渠道 | 方式 | 预估 |
|------|------|------|
| RapidAPI 市场 | 自然搜索流量 | 50-200次/月（免费层） |
| Reddit/HN | 发帖分享 "I built a free phone specs API" | 一次性 500-2000次 |
| GitHub | 开源 API 客户端库 | 持续引流 |
| API 聚合站 | 提交到 Public APIs 列表 | 稳定长尾流量 |

---

## 规模化路线图

| 阶段 | 内容 | 时间 |
|------|------|------|
| MVP | 10款手机 + 5个端点 | ✅ 已完成 |
| 扩数据 | 爬取京东前 100 热门手机 | Week 2 |
| 加品类 | 笔记本 + 平板 | Week 3-4 |
| 加端点 | /compare /autocomplete /price-history | Week 5-6 |
| 独立站 | 自有域名 + Stripe/Paddle 直收 | Month 3 |
