import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest
from telegram.error import TelegramError

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, RSS_FEEDS
from core.state import (
    last_rss_check,
    last_news_time,
    now_utc,
    idx_status
)

request = HTTPXRequest(
    connection_pool_size=20,
    connect_timeout=10,
    read_timeout=20,
    write_timeout=20,
    pool_timeout=20
)

telegram_bot = Bot(
    token=TELEGRAM_TOKEN,
    request=request
)

_send_queue = asyncio.Queue()

async def _telegram_worker():
    while True:
        chat_id, msg, preview = await _send_queue.get()
        try:
            await telegram_bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode="Markdown",
                disable_web_page_preview=preview
            )
        except TelegramError as e:
            print(f"[TELEGRAM SEND ERROR] {e}")
        await asyncio.sleep(0.3)
        _send_queue.task_done()

async def start_telegram_worker():
    asyncio.create_task(_telegram_worker())

async def send_telegram_broadcast(msg: str):
    await telegram_bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=msg,
        parse_mode="Markdown",
        disable_web_page_preview=False
    )

async def send_telegram_dm(chat_id: int, msg: str):
    await telegram_bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def telegram_status_listener():
    offset = None

    while True:
        try:
            updates = await telegram_bot.get_updates(
                offset=offset,
                timeout=30
            )

            for update in updates:
                offset = update.update_id + 1

                if not update.message:
                    continue

                if update.message.chat.type != "private":
                    continue

                if not update.message.text:
                    continue

                if update.message.text.strip() != "/status":
                    continue

                rss_info = (
                    "N/A"
                    if last_rss_check.value is None
                    else f"{int((now_utc() - last_rss_check.value).total_seconds())} detik"
                )

                news_info = (
                    "N/A"
                    if last_news_time.value is None
                    else f"{int((now_utc() - last_news_time.value).total_seconds())} detik"
                )

                msg = (
                    "🟢 *IDX News Bot — ONLINE*\n"
                    f"📡 Feeds aktif: {len(RSS_FEEDS)}\n"
                    f"⏱ Last RSS check: {rss_info} lalu\n"
                    f"📰 Last news: {news_info} lalu\n"
                    f"📊 IDX Status: {idx_status}"
                )

                await send_telegram_dm(update.message.chat.id, msg)

        except TelegramError as e:
            print(f"[TELEGRAM ERROR] {e}")
            await asyncio.sleep(5)

        except Exception as e:
            print(f"[TELEGRAM FATAL] {e}")
            await asyncio.sleep(5)