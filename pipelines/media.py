import asyncio
from datetime import datetime, timezone, timedelta

from config import RSS_FEEDS, MEDIA_INTERVAL, STATE_FILE
from core.state import (
    now_utc,
    load_json,
    save_json,
    sent_cache,
    cleanup_sent_cache,
    last_rss_check,
    last_news_time
)
from core.fetchers import fetch_feed
from core.utils import escape_markdown
from platforms.discord import send_discord
from platforms.telegram import send_telegram_broadcast
from core.filters import is_relevant

MAX_AGE_DAYS = 3
media_last_seen = load_json(STATE_FILE, {k: None for k in RSS_FEEDS})

def is_recent(entry) -> bool:
    if not hasattr(entry, "published_parsed") or not entry.published_parsed:
        return True

    published = datetime(
        *entry.published_parsed[:6],
        tzinfo=timezone.utc
    )

    return now_utc() - published <= timedelta(days=MAX_AGE_DAYS)

async def media_pipeline():
    while True:
        last_rss_check.value = now_utc()
        cleanup_sent_cache()

        for source, url in RSS_FEEDS.items():
            try:
                feed = await fetch_feed(url)
                if not feed.entries:
                    continue

                if media_last_seen.get(source) is None:
                    media_last_seen[source] = (
                        feed.entries[0].get("id")
                        or feed.entries[0].get("link")
                    )
                    continue

                for entry in feed.entries:
                    entry_id = entry.get("id") or entry.get("link")
                    if not entry_id:
                        continue

                    if entry_id == media_last_seen[source]:
                        break

                    if entry_id in sent_cache:
                        continue

                    if not is_recent(entry):
                        continue

                    if not is_relevant(entry.title):
                        continue

                    title = escape_markdown(entry.title)

                    msg = (
                        f"📰 *{title}*\n"
                        f"🏷️ *Sumber:* {source}\n"
                        f"🔗 {entry.link}"
                    )

                    await send_discord(msg)
                    await send_telegram_broadcast(msg)

                    sent_cache[entry_id] = now_utc()
                    last_news_time.value = now_utc()

                media_last_seen[source] = (
                    feed.entries[0].get("id")
                    or feed.entries[0].get("link")
                )
                save_json(STATE_FILE, media_last_seen)

            except Exception as e:
                print(f"[MEDIA ERROR] {source}: {e}")

        await asyncio.sleep(MEDIA_INTERVAL)