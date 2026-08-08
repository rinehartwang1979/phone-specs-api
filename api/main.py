"""
电子产品规格 API 服务

端点:
    GET  /api/v1/search?q=关键词        搜索手机
    GET  /api/v1/specs/{id}             查询详细规格
    GET  /api/v1/brands                 品牌列表
    GET  /api/v1/stats                  数据统计
    GET  /api/v1/health                 健康检查

部署: Railway (免费层) / 或 Vercel Serverless
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# -------- 配置 --------
DATA_FILE = Path(__file__).parent.parent / "data" / "phones.json"
APP_VERSION = "1.0.0"

# -------- 应用初始化 --------
app = FastAPI(
    title="Phone Specs API",
    description="电子产品规格查询 API — 手机品类",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Static files (demo landing page)
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# -------- 数据加载（内存缓存） --------
_cache: dict = {"data": None, "loaded_at": None}


def load_data() -> list:
    """加载手机数据（带缓存）"""
    now = datetime.now(timezone.utc)
    if _cache["data"] is not None and _cache["loaded_at"] is not None:
        age = (now - _cache["loaded_at"]).total_seconds()
        if age < 300:  # 5 分钟缓存
            return _cache["data"]
    
    if DATA_FILE.exists():
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        _cache["data"] = data
        _cache["loaded_at"] = now
        return data
    return []


def force_reload():
    """强制重新加载数据"""
    _cache["data"] = None
    _cache["loaded_at"] = None


# -------- 工具函数 --------
def search_phones(query: str, limit: int = 20) -> list:
    """全文搜索手机"""
    phones = load_data()
    q = query.lower().strip()
    if not q:
        return phones[:limit]
    
    results = []
    for p in phones:
        score = 0
        searchable = f"{p.get('brand','')} {p.get('model','')} {p.get('model_name','')} {p.get('chipset','')} {p.get('os','')}"
        searchable = searchable.lower()
        
        # 精确匹配加分
        if q in searchable:
            score += 10
        # 单词匹配
        for word in q.split():
            if word in searchable:
                score += 3
        if score > 0:
            results.append((score, p))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:limit]]


# -------- 端点 --------
@app.get("/")
async def root():
    """演示首页"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Phone Specs API — see /docs for API documentation"}

@app.get("/api/v1/health")
async def health():
    """健康检查"""
    phones = load_data()
    return {
        "status": "ok",
        "version": APP_VERSION,
        "record_count": len(phones),
        "updated_at": _cache["loaded_at"].isoformat() if _cache["loaded_at"] else None,
    }


@app.get("/api/v1/stats")
async def stats():
    """数据统计"""
    phones = load_data()
    brands = {}
    for p in phones:
        b = p.get("brand", "Unknown")
        brands[b] = brands.get(b, 0) + 1
    
    chipsets = {}
    for p in phones:
        c = p.get("chipset", "")
        if c:
            chipsets[c] = chipsets.get(c, 0) + 1
    
    return {
        "total": len(phones),
        "brands": brands,
        "top_chipsets": dict(sorted(chipsets.items(), key=lambda x: x[1], reverse=True)[:10]),
        "data_source": "jd.com",
    }


@app.get("/api/v1/brands")
async def brands():
    """品牌列表"""
    phones = load_data()
    brand_set = {}
    for p in phones:
        b = p.get("brand", "Unknown")
        if b not in brand_set:
            brand_set[b] = 0
        brand_set[b] += 1
    return {
        "brands": [
            {"name": k, "count": v}
            for k, v in sorted(brand_set.items(), key=lambda x: x[1], reverse=True)
        ]
    }


@app.get("/api/v1/search")
async def search(
    q: str = Query(..., description="搜索关键词（品牌/型号/芯片/系统）"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    fields: Optional[str] = Query(None, description="返回字段（逗号分隔），默认全部"),
):
    """
    搜索手机 — 支持品牌、型号、芯片、系统等关键词
    
    示例:
        /api/v1/search?q=iPhone
        /api/v1/search?q=Snapdragon
        /api/v1/search?q=华为&fields=id,brand,model,chipset,price_range
    """
    results = search_phones(q, limit)
    
    # 字段筛选
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        results = [
            {k: v for k, v in r.items() if k in field_list or k == "id"}
            for r in results
        ]
    
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.get("/api/v1/specs/{phone_id}")
async def specs(phone_id: str):
    """
    查询手机完整规格
    
    示例:
        /api/v1/specs/apple_iphone16promax
    """
    phones = load_data()
    for p in phones:
        if p.get("id") == phone_id:
            return {"found": True, "data": p}
    
    # 尝试模糊匹配
    phone_id_lower = phone_id.lower()
    for p in phones:
        if phone_id_lower in p.get("id", "").lower():
            return {"found": True, "matched_by": "fuzzy", "data": p}
    
    raise HTTPException(status_code=404, detail=f"Phone not found: {phone_id}")


@app.get("/api/v1/releases")
async def releases(
    year: Optional[int] = Query(None, description="按年份筛选（如 2024）"),
    month: Optional[int] = Query(None, ge=1, le=12, description="按月份筛选（1-12）"),
    brand: Optional[str] = Query(None, description="按品牌筛选"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    fields: Optional[str] = Query(None, description="返回字段（逗号分隔），默认全部"),
):
    """
    发布日历 — 按发布时间查询手机
    
    示例:
        /api/v1/releases?year=2024
        /api/v1/releases?year=2024&month=9
        /api/v1/releases?brand=Apple
        /api/v1/releases?year=2025&fields=id,brand,model,launch_date
    """
    phones = load_data()
    results = []
    for p in phones:
        ld = p.get("launch_date", "")
        if not ld:
            continue
        if year is not None and ld[:4] != str(year):
            continue
        if month is not None and ld[5:7] != f"{month:02d}":
            continue
        if brand and brand.lower() not in p.get("brand", "").lower():
            continue
        results.append(p)
    
    # 按发布日期倒序
    results.sort(key=lambda x: x.get("launch_date", ""), reverse=True)
    results = results[:limit]
    
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        results = [
            {k: v for k, v in r.items() if k in field_list or k == "id"}
            for r in results
        ]
    
    return {
        "year": year,
        "month": month,
        "brand": brand,
        "count": len(results),
        "results": results,
    }


@app.get("/api/v1/image/{phone_id}")
async def image(phone_id: str):
    """
    查询手机图片 URL
    
    示例:
        /api/v1/image/apple_iphone16promax
    """
    phones = load_data()
    for p in phones:
        if p.get("id") == phone_id:
            img = p.get("image_url", "")
            if img:
                return {"found": True, "id": phone_id, "image_url": img}
            return {"found": True, "id": phone_id, "image_url": None, "note": "No image available"}
    
    raise HTTPException(status_code=404, detail=f"Phone not found: {phone_id}")


@app.get("/api/v1/price/{phone_id}")
async def price(phone_id: str):
    """
    查询手机价格区间（USD）
    
    示例:
        /api/v1/price/apple_iphone16promax
    """
    phones = load_data()
    for p in phones:
        if p.get("id") == phone_id:
            price_data = {
                "found": True,
                "id": phone_id,
                "model_name": p.get("model_name", ""),
                "price_usd": p.get("price_usd"),
                "price_range_usd": p.get("price_range_usd"),
                "currency": "USD",
                "note": "Approximate retail price range from GSMArena" if p.get("price_range_usd") else "No price data available",
            }
            return price_data
    
    raise HTTPException(status_code=404, detail=f"Phone not found: {phone_id}")


@app.get("/api/v1/compare")
async def compare(
    id1: str = Query(..., description="第一款手机 ID"),
    id2: str = Query(..., description="第二款手机 ID"),
):
    """
    对比两款手机规格
    
    示例:
        /api/v1/compare?id1=apple_iphone16promax&id2=samsung_galaxys24ultra
    """
    phones = load_data()
    phone1 = phone2 = None
    
    for p in phones:
        if p.get("id") == id1:
            phone1 = p
        if p.get("id") == id2:
            phone2 = p
    
    if not phone1:
        raise HTTPException(status_code=404, detail=f"Phone not found: {id1}")
    if not phone2:
        raise HTTPException(status_code=404, detail=f"Phone not found: {id2}")
    
    # 共同字段对比
    compare_fields = [
        "brand", "screen_size", "screen_type", "resolution", "refresh_rate",
        "chipset", "ram", "storage", "rear_camera_main", "front_camera",
        "battery_capacity", "charging_wired", "os", "weight", "water_resistance",
    ]
    
    comparison = {}
    for field in compare_fields:
        comparison[field] = {
            "phone1": phone1.get(field, ""),
            "phone2": phone2.get(field, ""),
        }
    
    return {
        "phone1": {"id": phone1["id"], "model_name": phone1["model_name"]},
        "phone2": {"id": phone2["id"], "model_name": phone2["model_name"]},
        "comparison": comparison,
    }


# -------- RapidAPI 兼容头处理 --------
@app.middleware("http")
async def rapidapi_rate_limit_header(request, call_next):
    """为 RapidAPI 添加流量统计头"""
    response = await call_next(request)
    response.headers["X-API-Version"] = APP_VERSION
    response.headers["X-RateLimit-Remaining"] = "1000"
    return response


# -------- 直接运行 --------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
