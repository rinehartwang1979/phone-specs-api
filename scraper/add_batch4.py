import json, os
from datetime import datetime, timezone

DATA_PATH = '/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service/data/phones.json'

with open(DATA_PATH) as f:
    existing = json.load(f)

existing_keys = {(p['model_name'], p['brand']) for p in existing}
now = datetime.now(timezone.utc).isoformat()

def ph(**kw):
    kw['fetched_at'] = now
    return kw

new = [
    ph(id="samsung_galaxyzflip6",brand="Samsung",model="Galaxy Z Flip 6",model_name="Galaxy Z Flip 6",
      screen_size="6.7英寸",screen_type="Foldable Dynamic LTPO AMOLED 2X",resolution="2640x1080",refresh_rate="120Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄(OIS)+12MP超广角",front_camera="10MP",video="4K@60fps",
      battery_capacity="4000mAh",charging_wired="25W",charging_wireless="15W",fast_charging=True,
      os="Android 14",network_5g=True,sim_type="Nano-SIM+eSIM",
      weight="187g",dimensions="165.1x71.9x6.9mm(展开)",water_resistance="IP48",material="玻璃面板+铝合金边框",
      fingerprint="侧边",face_unlock=True,nfc=True,infrared=False,headphone_jack=False,
      launch_date="2024-07",source="samsung.com",source_url=""),
    ph(id="samsung_galaxys24plus",brand="Samsung",model="Galaxy S24+",model_name="Galaxy S24+",
      screen_size="6.7英寸",screen_type="Dynamic LTPO AMOLED 2X",resolution="3088x1440",refresh_rate="120Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="3摄",rear_camera_specs="50MP主摄(OIS)+10MP长焦(3x)+12MP超广角",front_camera="12MP",video="8K@30fps",
      battery_capacity="4900mAh",charging_wired="45W",charging_wireless="15W",fast_charging=True,
      os="Android 14",network_5g=True,sim_type="Nano-SIM+eSIM",
      weight="196g",dimensions="158.5x75.9x7.7mm",water_resistance="IP68",material="玻璃面板+玻璃背板+铝合金边框",
      fingerprint="超声波屏下",face_unlock=True,nfc=True,infrared=False,headphone_jack=False,
      launch_date="2024-01",source="samsung.com",source_url=""),
    ph(id="apple_iphone15pro",brand="Apple",model="iPhone 15 Pro",model_name="iPhone 15 Pro",
      screen_size="6.1英寸",screen_type="Super Retina XDR OLED",resolution="2556x1179",refresh_rate="120Hz",
      chipset="A17 Pro",cpu_cores="6核",gpu="Apple 6核GPU",ram="8GB",storage="128GB",storage_expandable=False,
      rear_camera_main="48MP",rear_camera_count="3摄",rear_camera_specs="48MP主摄(位移式OIS)+12MP超广角+12MP长焦(3x)",front_camera="12MP",video="4K@60fps",
      battery_capacity="3274mAh",charging_wired="27W",charging_wireless="15W(MagSafe)",fast_charging=True,
      os="iOS 17",network_5g=True,sim_type="Nano-SIM+eSIM",
      weight="187g",dimensions="146.6x70.6x8.3mm",water_resistance="IP68",material="钛合金边框+玻璃背板",
      fingerprint="无",face_unlock=True,nfc=True,infrared=False,headphone_jack=False,
      launch_date="2023-09",source="apple.com",source_url=""),
    ph(id="google_pixel9profold",brand="Google",model="Pixel 9 Pro Fold",model_name="Pixel 9 Pro Fold",
      screen_size="8.0英寸",screen_type="Foldable LTPO OLED",resolution="2076x2152",refresh_rate="120Hz",
      chipset="Tensor G4",cpu_cores="8核",gpu="Mali-G715",ram="16GB",storage="256GB",storage_expandable=False,
      rear_camera_main="48MP",rear_camera_count="3摄",rear_camera_specs="48MP主摄(OIS)+10.5MP长焦(5x)+12MP超广角",front_camera="10MP",video="4K@60fps",
      battery_capacity="4650mAh",charging_wired="21W",charging_wireless="7.5W",fast_charging=True,
      os="Android 14",network_5g=True,sim_type="Nano-SIM+eSIM",
      weight="257g",dimensions="155.2x150.2x5.1mm(展开)",water_resistance="IPX8",material="玻璃面板+玻璃背板+铝合金边框",
      fingerprint="侧边",face_unlock=True,nfc=True,infrared=False,headphone_jack=False,
      launch_date="2024-08",source="store.google.com",source_url=""),
    ph(id="xiaomi_14pro",brand="Xiaomi",model="14 Pro",model_name="14 Pro",
      screen_size="6.73英寸",screen_type="LTPO AMOLED",resolution="3200x1440",refresh_rate="120Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="3摄",rear_camera_specs="50MP主摄(可变光圈,OIS)+50MP长焦(3.2x)+50MP超广角",front_camera="32MP",video="8K@24fps",
      battery_capacity="4880mAh",charging_wired="120W",charging_wireless="50W",fast_charging=True,
      os="Android 14, HyperOS",network_5g=True,sim_type="Nano-SIM",
      weight="223g",dimensions="161.4x75.3x8.5mm",water_resistance="IP68",material="玻璃背板+铝合金边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2023-10",source="mi.com",source_url=""),
    ph(id="vivo_iqoo12",brand="vivo",model="iQOO 12",model_name="iQOO 12",
      screen_size="6.78英寸",screen_type="LTPO AMOLED",resolution="2800x1260",refresh_rate="144Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="3摄",rear_camera_specs="50MP主摄(OIS)+50MP超广角+64MP潜望长焦(3x)",front_camera="16MP",video="8K@30fps",
      battery_capacity="5000mAh",charging_wired="120W",charging_wireless="无",fast_charging=True,
      os="Android 14, OriginOS 4",network_5g=True,sim_type="Nano-SIM",
      weight="203g",dimensions="163.2x75.9x8.1mm",water_resistance="IP64",material="玻璃或素皮背板+铝合金边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2023-11",source="vivo.com",source_url=""),
    ph(id="vivo_iqooneo10",brand="vivo",model="iQOO Neo 10",model_name="iQOO Neo 10",
      screen_size="6.78英寸",screen_type="LTPO AMOLED",resolution="2800x1260",refresh_rate="144Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄(OIS)+8MP超广角",front_camera="16MP",video="4K@60fps",
      battery_capacity="6100mAh",charging_wired="120W",charging_wireless="无",fast_charging=True,
      os="Android 14, OriginOS 4",network_5g=True,sim_type="Nano-SIM",
      weight="204g",dimensions="162.9x75.4x8.1mm",water_resistance="IP64",material="玻璃背板+塑料边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2024-10",source="vivo.com",source_url=""),
    ph(id="oppo_reno13",brand="OPPO",model="Reno 13",model_name="Reno 13",
      screen_size="6.67英寸",screen_type="AMOLED",resolution="2712x1220",refresh_rate="120Hz",
      chipset="Dimensity 8300",cpu_cores="8核",gpu="Mali-G615 MC6",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄(OIS)+8MP超广角",front_camera="50MP",video="4K@30fps",
      battery_capacity="5600mAh",charging_wired="80W",charging_wireless="无",fast_charging=True,
      os="Android 14, ColorOS 14",network_5g=True,sim_type="Nano-SIM",
      weight="184g",dimensions="161.5x74.8x7.6mm",water_resistance="IP65",material="玻璃背板+塑料边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2024-11",source="oppo.com",source_url=""),
    ph(id="huawei_p60pro",brand="Huawei",model="P60 Pro",model_name="P60 Pro",
      screen_size="6.67英寸",screen_type="LTPO OLED",resolution="2700x1220",refresh_rate="120Hz",
      chipset="Snapdragon 8+ Gen 1",cpu_cores="8核",gpu="Adreno 730",ram="8GB",storage="256GB",storage_expandable=True,
      rear_camera_main="48MP",rear_camera_count="3摄",rear_camera_specs="48MP主摄(OIS)+48MP长焦(3.5x,微距)+13MP超广角",front_camera="13MP",video="4K@60fps",
      battery_capacity="4815mAh",charging_wired="88W",charging_wireless="50W",fast_charging=True,
      os="HarmonyOS 3.1",network_5g=False,sim_type="Nano-SIM",
      weight="200g",dimensions="161x74.5x8.3mm",water_resistance="IP68",material="玻璃背板+铝合金边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2023-03",source="huawei.com",source_url=""),
    ph(id="oneplus_12r",brand="OnePlus",model="12R",model_name="12R",
      screen_size="6.78英寸",screen_type="LTPO4 AMOLED",resolution="2780x1264",refresh_rate="120Hz",
      chipset="Snapdragon 8 Gen 2",cpu_cores="8核",gpu="Adreno 740",ram="8GB",storage="128GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="3摄",rear_camera_specs="50MP主摄(OIS)+8MP超广角+2MP微距",front_camera="16MP",video="4K@60fps",
      battery_capacity="5500mAh",charging_wired="100W",charging_wireless="无",fast_charging=True,
      os="Android 14, OxygenOS 14",network_5g=True,sim_type="Nano-SIM",
      weight="207g",dimensions="163.3x75.3x8.8mm",water_resistance="IP65",material="玻璃背板+铝合金边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=False,
      launch_date="2024-02",source="oneplus.com",source_url=""),
    ph(id="motorola_g85",brand="Motorola",model="G85 5G",model_name="G85 5G",
      screen_size="6.67英寸",screen_type="P-OLED",resolution="2400x1080",refresh_rate="120Hz",
      chipset="Snapdragon 6s Gen 3",cpu_cores="8核",gpu="Adreno 619",ram="12GB",storage="256GB",storage_expandable=True,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄(OIS)+8MP超广角(微距)",front_camera="32MP",video="1080p@30fps",
      battery_capacity="5000mAh",charging_wired="30W",charging_wireless="无",fast_charging=True,
      os="Android 14",network_5g=True,sim_type="Nano-SIM+eSIM",
      weight="173g",dimensions="161.9x73.1x7.6mm",water_resistance="IP54",material="素皮或塑料背板",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=False,headphone_jack=True,
      launch_date="2024-07",source="motorola.com",source_url=""),
    ph(id="realme_c75",brand="Realme",model="C75",model_name="C75",
      screen_size="6.67英寸",screen_type="IPS LCD",resolution="1604x720",refresh_rate="90Hz",
      chipset="Helio G85",cpu_cores="8核",gpu="Mali-G52 MC2",ram="6GB",storage="128GB",storage_expandable=True,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄+2MP景深",front_camera="8MP",video="1080p@30fps",
      battery_capacity="6000mAh",charging_wired="15W",charging_wireless="无",fast_charging=False,
      os="Android 14, Realme UI 5",network_5g=False,sim_type="Nano-SIM",
      weight="189g",dimensions="165.6x76.1x8.1mm",water_resistance="IP54",material="塑料背板",
      fingerprint="侧边",face_unlock=True,nfc=False,infrared=False,headphone_jack=True,
      launch_date="2024-08",source="realme.com",source_url=""),
    ph(id="nothing_phone2",brand="Nothing",model="Phone (2)",model_name="Phone (2)",
      screen_size="6.7英寸",screen_type="LTPO OLED",resolution="2412x1080",refresh_rate="120Hz",
      chipset="Snapdragon 8+ Gen 1",cpu_cores="8核",gpu="Adreno 730",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="2摄",rear_camera_specs="50MP主摄(OIS)+50MP超广角",front_camera="32MP",video="4K@60fps",
      battery_capacity="4700mAh",charging_wired="45W",charging_wireless="15W",fast_charging=True,
      os="Android 13, Nothing OS 2.5",network_5g=True,sim_type="Nano-SIM",
      weight="201g",dimensions="162.1x76.4x8.6mm",water_resistance="IP54",material="玻璃背板+铝合金边框+Glyph灯带",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=False,headphone_jack=False,
      launch_date="2023-07",source="nothing.tech",source_url=""),
    ph(id="asus_zenfone11ultra",brand="ASUS",model="Zenfone 11 Ultra",model_name="Zenfone 11 Ultra",
      screen_size="6.78英寸",screen_type="LTPO AMOLED",resolution="2400x1080",refresh_rate="144Hz",
      chipset="Snapdragon 8 Gen 3",cpu_cores="8核",gpu="Adreno 750",ram="12GB",storage="256GB",storage_expandable=False,
      rear_camera_main="50MP",rear_camera_count="3摄",rear_camera_specs="50MP主摄(云台OIS)+32MP长焦(3x)+13MP超广角",front_camera="32MP",video="8K@24fps",
      battery_capacity="5500mAh",charging_wired="65W",charging_wireless="15W",fast_charging=True,
      os="Android 14",network_5g=True,sim_type="Nano-SIM",
      weight="224g",dimensions="163.8x76.8x8.9mm",water_resistance="IP68",material="玻璃背板+铝合金边框",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=False,headphone_jack=True,
      launch_date="2024-03",source="asus.com",source_url=""),
    ph(id="xiaomi_redminote13",brand="Xiaomi",model="Redmi Note 13",model_name="Redmi Note 13",
      screen_size="6.67英寸",screen_type="AMOLED",resolution="2400x1080",refresh_rate="120Hz",
      chipset="Dimensity 6080",cpu_cores="8核",gpu="Mali-G57 MC2",ram="6GB",storage="128GB",storage_expandable=True,
      rear_camera_main="108MP",rear_camera_count="3摄",rear_camera_specs="108MP主摄+8MP超广角+2MP微距",front_camera="16MP",video="1080p@30fps",
      battery_capacity="5000mAh",charging_wired="33W",charging_wireless="无",fast_charging=True,
      os="Android 13, MIUI 14",network_5g=True,sim_type="Nano-SIM",
      weight="174g",dimensions="161.1x75x7.6mm",water_resistance="IP54",material="塑料背板",
      fingerprint="屏下光学",face_unlock=True,nfc=True,infrared=True,headphone_jack=True,
      launch_date="2023-09",source="mi.com",source_url=""),
]

added = 0
for phone in new:
    key = (phone['model_name'], phone['brand'])
    if key not in existing_keys:
        existing.append(phone)
        existing_keys.add(key)
        added += 1

print(f"Final batch: Added {added}")

with open(DATA_PATH, 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

brands = {}
for p in existing:
    brands[p['brand']] = brands.get(p['brand'], 0) + 1
print(f"Total: {len(existing)} phones, {len(brands)} brands")
for b, c in sorted(brands.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c}")
