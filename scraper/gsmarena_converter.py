"""
GSMArena spec JSON → PhoneSpecs schema converter
Takes browser_console output and maps to our internal schema.
"""
import json, os, re, sys
sys.path.insert(0, '/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service')
from scraper.schema import PhoneSpecs

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def parse_gsmarena_to_phonespec(gsm_json: dict) -> dict:
    """Convert GSMArena browser console JSON to our PhoneSpecs format."""
    name = gsm_json.get('__name__', '')
    network = gsm_json.get('Network', {})
    launch = gsm_json.get('Launch', {})
    body = gsm_json.get('Body', {})
    display = gsm_json.get('Display', {})
    platform = gsm_json.get('Platform', {})
    memory = gsm_json.get('Memory', {})
    main_cam = gsm_json.get('Main Camera', {})
    selfie_cam = gsm_json.get('Selfie camera', {})
    sound = gsm_json.get('Sound', {})
    comms = gsm_json.get('Comms', {})
    features = gsm_json.get('Features', {})
    battery = gsm_json.get('Battery', {})
    misc = gsm_json.get('Misc', {})
    
    # Parse dimensions
    dims = body.get('Dimensions', '')
    w_match = re.search(r'(\d+\.?\d*) g', body.get('Weight', ''))
    
    # Parse display
    size_match = re.search(r'(\d+\.?\d*) inches', display.get('Size', ''))
    res_match = re.search(r'(\d+)\s*x\s*(\d+)', display.get('Resolution', ''))
    ppi_match = re.search(r'(\d+)\s*ppi', display.get('Resolution', ''))
    
    # Parse battery
    bat_match = re.search(r'(\d+)\s*mAh', battery.get('Type', ''))
    charge_power = re.search(r'(\d+)W', battery.get('Charging', ''))
    
    # Parse OS/Android version
    os_str = platform.get('OS', '')
    android_match = re.search(r'Android\s*(\d+)', os_str)
    
    # Parse chipset
    chipset = platform.get('Chipset', '')
    
    # Parse RAM/Storage
    mem_str = memory.get('Internal', '')
    ram_match = re.search(r'(\d+)GB\s*RAM', mem_str)
    storages = re.findall(r'(\d+)GB', mem_str.replace('RAM', ''))
    
    # Parse main camera
    main_mp = re.search(r'(\d+)\s*MP', main_cam.get(list(main_cam.keys())[0] if main_cam else '', ''))
    selfie_mp = re.search(r'(\d+)\s*MP', selfie_cam.get('Single', ''))
    
    # Parse colors
    colors = misc.get('Colors', '').split(', ')
    
    # Parse price
    price_str = misc.get('Price', '')
    usd_match = re.search(r'\$\s*([\d,]+\.?\d*)', price_str)
    
    # Brand detection
    brands_map = {
        'Apple': 'Apple', 'iPhone': 'Apple',
        'Samsung': 'Samsung', 'Galaxy': 'Samsung',
        'Xiaomi': 'Xiaomi', 'Redmi': 'Xiaomi', 'POCO': 'Xiaomi',
        'Huawei': 'Huawei',
        'OPPO': 'OPPO', 'OnePlus': 'OnePlus',
        'vivo': 'vivo', 'Vivo': 'vivo',
        'Google': 'Google', 'Pixel': 'Google',
        'Sony': 'Sony', 'Xperia': 'Sony',
        'Nothing': 'Nothing', 'Motorola': 'Motorola',
        'Realme': 'Realme', 'Honor': 'Honor',
        'ASUS': 'ASUS', 'Zenfone': 'ASUS', 'ROG': 'ASUS',
        'Tecno': 'Tecno', 'Infinix': 'Infinix',
        'TCL': 'TCL', 'SHARP': 'SHARP',
        'Meizu': 'Meizu', 'ZTE': 'ZTE',
        'Nokia': 'Nokia', 'Lenovo': 'Lenovo',
    }
    
    brand = 'Other'
    for key, val in brands_map.items():
        if key.lower() in name.lower():
            brand = val
            break
    
    # Determine body material
    build = body.get('Build', '')
    back_material = 'glass' if 'glass back' in build.lower() else 'other'
    frame_material = 'aluminum' if 'aluminum' in build.lower() else 'other'
    
    # IP rating
    ip_match = re.search(r'IP(\d+)', body.get('Build', '') + body.get('SIM', '') + battery.get('Type', ''))
    
    # Refresh rate
    refresh_match = re.search(r'(\d+)\s*Hz', display.get('Type', '') + display.get('Size', ''))
    
    # Dimensions
    dim_parts = re.findall(r'(\d+\.?\d*)', dims.split('mm')[0] if 'mm' in dims else '')
    height = float(dim_parts[0]) if len(dim_parts) >= 1 else None
    width = float(dim_parts[1]) if len(dim_parts) >= 2 else None
    thickness = float(dim_parts[2]) if len(dim_parts) >= 3 else None
    
    return {
        'id': 0,  # will be assigned later
        'name': name,
        'brand': brand,
        'model': name.replace(brand, '').strip(),
        'release_date': launch.get('Announced', '').split(',')[0] if 'Announced' in launch else '',
        'price_cny': None,
        'price_usd': float(usd_match.group(1).replace(',', '')) if usd_match else None,
        'os': os_str.split(',')[0].strip() if os_str else '',
        'android_version': int(android_match.group(1)) if android_match else None,
        'chipset': chipset,
        'cpu': platform.get('CPU', ''),
        'gpu': platform.get('GPU', ''),
        'ram_gb': int(ram_match.group(1)) if ram_match else None,
        'storage_gb': int(storages[0]) if storages else None,
        'storage_options': storages,
        'screen_size_inch': float(size_match.group(1)) if size_match else None,
        'screen_resolution': f"{res_match.group(1)}x{res_match.group(2)}" if res_match else '',
        'screen_ppi': int(ppi_match.group(1)) if ppi_match else None,
        'screen_type': display.get('Type', '').split(',')[0],
        'refresh_rate_hz': int(refresh_match.group(1)) if refresh_match else None,
        'battery_mah': int(bat_match.group(1)) if bat_match else None,
        'charging_watt': int(charge_power.group(1)) if charge_power else None,
        'rear_camera_mp': int(main_mp.group(1)) if main_mp else None,
        'rear_camera_detail': main_cam.get(list(main_cam.keys())[0] if main_cam else '', ''),
        'front_camera_mp': int(selfie_mp.group(1)) if selfie_mp else None,
        'front_camera_detail': selfie_cam.get('Single', ''),
        'weight_g': int(round(float(w_match.group(1)))) if w_match else None,
        'height_mm': height,
        'width_mm': width,
        'thickness_mm': thickness,
        'body_material': build,
        'back_material': back_material,
        'frame_material': frame_material,
        'waterproof': f'IP{ip_match.group(1)}' if ip_match else '',
        'five_g': '5G' in network.get('Technology', ''),
        'nfc': comms.get('NFC', '') == 'Yes',
        'bluetooth': comms.get('Bluetooth', ''),
        'wifi': comms.get('WLAN', ''),
        'usb': comms.get('USB', ''),
        'headphone_jack': sound.get('3.5mm jack', '') == 'Yes',
        'stereo_speakers': 'stereo' in sound.get('Loudspeaker', '').lower(),
        'colors': colors,
        'data_source': 'gsmarena.com',
        'source_url': gsm_json.get('__url__', ''),
    }


def merge_specs(existing_path: str, new_specs: list[dict]) -> list[dict]:
    """Merge new specs into existing, avoiding duplicates by name+brand."""
    existing = []
    if os.path.exists(existing_path):
        with open(existing_path) as f:
            existing = json.load(f)
    
    existing_keys = {(s['name'], s['brand']) for s in existing}
    
    for spec in new_specs:
        key = (spec['name'], spec['brand'])
        if key not in existing_keys:
            existing.append(spec)
            existing_keys.add(key)
    
    # Reassign IDs
    for i, spec in enumerate(existing, 1):
        spec['id'] = i
    
    return existing


# --- When run as script with JSON file argument ---
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Load GSMArena JSON file(s)
        new_specs = []
        for fpath in sys.argv[1:]:
            with open(fpath) as f:
                gsm_data = json.load(f)
            spec = parse_gsmarena_to_phonespec(gsm_data)
            new_specs.append(spec)
            print(f"Parsed: {spec['name']} ({spec['brand']})")
        
        # Merge with existing
        data_path = '/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service/data/phones.json'
        merged = merge_specs(data_path, new_specs)
        
        with open(data_path, 'w') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        
        print(f"Total phones: {len(merged)}")
    else:
        print("Usage: python3 gsmarena_converter.py <gsmarena_json_file> [...]")
