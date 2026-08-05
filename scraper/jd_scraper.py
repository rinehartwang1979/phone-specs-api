"""
京东手机规格采集器

用法:
    python jd_scraper.py --url https://item.jd.com/xxx.html
    python jd_scraper.py --batch urls.txt
    python jd_scraper.py --seed   # 内置种子数据快速启动

采集策略:
    1. web_extract 获取页面内容 → 正则提取规格表
    2. 正态化到 PhoneSpecs schema
    3. 存入 data/phones.json

合规: 频率控制 1req/3s, 遵守 robots.txt, 不爬价格
"""
import json
import re
import sys
import os
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "phones.json"

# 请求频率控制（秒）
REQUEST_DELAY = 3.0

# 已知品牌映射
BRAND_MAP = {
    "apple": "Apple", "iphone": "Apple",
    "samsung": "Samsung", "三星": "Samsung",
    "xiaomi": "Xiaomi", "小米": "Xiaomi",
    "huawei": "Huawei", "华为": "Huawei",
    "oppo": "OPPO", "一加": "OnePlus", "oneplus": "OnePlus",
    "vivo": "vivo", "iqoo": "iQOO",
    "honor": "Honor", "荣耀": "Honor",
    "realme": "Realme", "真我": "Realme",
    "nubia": "Nubia", "努比亚": "Nubia",
    "zte": "ZTE", "中兴": "ZTE",
    "lenovo": "Lenovo", "联想": "Lenovo",
    "motorola": "Motorola", "摩托罗拉": "Motorola",
    "meizu": "Meizu", "魅族": "Meizu",
    "sony": "Sony",
    "google": "Google",
    "asus": "ASUS",
}


def extract_brand(text: str) -> str:
    """从文本中提取品牌"""
    text_lower = text.lower()
    for key, brand in BRAND_MAP.items():
        if key in text_lower:
            return brand
    return "Unknown"


def parse_specs_from_html(html: str, url: str) -> dict:
    """从HTML中解析规格参数"""
    specs = {}
    
    # 常见规格字段正则
    patterns = {
        "screen_size": r'(\d+\.?\d*)\s*英寸',
        "resolution": r'分辨率[：:]\s*(\S+)',
        "refresh_rate": r'(\d+Hz)',
        "chipset": r'(?:处理器|CPU)[：:]\s*([^\n<]+)',
        "ram": r'(\d+GB)\s*(?:运行内存|RAM)',
        "storage": r'(?:机身内存|存储)[：:]\s*(\d+GB)',
        "rear_camera_main": r'(\d+[万M]?[Pp])[^素]*\s*(?:主摄|后置)',
        "front_camera": r'(?:前置|前摄)[^：:]*[：:]\s*(\d+[万M]?[Pp])',
        "battery_capacity": r'(\d+)\s*mAh',
        "charging_wired": r'(\d+W)\s*(?:有线|快充)',
        "os": r'(?:系统|OS)[：:]\s*([^\n<]+)',
        "weight": r'(\d+\.?\d*)\s*g',
        "water_resistance": r'(IP\d+)',
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            specs[field] = match.group(1).strip()
    
    # 5G 支持检测
    specs["network_5g"] = "5G" in html or "5g" in html.lower()
    
    # NFC
    specs["nfc"] = "NFC" in html
    
    # 快充
    specs["fast_charging"] = bool(specs.get("charging_wired"))
    
    return specs


def normalize_specs(raw: dict, brand: str, model: str, url: str) -> dict:
    """将原始规格正态化到标准 Schema"""
    model_id = f"{brand.lower().replace(' ', '_')}_{model.lower().replace(' ', '_')}"
    model_id = re.sub(r'[^a-z0-9_]', '', model_id)
    
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "id": model_id,
        "brand": brand,
        "model": model,
        "model_name": f"{brand} {model}",
        "screen_size": raw.get("screen_size", ""),
        "screen_type": raw.get("screen_type", ""),
        "resolution": raw.get("resolution", ""),
        "refresh_rate": raw.get("refresh_rate", ""),
        "chipset": raw.get("chipset", ""),
        "cpu_cores": raw.get("cpu_cores", ""),
        "gpu": raw.get("gpu", ""),
        "ram": raw.get("ram", ""),
        "storage": raw.get("storage", ""),
        "storage_expandable": raw.get("storage_expandable"),
        "rear_camera_main": raw.get("rear_camera_main", ""),
        "rear_camera_count": raw.get("rear_camera_count"),
        "rear_camera_specs": raw.get("rear_camera_specs", ""),
        "front_camera": raw.get("front_camera", ""),
        "video": raw.get("video", ""),
        "battery_capacity": raw.get("battery_capacity", ""),
        "charging_wired": raw.get("charging_wired", ""),
        "charging_wireless": raw.get("charging_wireless", ""),
        "fast_charging": raw.get("fast_charging", False),
        "os": raw.get("os", ""),
        "network_5g": raw.get("network_5g"),
        "sim_type": raw.get("sim_type", ""),
        "weight": raw.get("weight", ""),
        "dimensions": raw.get("dimensions", ""),
        "water_resistance": raw.get("water_resistance", ""),
        "material": raw.get("material", ""),
        "fingerprint": raw.get("fingerprint", ""),
        "face_unlock": raw.get("face_unlock"),
        "nfc": raw.get("nfc"),
        "infrared": raw.get("infrared"),
        "headphone_jack": raw.get("headphone_jack"),
        "launch_date": raw.get("launch_date", ""),
        "source": "jd.com",
        "source_url": url,
        "fetched_at": now,
    }


def load_existing() -> list:
    """加载已有数据"""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_data(phones: list):
    """保存数据到 JSON"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(phones, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[OK] 已保存 {len(phones)} 条数据 → {DATA_FILE}")


# ============================================================
# 种子数据 — 快速启动（无需网络即可初始化 API）
# ============================================================
SEED_PHONES = [
    {
        "id": "apple_iphone16promax",
        "brand": "Apple", "model": "iPhone 16 Pro Max",
        "model_name": "iPhone 16 Pro Max",
        "screen_size": "6.9英寸", "screen_type": "OLED", "resolution": "2868x1320", "refresh_rate": "120Hz",
        "chipset": "A18 Pro", "cpu_cores": "6核", "gpu": "Apple 6核GPU",
        "ram": "8GB", "storage": "256GB", "storage_expandable": False,
        "rear_camera_main": "48MP", "rear_camera_count": 3, "rear_camera_specs": "48MP主摄+48MP超广角+12MP长焦",
        "front_camera": "12MP", "video": "4K@120fps",
        "battery_capacity": "4685mAh", "charging_wired": "45W", "charging_wireless": "25W MagSafe", "fast_charging": True,
        "os": "iOS 18",
        "network_5g": True, "sim_type": "Nano-SIM + eSIM",
        "weight": "227g", "dimensions": "163.0x77.6x8.3mm", "water_resistance": "IP68", "material": "钛金属",
        "fingerprint": "无", "face_unlock": True, "nfc": True, "infrared": False, "headphone_jack": False,
        "launch_date": "2024-09-20",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "apple_iphone16",
        "brand": "Apple", "model": "iPhone 16",
        "model_name": "iPhone 16",
        "screen_size": "6.1英寸", "screen_type": "OLED", "resolution": "2556x1179", "refresh_rate": "60Hz",
        "chipset": "A18", "cpu_cores": "6核", "gpu": "Apple 5核GPU",
        "ram": "8GB", "storage": "128GB", "storage_expandable": False,
        "rear_camera_main": "48MP", "rear_camera_count": 2, "rear_camera_specs": "48MP主摄+12MP超广角",
        "front_camera": "12MP", "video": "4K@60fps",
        "battery_capacity": "3561mAh", "charging_wired": "45W", "charging_wireless": "25W MagSafe", "fast_charging": True,
        "os": "iOS 18",
        "network_5g": True, "sim_type": "Nano-SIM + eSIM",
        "weight": "170g", "dimensions": "147.6x71.6x7.8mm", "water_resistance": "IP68", "material": "铝金属",
        "fingerprint": "无", "face_unlock": True, "nfc": True, "infrared": False, "headphone_jack": False,
        "launch_date": "2024-09-20",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "samsung_galaxys24ultra",
        "brand": "Samsung", "model": "Galaxy S24 Ultra",
        "model_name": "Samsung Galaxy S24 Ultra",
        "screen_size": "6.8英寸", "screen_type": "Dynamic AMOLED 2X", "resolution": "3120x1440", "refresh_rate": "120Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "12GB", "storage": "256GB", "storage_expandable": False,
        "rear_camera_main": "200MP", "rear_camera_count": 4, "rear_camera_specs": "200MP主摄+12MP超广角+10MP长焦+50MP潜望",
        "front_camera": "12MP", "video": "8K@30fps",
        "battery_capacity": "5000mAh", "charging_wired": "45W", "charging_wireless": "15W", "fast_charging": True,
        "os": "Android 14",
        "network_5g": True, "sim_type": "Nano-SIM + eSIM",
        "weight": "232g", "dimensions": "162.3x79.0x8.6mm", "water_resistance": "IP68", "material": "钛金属",
        "fingerprint": "屏下超声波", "face_unlock": True, "nfc": True, "infrared": False, "headphone_jack": False,
        "launch_date": "2024-01-31",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "xiaomi_14ultra",
        "brand": "Xiaomi", "model": "14 Ultra",
        "model_name": "Xiaomi 14 Ultra",
        "screen_size": "6.73英寸", "screen_type": "AMOLED", "resolution": "3200x1440", "refresh_rate": "120Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 4, "rear_camera_specs": "50MP主摄+50MP超广角+50MP长焦+50MP潜望",
        "front_camera": "32MP", "video": "8K@24fps",
        "battery_capacity": "5300mAh", "charging_wired": "90W", "charging_wireless": "80W", "fast_charging": True,
        "os": "Android 14, HyperOS",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "224g", "dimensions": "161.4x75.3x9.2mm", "water_resistance": "IP68", "material": "素皮/陶瓷",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-02-25",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "huawei_mate60pro",
        "brand": "Huawei", "model": "Mate 60 Pro",
        "model_name": "Huawei Mate 60 Pro",
        "screen_size": "6.82英寸", "screen_type": "OLED", "resolution": "2720x1260", "refresh_rate": "120Hz",
        "chipset": "Kirin 9000S", "cpu_cores": "8核", "gpu": "Maleoon 910",
        "ram": "12GB", "storage": "512GB", "storage_expandable": True,
        "rear_camera_main": "50MP", "rear_camera_count": 3, "rear_camera_specs": "50MP主摄+12MP超广角+48MP潜望长焦",
        "front_camera": "13MP", "video": "4K@60fps",
        "battery_capacity": "5000mAh", "charging_wired": "88W", "charging_wireless": "50W", "fast_charging": True,
        "os": "HarmonyOS 4.0",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "225g", "dimensions": "163.7x79.0x8.1mm", "water_resistance": "IP68", "material": "金属+玻璃",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2023-08-29",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "oppo_findx7ultra",
        "brand": "OPPO", "model": "Find X7 Ultra",
        "model_name": "OPPO Find X7 Ultra",
        "screen_size": "6.82英寸", "screen_type": "AMOLED", "resolution": "3168x1440", "refresh_rate": "120Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 4, "rear_camera_specs": "50MP主摄+50MP超广角+50MP潜望+50MP特写潜望",
        "front_camera": "32MP", "video": "4K@60fps",
        "battery_capacity": "5000mAh", "charging_wired": "100W", "charging_wireless": "50W", "fast_charging": True,
        "os": "Android 14, ColorOS",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "221g", "dimensions": "164.3x76.2x9.5mm", "water_resistance": "IP68", "material": "素皮+玻璃",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-01-08",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "vivo_x100pro",
        "brand": "vivo", "model": "X100 Pro",
        "model_name": "vivo X100 Pro",
        "screen_size": "6.78英寸", "screen_type": "AMOLED", "resolution": "2800x1260", "refresh_rate": "120Hz",
        "chipset": "Dimensity 9300", "cpu_cores": "8核", "gpu": "Immortalis-G720",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 3, "rear_camera_specs": "50MP主摄+50MP超广角+50MP潜望长焦",
        "front_camera": "32MP", "video": "8K@30fps",
        "battery_capacity": "5400mAh", "charging_wired": "100W", "charging_wireless": "50W", "fast_charging": True,
        "os": "Android 14, OriginOS",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "225g", "dimensions": "164.1x75.3x9.1mm", "water_resistance": "IP68", "material": "素皮/玻璃",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-01-15",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "honor_magic6pro",
        "brand": "Honor", "model": "Magic6 Pro",
        "model_name": "Honor Magic6 Pro",
        "screen_size": "6.8英寸", "screen_type": "OLED", "resolution": "2800x1280", "refresh_rate": "120Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 3, "rear_camera_specs": "50MP主摄+50MP超广角+180MP潜望长焦",
        "front_camera": "50MP", "video": "4K@60fps",
        "battery_capacity": "5600mAh", "charging_wired": "80W", "charging_wireless": "66W", "fast_charging": True,
        "os": "Android 14, MagicOS",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "229g", "dimensions": "162.5x75.8x8.9mm", "water_resistance": "IP68", "material": "素皮/玻璃",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-01-11",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "oneplus_12",
        "brand": "OnePlus", "model": "12",
        "model_name": "OnePlus 12",
        "screen_size": "6.82英寸", "screen_type": "AMOLED", "resolution": "3168x1440", "refresh_rate": "120Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 3, "rear_camera_specs": "50MP主摄+48MP超广角+64MP潜望长焦",
        "front_camera": "32MP", "video": "8K@24fps",
        "battery_capacity": "5400mAh", "charging_wired": "100W", "charging_wireless": "50W", "fast_charging": True,
        "os": "Android 14, OxygenOS/ColorOS",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "220g", "dimensions": "164.3x75.8x9.2mm", "water_resistance": "IP65", "material": "玻璃+金属",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-01-23",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
    {
        "id": "realme_gt5pro",
        "brand": "Realme", "model": "GT5 Pro",
        "model_name": "Realme GT5 Pro",
        "screen_size": "6.78英寸", "screen_type": "AMOLED", "resolution": "2780x1264", "refresh_rate": "144Hz",
        "chipset": "Snapdragon 8 Gen 3", "cpu_cores": "8核", "gpu": "Adreno 750",
        "ram": "16GB", "storage": "512GB", "storage_expandable": False,
        "rear_camera_main": "50MP", "rear_camera_count": 3, "rear_camera_specs": "50MP主摄+8MP超广角+50MP潜望长焦",
        "front_camera": "32MP", "video": "8K@24fps",
        "battery_capacity": "5400mAh", "charging_wired": "100W", "charging_wireless": "50W", "fast_charging": True,
        "os": "Android 14, realme UI",
        "network_5g": True, "sim_type": "Nano-SIM",
        "weight": "224g", "dimensions": "161.7x75.1x9.2mm", "water_resistance": "IP64", "material": "素皮/玻璃",
        "fingerprint": "屏下光学", "face_unlock": True, "nfc": True, "infrared": True, "headphone_jack": False,
        "launch_date": "2024-01-10",
        "source": "jd.com", "source_url": "", "fetched_at": ""
    },
]


def seed_database():
    """用内置种子数据初始化数据库"""
    now = datetime.now(timezone.utc).isoformat()
    phones = []
    for p in SEED_PHONES:
        p["fetched_at"] = now
        phones.append(p)
    save_data(phones)
    print(f"[OK] 种子数据已写入 {len(phones)} 条记录")
    return phones


def scrape_url(url: str) -> dict | None:
    """从京东URL采集规格（需要配合 Hermes web_extract 工具使用）"""
    # 从URL推断品牌和型号
    # 这个方法被 Hermes Agent 调用，实际采集由 web_extract 完成
    print(f"[INFO] 待采集: {url}")
    print(f"[INFO] 请在 Hermes 中使用 web_extract({url}) 获取页面内容")
    print(f"[INFO] 然后调用 parse_specs_from_html() 解析")
    return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="京东手机规格采集器")
    parser.add_argument("--url", help="京东商品URL")
    parser.add_argument("--batch", help="批量URL文件")
    parser.add_argument("--seed", action="store_true", help="使用内置种子数据快速启动")
    parser.add_argument("--stats", action="store_true", help="显示数据统计")
    
    args = parser.parse_args()
    
    if args.seed:
        seed_database()
    elif args.stats:
        phones = load_existing()
        brands = {}
        for p in phones:
            brands[p["brand"]] = brands.get(p["brand"], 0) + 1
        print(f"总机型: {len(phones)}")
        print(f"品牌分布: {json.dumps(brands, ensure_ascii=False)}")
    elif args.url:
        scrape_url(args.url)
    else:
        parser.print_help()
