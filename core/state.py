import os
import json
from datetime import datetime, timezone, timedelta

SENT_TTL_HOURS = 6

sent_cache = {}

idx_status = "OFFLINE"

class MutableTime:
    def __init__(self):
        self.value = None

last_rss_check = MutableTime()
last_news_time = MutableTime()

def now_utc():
    return datetime.now(timezone.utc)

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

def cleanup_sent_cache():
    now = now_utc()
    expired = [
        k for k, v in sent_cache.items()
        if now - v > timedelta(hours=SENT_TTL_HOURS)
    ]
    for k in expired:
        del sent_cache[k]