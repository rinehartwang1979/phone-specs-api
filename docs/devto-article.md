# How I Built a Phone Specs API in 2 Days (and Launched It on RapidAPI)

I spent a weekend building a smartphone specifications API. Here's the tech stack, the decisions I made, and how you can build one too.

## Why Phone Specs?

I needed structured phone specification data for a comparison tool. Existing solutions were either:
- Too expensive ($99+/month)
- Outdated (2022 specs)
- Missing Chinese brands (Xiaomi, OPPO, vivo, Huawei)

So I built my own.

## The Stack

| Layer | Choice | Why |
|-------|--------|-----|
| API | FastAPI | Fast, auto-docs (Swagger), async |
| Data | JSON file | No DB overhead for 130 records |
| Hosting | Railway | Auto-deploy from GitHub, free tier |
| Distribution | RapidAPI | Built-in billing, rate limiting, discoverability |
| Search | In-memory | Python string scoring, no Elasticsearch |

Total monthly cost: **$0** (Railway free tier + RapidAPI free plan)

## The Schema

Each phone record has 38 fields covering:

- **Display**: size, type, resolution, refresh rate
- **Performance**: chipset, CPU cores, GPU, RAM, storage
- **Camera**: main, count, specs, front, video
- **Battery**: capacity, wired/wireless charging
- **Design**: weight, dimensions, water resistance, material
- **Connectivity**: 5G, NFC, infrared, headphone jack

```json
{
  "id": "samsung_galaxys25ultra",
  "brand": "Samsung",
  "model": "Galaxy S25 Ultra",
  "screen_size": "6.8英寸",
  "screen_type": "Dynamic LTPO AMOLED 2X",
  "resolution": "3120x1440",
  "refresh_rate": "120Hz",
  "chipset": "Snapdragon 8 Gen 4",
  "ram": "16GB",
  "storage": "512GB",
  "rear_camera_main": "200MP",
  "battery_capacity": "5000mAh",
  "os": "Android 15",
  "water_resistance": "IP68"
}
```

## The Endpoints

```bash
# Search by keyword
GET /api/v1/search?q=iPhone&limit=10

# Full specs by ID
GET /api/v1/specs/apple_iphone16promax

# Side-by-side comparison
GET /api/v1/compare?id1=apple_iphone16pro&id2=samsung_galaxys25ultra

# Brand catalog
GET /api/v1/brands

# Database stats
GET /api/v1/stats
```

That's it. Six endpoints. No auth required for the demo.

## Current Coverage

- **130+ phones** across 24 brands
- **Samsung** (20), **Xiaomi** (18), **Apple** (12), **Google** (8), **vivo** (8), **Huawei** (7), **OPPO** (7), **Realme** (7), **OnePlus** (5), **Nothing** (5), and more
- Chipsets: Snapdragon 8 Gen 3 (25 phones), A15 Bionic (4), Dimensity 9400 (3)

## Try It Live

The API has a live demo page at [phone-specs-api-production.up.railway.app](https://phone-specs-api-production.up.railway.app) — search any brand or chipset instantly.

Swagger docs at [/docs](https://phone-specs-api-production.up.railway.app/docs).

## Get It on RapidAPI

Available on RapidAPI with three pricing tiers:
- **Free** — 100 requests/day
- **Starter** — 1,000 requests/day
- **Pro** — 10,000 requests/day

[View on RapidAPI](https://rapidapi.com)

---

*Source code on [GitHub](https://github.com/rinehartwang1979/phone-specs-api) — MIT licensed.*
