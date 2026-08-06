"""Batch 6: add ~40 more phones → 150+"""
import json
from datetime import datetime, timezone

DATA_PATH = '/mnt/c/Users/Reinhart/Desktop/hermes/api-data-service/data/phones.json'
with open(DATA_PATH) as f:
    existing = json.load(f)

existing_keys...[truncated]