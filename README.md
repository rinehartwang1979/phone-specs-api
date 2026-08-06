# Phone Specs API

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

**REST API for smartphone specifications** — 132 phones across 24 brands with 38 field structured schema. Deployed on Railway, distributed via [RapidAPI](https://rapidapi.com).

## Quick Start

```bash
# Search phones
curl "https://phone-specs-api-production.up.railway.app/api/v1/search?q=iPhone"

# Get full specs
curl "https://phone-specs-api-production.up.railway.app/api/v1/specs/apple_iphone16promax"

# Compare two phones
curl "https://phone-specs-api-production.up.railway.app/api/v1/compare?id1=apple_iphone16promax&id2=samsung_galaxys25ultra"

# List all brands
curl "https://phone-specs-api-production.up.railway.app/api/v1/brands"

# Database stats
curl "https://phone-specs-api-production.up.railway.app/api/v1/stats"

# Health check
curl "https://phone-specs-api-production.up.railway.app/api/v1/health"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/search?q={keyword}` | Full-text search by brand, model, chipset, OS |
| GET | `/api/v1/search?q={keyword}&fields=id,brand,chipset` | Search with field filtering |
| GET | `/api/v1/specs/{phone_id}` | Detailed specs for one phone |
| GET | `/api/v1/compare?id1={id}&id2={id}` | Side-by-side comparison |
| GET | `/api/v1/brands` | All brands with phone counts |
| GET | `/api/v1/stats` | Database statistics |
| GET | `/api/v1/health` | Service health & record count |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/redoc` | ReDoc documentation |

## Example Response (Search)

```json
{
  "query": "Galaxy S25",
  "count": 3,
  "results": [
    {
      "id": "samsung_galaxys25ultra",
      "brand": "Samsung",
      "model": "Galaxy S25 Ultra",
      "model_name": "Galaxy S25 Ultra",
      "screen_size": "6.8英寸",
      "screen_type": "Dynamic LTPO AMOLED 2X",
      "resolution": "3120x1440",
      "refresh_rate": "120Hz",
      "chipset": "Snapdragon 8 Gen 4",
      "ram": "16GB",
      "storage": "512GB",
      "rear_camera_main": "200MP",
      "battery_capacity": "5000mAh",
      "charging_wired": "45W",
      "os": "Android 15",
      "network_5g": true,
      "water_resistance": "IP68",
      "weight": "219g"
    }
  ]
}
```

## Full Schema (38 fields)

Each phone record includes:

**Basic**: `id`, `brand`, `model`, `model_name`
**Display**: `screen_size`, `screen_type`, `resolution`, `refresh_rate`
**Performance**: `chipset`, `cpu_cores`, `gpu`, `ram`, `storage`, `storage_expandable`
**Camera**: `rear_camera_main`, `rear_camera_count`, `rear_camera_specs`, `front_camera`, `video`
**Battery**: `battery_capacity`, `charging_wired`, `charging_wireless`, `fast_charging`
**Software**: `os`
**Connectivity**: `network_5g`, `sim_type`, `nfc`, `infrared`
**Design**: `weight`, `dimensions`, `water_resistance`, `material`
**Security**: `fingerprint`, `face_unlock`
**Ports**: `headphone_jack`
**Metadata**: `launch_date`, `source`, `source_url`, `fetched_at`

## Database Coverage

| Brand | Phones | Key Models |
|-------|--------|------------|
| Samsung | 20 | S25/S24/S23, Z Flip/Fold, A/M series |
| Xiaomi | 18 | Xiaomi 14/15, Redmi Note, Poco F/X |
| Apple | 12 | iPhone 13-16 (Pro/Max/Plus) |
| Google | 8 | Pixel 7/8/9 (Pro/a/XL) |
| vivo | 8 | X100/X200, iQOO |
| Huawei | 7 | Mate 70, Pura 70, Nova |
| OPPO | 7 | Find X8, Reno, A series |
| Realme | 7 | GT 6/7, 13/14 Pro |
| Motorola | 6 | Edge 50, Razr 50 |
| OnePlus | 5 | OnePlus 13, Nord, Ace |
| + 14 more brands | | Honor, Nothing, Sony, ASUS, Tecno, Infinix, ZTE... |

## Pagination Support

The API supports the `limit` parameter for search results:

```bash
curl "https://.../api/v1/search?q=Samsung&limit=50"
```

Max 100 results per request.

## RapidAPI Integration

Listed on RapidAPI with 3 pricing plans — see the RapidAPI dashboard for subscription details.

The API uses JSON response format and includes standard HTTP headers:
- `X-API-Version`: API version
- `X-RateLimit-Remaining`: Request quota (1000/hour on free plan)

## Local Development

```bash
# Install dependencies
pip install fastapi uvicorn

# Run locally
cd api && uvicorn main:app --reload

# Or via Railway CLI
railway run uvicorn api.main:app --host 0.0.0.0 --port 8000

# Swagger docs at http://localhost:8000/docs
```

## Adding New Phones

Edit `data/phones.json` — each entry follows the 38-field schema. Use `scraper/gsmarena_converter.py` to convert GSMArena browser-extracted data into the internal schema.

```python
# Example: add a new phone
new_phone = {
    "id": "brand_model",
    "brand": "Brand",
    "model": "Model Name",
    "model_name": "Model Name",
    # ... remaining 35 fields
}
# Append to data/phones.json array
```

## Stack

- **Backend**: FastAPI (Python)
- **Deploy**: Railway + GitHub auto-deploy
- **Distribution**: RapidAPI marketplace
- **Search**: In-memory inverted scoring
- **Data**: Static JSON, 5-min cache

## License

MIT
