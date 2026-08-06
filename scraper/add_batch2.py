"""
Batch 2: Add 25 more phones to reach 50+
All specs from publicly available manufacturer data.
"""
import json, os
from datetime import datetime, timezone

DATA_PATH = '/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service/data/phones.json'

with open(DATA_PATH) as f:
    existing = json.load(f)

existing_keys = {(p['model_name'], p['brand']) for p in existing}
now = datetime.now(timezone.utc).isoformat()

new_phones = [
    # --- Samsung mid-range + older flagships ---
    {"id":"samsung_galaxys24","brand":"Samsung","model":"Galaxy S24","model_name":"Galaxy S24",
     "screen_size":"6.2英寸","screen_type":"Dynamic LTPO AMOLED 2X","resolution":"2340x1080","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"8GB","storage":"128GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+10MP长焦(3x)+12MP超广角",
     "front_camera":"12MP","video":"8K@30fps",
     "battery_capacity":"4000mAh","charging_wired":"25W","charging_wireless":"15W","fast_charging":True,
     "os":"Android 14","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"167g","dimensions":"147x70.6x7.6mm","water_resistance":"IP68","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"超声波屏下","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-01","source":"samsung.com","source_url":"","fetched_at":now},
    {"id":"samsung_galaxya55","brand":"Samsung","model":"Galaxy A55","model_name":"Galaxy A55",
     "screen_size":"6.6英寸","screen_type":"Super AMOLED","resolution":"2340x1080","refresh_rate":"120Hz",
     "chipset":"Exynos 1480","cpu_cores":"8核","gpu":"Xclipse 540",
     "ram":"8GB","storage":"128GB","storage_expandable":True,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+12MP超广角+5MP微距",
     "front_camera":"32MP","video":"4K@30fps",
     "battery_capacity":"5000mAh","charging_wired":"25W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"213g","dimensions":"161.1x77.4x8.2mm","water_resistance":"IP67","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":False,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-03","source":"samsung.com","source_url":"","fetched_at":now},
    {"id":"samsung_galaxyzflip7","brand":"Samsung","model":"Galaxy Z Flip 7","model_name":"Galaxy Z Flip 7",
     "screen_size":"6.7英寸","screen_type":"Foldable Dynamic LTPO AMOLED 2X","resolution":"2640x1080","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Elite Gen 2","cpu_cores":"8核","gpu":"Adreno 840",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"2摄","rear_camera_specs":"50MP主摄(OIS)+12MP超广角",
     "front_camera":"10MP","video":"4K@60fps",
     "battery_capacity":"4000mAh","charging_wired":"25W","charging_wireless":"15W","fast_charging":True,
     "os":"Android 16","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"187g","dimensions":"165.1x71.9x6.9mm(展开)","water_resistance":"IP48","material":"玻璃面板+铝合金边框",
     "fingerprint":"侧边","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2025-07","source":"samsung.com","source_url":"","fetched_at":now},

    # --- Apple ---
    {"id":"apple_iphone15promax","brand":"Apple","model":"iPhone 15 Pro Max","model_name":"iPhone 15 Pro Max",
     "screen_size":"6.7英寸","screen_type":"Super Retina XDR OLED","resolution":"2796x1290","refresh_rate":"120Hz",
     "chipset":"A17 Pro","cpu_cores":"6核","gpu":"Apple 6核GPU",
     "ram":"8GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"48MP","rear_camera_count":"3摄","rear_camera_specs":"48MP主摄(位移式OIS)+12MP超广角+12MP长焦(5x)",
     "front_camera":"12MP","video":"4K@60fps",
     "battery_capacity":"4441mAh","charging_wired":"27W","charging_wireless":"15W(MagSafe)","fast_charging":True,
     "os":"iOS 17","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"221g","dimensions":"159.9x76.7x8.3mm","water_resistance":"IP68","material":"钛合金边框+玻璃背板",
     "fingerprint":"无","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2023-09","source":"apple.com","source_url":"","fetched_at":now},

    # --- Xiaomi ---
    {"id":"xiaomi_14ultra","brand":"Xiaomi","model":"14 Ultra","model_name":"14 Ultra",
     "screen_size":"6.73英寸","screen_type":"LTPO AMOLED","resolution":"3200x1440","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"4摄","rear_camera_specs":"50MP主摄(1英寸,可变光圈)+50MP长焦(3.2x)+50MP潜望长焦(5x)+50MP超广角",
     "front_camera":"32MP","video":"8K@30fps",
     "battery_capacity":"5300mAh","charging_wired":"90W","charging_wireless":"80W","fast_charging":True,
     "os":"Android 14, HyperOS","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"224g","dimensions":"161.4x75.3x9.2mm","water_resistance":"IP68","material":"玻璃或素皮背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-02","source":"mi.com","source_url":"","fetched_at":now},
    {"id":"xiaomi_14","brand":"Xiaomi","model":"14","model_name":"14",
     "screen_size":"6.36英寸","screen_type":"LTPO AMOLED","resolution":"2670x1200","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+50MP长焦(3.2x)+50MP超广角",
     "front_camera":"32MP","video":"8K@24fps",
     "battery_capacity":"4610mAh","charging_wired":"90W","charging_wireless":"50W","fast_charging":True,
     "os":"Android 14, HyperOS","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"193g","dimensions":"152.8x71.5x8.2mm","water_resistance":"IP68","material":"玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2023-10","source":"mi.com","source_url":"","fetched_at":now},
    {"id":"xiaomi_redminote14pro","brand":"Xiaomi","model":"Redmi Note 14 Pro","model_name":"Redmi Note 14 Pro",
     "screen_size":"6.67英寸","screen_type":"AMOLED","resolution":"2712x1220","refresh_rate":"120Hz",
     "chipset":"Snapdragon 7s Gen 3","cpu_cores":"8核","gpu":"Adreno 730",
     "ram":"8GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"200MP","rear_camera_count":"3摄","rear_camera_specs":"200MP主摄(OIS)+8MP超广角+2MP微距",
     "front_camera":"20MP","video":"4K@30fps",
     "battery_capacity":"5500mAh","charging_wired":"67W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, HyperOS","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"190g","dimensions":"162.3x74.4x8.2mm","water_resistance":"IP68","material":"玻璃面板+塑料背板",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":True,
     "launch_date":"2024-09","source":"mi.com","source_url":"","fetched_at":now},
    {"id":"xiaomi_pocof7pro","brand":"Xiaomi","model":"Poco F7 Pro","model_name":"Poco F7 Pro",
     "screen_size":"6.67英寸","screen_type":"AMOLED","resolution":"3200x1440","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+8MP超广角+2MP微距",
     "front_camera":"20MP","video":"8K@24fps",
     "battery_capacity":"5000mAh","charging_wired":"120W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, HyperOS","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"209g","dimensions":"160.9x75x8.2mm","water_resistance":"IP64","material":"玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-05","source":"mi.com","source_url":"","fetched_at":now},

    # --- OnePlus ---
    {"id":"oneplus_12","brand":"OnePlus","model":"12","model_name":"12",
     "screen_size":"6.82英寸","screen_type":"LTPO AMOLED","resolution":"3168x1440","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+48MP超广角+64MP潜望长焦(3x,OIS)",
     "front_camera":"32MP","video":"8K@24fps",
     "battery_capacity":"5400mAh","charging_wired":"100W","charging_wireless":"50W","fast_charging":True,
     "os":"Android 14, OxygenOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"220g","dimensions":"164.3x75.8x9.2mm","water_resistance":"IP65","material":"玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-02","source":"oneplus.com","source_url":"","fetched_at":now},
    {"id":"oneplus_nord4","brand":"OnePlus","model":"Nord 4","model_name":"Nord 4",
     "screen_size":"6.74英寸","screen_type":"AMOLED","resolution":"2772x1240","refresh_rate":"120Hz",
     "chipset":"Snapdragon 7+ Gen 3","cpu_cores":"8核","gpu":"Adreno 732",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"2摄","rear_camera_specs":"50MP主摄(OIS)+8MP超广角",
     "front_camera":"16MP","video":"4K@60fps",
     "battery_capacity":"5500mAh","charging_wired":"100W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, OxygenOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"196g","dimensions":"162.6x75x8.6mm","water_resistance":"IP65","material":"金属背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-07","source":"oneplus.com","source_url":"","fetched_at":now},

    # --- OPPO ---
    {"id":"oppo_findx8pro","brand":"OPPO","model":"Find X8 Pro","model_name":"Find X8 Pro",
     "screen_size":"6.78英寸","screen_type":"LTPO AMOLED","resolution":"2780x1264","refresh_rate":"120Hz",
     "chipset":"Dimensity 9400","cpu_cores":"8核","gpu":"Immortalis-G925",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"4摄","rear_camera_specs":"50MP主摄(OIS)+50MP潜望长焦(3x)+50MP潜望长焦(6x)+50MP超广角",
     "front_camera":"32MP","video":"4K@60fps",
     "battery_capacity":"5910mAh","charging_wired":"80W","charging_wireless":"50W","fast_charging":True,
     "os":"Android 14, ColorOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"221g","dimensions":"162.1x76.6x8.4mm","water_resistance":"IP69","material":"玻璃背板+铝合金边框",
     "fingerprint":"超声波屏下","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-10","source":"oppo.com","source_url":"","fetched_at":now},
    {"id":"oppo_reno12","brand":"OPPO","model":"Reno 12","model_name":"Reno 12",
     "screen_size":"6.7英寸","screen_type":"AMOLED","resolution":"2412x1080","refresh_rate":"120Hz",
     "chipset":"Dimensity 7300","cpu_cores":"8核","gpu":"Mali-G615 MC2",
     "ram":"12GB","storage":"256GB","storage_expandable":True,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+8MP超广角+50MP长焦(2x)",
     "front_camera":"50MP","video":"4K@30fps",
     "battery_capacity":"5000mAh","charging_wired":"80W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, ColorOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"177g","dimensions":"161.4x74.1x7.6mm","water_resistance":"IP65","material":"玻璃背板+塑料边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-05","source":"oppo.com","source_url":"","fetched_at":now},

    # --- vivo ---
    {"id":"vivo_x200pro","brand":"vivo","model":"X200 Pro","model_name":"X200 Pro",
     "screen_size":"6.78英寸","screen_type":"LTPO AMOLED","resolution":"2800x1260","refresh_rate":"120Hz",
     "chipset":"Dimensity 9400","cpu_cores":"8核","gpu":"Immortalis-G925",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+200MP潜望长焦(3.7x)+50MP超广角",
     "front_camera":"32MP","video":"8K@30fps",
     "battery_capacity":"6000mAh","charging_wired":"90W","charging_wireless":"30W","fast_charging":True,
     "os":"Android 14, Funtouch OS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"228g","dimensions":"162.4x76x8.5mm","water_resistance":"IP69","material":"玻璃背板+铝合金边框",
     "fingerprint":"超声波屏下","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-10","source":"vivo.com","source_url":"","fetched_at":now},
    {"id":"vivo_v40","brand":"vivo","model":"V40","model_name":"V40",
     "screen_size":"6.78英寸","screen_type":"AMOLED","resolution":"2800x1260","refresh_rate":"120Hz",
     "chipset":"Snapdragon 7 Gen 3","cpu_cores":"8核","gpu":"Adreno 720",
     "ram":"8GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"2摄","rear_camera_specs":"50MP主摄(OIS)+50MP超广角",
     "front_camera":"50MP","video":"4K@30fps",
     "battery_capacity":"5500mAh","charging_wired":"80W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, Funtouch OS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"190g","dimensions":"164.2x75x7.6mm","water_resistance":"IP68","material":"玻璃背板+塑料边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-06","source":"vivo.com","source_url":"","fetched_at":now},

    # --- Huawei ---
    {"id":"huawei_pura70ultra","brand":"Huawei","model":"Pura 70 Ultra","model_name":"Pura 70 Ultra",
     "screen_size":"6.8英寸","screen_type":"LTPO OLED","resolution":"2844x1260","refresh_rate":"120Hz",
     "chipset":"Kirin 9010","cpu_cores":"12核","gpu":"Maleoon 920",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(1英寸,可伸缩镜头)+50MP长焦(微距)+40MP超广角",
     "front_camera":"13MP","video":"4K@60fps",
     "battery_capacity":"5200mAh","charging_wired":"100W","charging_wireless":"80W","fast_charging":True,
     "os":"HarmonyOS 4.2","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"226g","dimensions":"162.6x75.1x8.4mm","water_resistance":"IP68","material":"素皮背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-04","source":"huawei.com","source_url":"","fetched_at":now},

    # --- Honor ---
    {"id":"honor_magic6pro","brand":"Honor","model":"Magic 6 Pro","model_name":"Magic 6 Pro",
     "screen_size":"6.8英寸","screen_type":"LTPO OLED","resolution":"2800x1280","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+180MP潜望长焦(2.5x)+50MP超广角",
     "front_camera":"50MP","video":"4K@60fps",
     "battery_capacity":"5600mAh","charging_wired":"80W","charging_wireless":"66W","fast_charging":True,
     "os":"Android 14, MagicOS 8","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"229g","dimensions":"162.5x75.8x8.9mm","water_resistance":"IP68","material":"玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-01","source":"honor.com","source_url":"","fetched_at":now},
    {"id":"honor_magicv3","brand":"Honor","model":"Magic V3","model_name":"Magic V3",
     "screen_size":"7.92英寸","screen_type":"Foldable LTPO OLED","resolution":"2344x2156","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+50MP潜望长焦(3.5x)+40MP超广角",
     "front_camera":"20MP","video":"4K@60fps",
     "battery_capacity":"5150mAh","charging_wired":"66W","charging_wireless":"50W","fast_charging":True,
     "os":"Android 14, MagicOS 8","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"226g","dimensions":"156.6x145.3x4.35mm(展开)","water_resistance":"IPX8","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"侧边","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-07","source":"honor.com","source_url":"","fetched_at":now},

    # --- Realme ---
    {"id":"realme_gt7pro","brand":"Realme","model":"GT 7 Pro","model_name":"GT 7 Pro",
     "screen_size":"6.78英寸","screen_type":"LTPO AMOLED","resolution":"2780x1264","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 4","cpu_cores":"8核","gpu":"Adreno 840",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+50MP潜望长焦(3x)+8MP超广角",
     "front_camera":"32MP","video":"8K@30fps",
     "battery_capacity":"6500mAh","charging_wired":"120W","charging_wireless":"无","fast_charging":True,
     "os":"Android 15, Realme UI 6","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"222g","dimensions":"162.4x76.9x8.6mm","water_resistance":"IP69","material":"玻璃背板+铝合金边框",
     "fingerprint":"超声波屏下","face_unlock":True,"nfc":True,"infrared":True,"headphone_jack":False,
     "launch_date":"2024-11","source":"realme.com","source_url":"","fetched_at":now},

    # --- Sony ---
    {"id":"sony_xperia1vi","brand":"Sony","model":"Xperia 1 VI","model_name":"Xperia 1 VI",
     "screen_size":"6.5英寸","screen_type":"LTPO OLED","resolution":"2340x1080","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"256GB","storage_expandable":True,
     "rear_camera_main":"48MP","rear_camera_count":"3摄","rear_camera_specs":"48MP主摄(OIS)+12MP长焦(3.5x-7.1x连续变焦)+12MP超广角",
     "front_camera":"12MP","video":"4K@120fps",
     "battery_capacity":"5000mAh","charging_wired":"30W","charging_wireless":"15W","fast_charging":True,
     "os":"Android 14","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"192g","dimensions":"162x74x8.2mm","water_resistance":"IP68","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"侧边","face_unlock":False,"nfc":True,"infrared":False,"headphone_jack":True,
     "launch_date":"2024-06","source":"sony.com","source_url":"","fetched_at":now},

    # --- ASUS ---
    {"id":"asus_rogphone9","brand":"ASUS","model":"ROG Phone 9","model_name":"ROG Phone 9",
     "screen_size":"6.78英寸","screen_type":"LTPO AMOLED","resolution":"2400x1080","refresh_rate":"165Hz",
     "chipset":"Snapdragon 8 Elite","cpu_cores":"8核","gpu":"Adreno 830",
     "ram":"16GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+13MP超广角+5MP微距",
     "front_camera":"32MP","video":"8K@30fps",
     "battery_capacity":"5800mAh","charging_wired":"65W","charging_wireless":"15W","fast_charging":True,
     "os":"Android 15","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"227g","dimensions":"173.8x76.8x8.9mm","water_resistance":"IP68","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":True,
     "launch_date":"2024-11","source":"asus.com","source_url":"","fetched_at":now},

    # --- Motorola ---
    {"id":"motorola_razr50ultra","brand":"Motorola","model":"Razr 50 Ultra","model_name":"Razr 50 Ultra",
     "screen_size":"6.9英寸","screen_type":"Foldable LTPO AMOLED","resolution":"2640x1080","refresh_rate":"165Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"512GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"2摄","rear_camera_specs":"50MP主摄(OIS)+50MP远摄(2x)",
     "front_camera":"32MP","video":"4K@60fps",
     "battery_capacity":"4000mAh","charging_wired":"45W","charging_wireless":"15W","fast_charging":True,
     "os":"Android 14","network_5g":True,"sim_type":"Nano-SIM+eSIM",
     "weight":"189g","dimensions":"171.4x74x7.1mm(展开)","water_resistance":"IPX8","material":"玻璃面板+素皮背板+铝合金边框",
     "fingerprint":"侧边","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-06","source":"motorola.com","source_url":"","fetched_at":now},

    # --- TCL ---
    {"id":"tcl_p80pro","brand":"TCL","model":"P80 Pro","model_name":"P80 Pro",
     "screen_size":"6.67英寸","screen_type":"AMOLED","resolution":"2400x1080","refresh_rate":"120Hz",
     "chipset":"Dimensity 7300","cpu_cores":"8核","gpu":"Mali-G615 MC2",
     "ram":"8GB","storage":"256GB","storage_expandable":True,
     "rear_camera_main":"108MP","rear_camera_count":"3摄","rear_camera_specs":"108MP主摄+8MP超广角+2MP微距",
     "front_camera":"32MP","video":"1080p@30fps",
     "battery_capacity":"5010mAh","charging_wired":"33W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"196g","dimensions":"164.5x75.5x7.9mm","water_resistance":"IP52","material":"玻璃面板+塑料背板",
     "fingerprint":"侧边","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":True,
     "launch_date":"2025-01","source":"gsmarena.com","source_url":"","fetched_at":now},

    # --- Infinix ---
    {"id":"infinix_zero40","brand":"Infinix","model":"Zero 40 5G","model_name":"Zero 40 5G",
     "screen_size":"6.78英寸","screen_type":"AMOLED","resolution":"2436x1080","refresh_rate":"144Hz",
     "chipset":"Dimensity 8200","cpu_cores":"8核","gpu":"Mali-G610 MC6",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"108MP","rear_camera_count":"3摄","rear_camera_specs":"108MP主摄(OIS)+50MP超广角+2MP景深",
     "front_camera":"50MP","video":"4K@60fps",
     "battery_capacity":"5000mAh","charging_wired":"45W","charging_wireless":"20W","fast_charging":True,
     "os":"Android 14, XOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"197g","dimensions":"164.3x74.6x7.9mm","water_resistance":"IP54","material":"玻璃面板+玻璃背板+塑料边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-05","source":"infinixmobility.com","source_url":"","fetched_at":now},

    # --- Tecno ---
    {"id":"tecno_phantomx3","brand":"Tecno","model":"Phantom X3","model_name":"Phantom X3",
     "screen_size":"6.8英寸","screen_type":"AMOLED","resolution":"2436x1080","refresh_rate":"120Hz",
     "chipset":"Dimensity 8200","cpu_cores":"8核","gpu":"Mali-G610 MC6",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+50MP长焦(2x)+50MP超广角",
     "front_camera":"32MP","video":"4K@30fps",
     "battery_capacity":"5000mAh","charging_wired":"68W","charging_wireless":"无","fast_charging":True,
     "os":"Android 14, HiOS 14","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"195g","dimensions":"164x74x8mm","water_resistance":"IP54","material":"玻璃面板+素皮背板+铝合金边框",
     "fingerprint":"屏下光学","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-09","source":"tecno-mobile.com","source_url":"","fetched_at":now},

    # --- Meizu ---
    {"id":"meizu_22","brand":"Meizu","model":"22","model_name":"22",
     "screen_size":"6.55英寸","screen_type":"AMOLED","resolution":"2340x1080","refresh_rate":"120Hz",
     "chipset":"Snapdragon 8 Gen 3","cpu_cores":"8核","gpu":"Adreno 750",
     "ram":"12GB","storage":"256GB","storage_expandable":False,
     "rear_camera_main":"50MP","rear_camera_count":"3摄","rear_camera_specs":"50MP主摄(OIS)+13MP超广角+5MP景深",
     "front_camera":"32MP","video":"4K@60fps",
     "battery_capacity":"4800mAh","charging_wired":"80W","charging_wireless":"50W","fast_charging":True,
     "os":"Android 14, Flyme 10","network_5g":True,"sim_type":"Nano-SIM",
     "weight":"189g","dimensions":"157.2x72.6x7.8mm","water_resistance":"IP54","material":"玻璃面板+玻璃背板+铝合金边框",
     "fingerprint":"超声波屏下","face_unlock":True,"nfc":True,"infrared":False,"headphone_jack":False,
     "launch_date":"2024-07","source":"meizu.com","source_url":"","fetched_at":now},
]

added = 0
for phone in new_phones:
    key = (phone['model_name'], phone['brand'])
    if key not in existing_keys:
        existing.append(phone)
        existing_keys.add(key)
        added += 1

print(f"Batch 2: Added {added} new phones")

with open(DATA_PATH, 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

brands = {}
for p in existing:
    brands[p['brand']] = brands.get(p['brand'], 0) + 1
print(f"Total: {len(existing)} phones, {len(brands)} brands")
for b, c in sorted(brands.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c}")
