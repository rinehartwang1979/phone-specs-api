"""
GSMArena 批量补数据脚本 — 第二阶段：匹配 catalog → 补 image_url → 抓价格页

用法: python3 scraper/gsm_enrich.py enrich
"""
import json, os, re, sys, time, urllib.request

BASE = "https://www.gsmarena.com"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CATALOG = os.path.join(DATA_DIR, "gsm_catalog.json")
PHONES = "/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service/data/phones.json"

def fetch(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            if i == retries - 1:
                print(f"  FAIL {url}: {e}")
                return ""
            time.sleep(2)

def norm(s):
    """规范化名称用于匹配"""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def nospace(s):
    return s.replace(" ", "")

# catalog 端后缀词（注意大小写不敏感）
CAT_SUFFIX_RE = re.compile(
    r"\b(android smartphone|android|smartphone|phone|tablet|smart watch|watch|specifications|5g|4g|3g|lte)\b",
    re.IGNORECASE,
)

# model 端后缀词（比 catalog 多 cellular，另处理括号）
MODEL_SUFFIX_RE = re.compile(
    r"\b(android smartphone|android|smartphone|phone|tablet|smart watch|watch|specifications|5g|4g|3g|lte|cellular)\b",
    re.IGNORECASE,
)

def cat_key(title):
    """catalog title → 规范化 key（去掉描述后缀词）"""
    t = title.split(".")[0]
    t = CAT_SUFFIX_RE.sub(" ", t)
    return norm(t)

def model_key(s):
    """model_name → 规范化 key（去括号 + 剥后缀词）"""
    s = re.sub(r"\([^)]*\)", " ", s)
    s = MODEL_SUFFIX_RE.sub(" ", s)
    return norm(s)

def build_index(catalog):
    """构建双索引（带空格 + 无空格）"""
    cat_by_norm = {}
    cat_by_ns = {}
    for it in catalog:
        if not it.get("title"):
            continue
        k = cat_key(it["title"])
        if k and k not in cat_by_norm:
            cat_by_norm[k] = it
        ns = nospace(k)
        if ns and ns not in cat_by_ns:
            cat_by_ns[ns] = it
    return cat_by_norm, cat_by_ns

def match_phone(p, cat_by_norm, cat_by_ns):
    """多级匹配：精确 → 无空格 → 双向子串"""
    br = norm(p.get("brand", ""))
    mn = norm(p.get("model_name", ""))
    md = norm(p.get("model", ""))
    candidates = []
    for s in [mn, md]:
        if not s:
            continue
        # 去重品牌前缀: "asus asus rog phone 9" -> "asus rog phone 9"
        if br and s.startswith(br + " ") and s.count(br) >= 2:
            s = s.replace(br + " ", "", 1)
        candidates.append(s)
        candidates.append(model_key(s))
    for s in [mn, md]:
        if s and br and not s.startswith(br):
            candidates.append(norm(f"{br} {s}"))
            candidates.append(model_key(f"{br} {s}"))
    # Motorola 特例: 试 "moto X" 形式
    if br == "motorola":
        for s in [mn, md]:
            if s and not s.startswith("moto"):
                candidates.append(norm(f"moto {s}"))
                candidates.append(model_key(f"moto {s}"))
    seen = set()
    for key in candidates:
        if not key or key in seen:
            continue
        seen.add(key)
        if key in cat_by_norm:
            return cat_by_norm[key]
    for key in seen:
        ns = nospace(key)
        if ns in cat_by_ns:
            return cat_by_ns[ns]
    for key in sorted(seen, key=len, reverse=True):
        if len(key) > 4:
            for ck, cit in cat_by_norm.items():
                if key in ck or (len(ck) > 4 and ck in key):
                    return cit
    for key in sorted(seen, key=len, reverse=True):
        ns = nospace(key)
        if len(ns) > 4:
            for ck, cit in cat_by_ns.items():
                if ns in ck or (len(ck) > 4 and ck in ns):
                    return cit
    return None

def parse_price(html):
    """从价格页提取价格点列表"""
    # 格式: &#36;&thinsp;1,157 或 $1,157 或 &euro;...
    prices = re.findall(r"&#36;&thinsp;([\d,]+)|&euro;&thinsp;([\d,]+)|\$([\d,]+)", html)
    usd = []
    for m in prices:
        val = (m[0] or m[2] or "").replace(",", "")
        if val:
            usd.append(int(val))
    if not usd:
        usd = [int(v.replace(",", "")) for v in re.findall(r"USD\s*([\d,]+)", html)]
    return sorted(set(usd))

def main():
    images_only = "--images-only" in sys.argv
    with open(CATALOG) as f:
        catalog = json.load(f)
    with open(PHONES) as f:
        phones = json.load(f)

    print(f"Catalog: {len(catalog)} | Phones: {len(phones)}")

    cat_by_norm, cat_by_ns = build_index(catalog)

    matched = 0
    price_fetched = 0
    for p in phones:
        it = match_phone(p, cat_by_norm, cat_by_ns)
        if it:
            matched += 1
            p["image_url"] = it.get("img", "")
            p["gsmarena_url"] = f"{BASE}/{it['slug']}-{it['id']}.php"
            p["gsmarena_slug"] = it["slug"]
            p["gsmarena_id"] = it["id"]
        else:
            p["image_url"] = ""
            p["gsmarena_url"] = ""
            p.pop("gsmarena_slug", None)
            p.pop("gsmarena_id", None)

    print(f"\nMatched images: {matched}/{len(phones)}")

    # 抓价格页（限速 1 req/s）
    for i, p in enumerate(phones):
        if images_only:
            break
        slug = p.get("gsmarena_slug", "")
        if not slug or p.get("price_range_usd"):
            continue
        # 价格页 URL: {slug}-price-{id}.php — 需要 id
        m = re.search(r"-(\d+)\.php$", p.get("gsmarena_url", ""))
        if not m:
            continue
        price_url = f"{BASE}/{slug}-price-{m.group(1)}.php"
        html = fetch(price_url)
        if html:
            prices = parse_price(html)
            if prices:
                p["price_range_usd"] = {"min": prices[0], "max": prices[-1], "points": prices}
                p["price_usd"] = prices[0]
                price_fetched += 1
                print(f"  [{i}] {p['model_name']}: ${prices[0]}-${prices[-1]}")
        time.sleep(0.6)

    print(f"\nPrice fetched: {price_fetched}/{len(phones)}")

    # 写回
    with open(PHONES, "w") as f:
        json.dump(phones, f, ensure_ascii=False, indent=1)
    print(f"Saved → {PHONES}")

if __name__ == "__main__":
    main()
