import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID not found in environment")

CHANNEL_TOPIC_MARKER = "TCHNEWS"

RSS_FEEDS = {
    "CNBC": "https://www.cnbcindonesia.com/market/rss",
    "CNN": "https://www.cnnindonesia.com/ekonomi/rss",
    "Tempo": "https://rss.tempo.co/bisnis",
    "Antara": "https://en.antaranews.com/rss/news.xml",
    "Kontan": "https://rss.kontan.co.id/news/keuangan",
    "Bloomberg Technoz": "https://www.bloombergtechnoz.com/rss"
}

IDX_URL = "https://idx.co.id/id/berita/pengumuman/"

MEDIA_INTERVAL = 60
IDX_INTERVAL = 300

STATE_FILE = "media_state.json"
IDX_STATE_FILE = "idx_state.json"

MAX_AGE_DAYS = 3
SENT_TTL_HOURS = 6

USER_AGENT = "Mozilla/5.0 (compatible; IDXPriorityBot/1.0)"