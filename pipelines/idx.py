import asyncio
import hashlib
import re
from bs4 import BeautifulSoup

from config import IDX_URL, IDX_INTERVAL, IDX_STATE_FILE
from core.state import load_json, save_json, now_utc
from core.market import is_market_open
from core.utils import is_maintenance_page, escape_markdown
from core.fetchers import fetch_html
from platforms.discord import send_discord, set_presence
from platforms.telegram import send_telegram_broadcast

idx_state = load_json(
    IDX_STATE_FILE,
    {
        "status": "OFFLINE",
        "sent_ids": []
    }
)

VALID_PATHS = (
    "/id/berita/pengumuman/",
    "/id/berita/suspensi/",
    "/id/berita/unusual-market-activity",
    "/id/berita/keterbukaan-informasi"
)

async def idx_pipeline():
    while True:
        try:
            html = await fetch_html(IDX_URL)

            if is_maintenance_page(html):
                if idx_state["status"] != "MAINTENANCE":
                    idx_state["status"] = "MAINTENANCE"
                    save_json(IDX_STATE_FILE, idx_state)

                    await set_presence("IDX Maintenance")

                    msg = (
                        "⚠️ *IDX STATUS UPDATE*\n"
                        "🛠️ Website IDX sedang maintenance\n"
                        f"🕒 {now_utc().strftime('%H:%M:%S WIB')}"
                    )

                    await send_discord(msg)
                    await send_telegram_broadcast(msg)

                await asyncio.sleep(IDX_INTERVAL)
                continue

            if idx_state["status"] in ("OFFLINE", "MAINTENANCE"):
                idx_state["status"] = "ACTIVE"
                save_json(IDX_STATE_FILE, idx_state)

                await set_presence("IDX & Market News")

                msg = (
                    "✅ *IDX STATUS UPDATE*\n"
                    "📈 Website IDX aktif kembali\n"
                    f"🕒 {now_utc().strftime('%H:%M:%S WIB')}"
                )

                await send_discord(msg)
                await send_telegram_broadcast(msg)

            soup = BeautifulSoup(html, "html.parser")
            anchors = soup.find_all("a", href=True)

            sent_count = 0

            for a in anchors:
                if sent_count >= 5:
                    break

                href = a["href"]

                if not any(p in href for p in VALID_PATHS):
                    continue

                title = a.get_text(strip=True)
                if not title or len(title) < 10:
                    continue

                link = (
                    href
                    if href.startswith("http")
                    else f"https://www.idx.co.id{href}"
                )

                hid = hashlib.sha256(link.encode()).hexdigest()
                if hid in idx_state["sent_ids"]:
                    continue

                t = title.lower()
                if "suspensi" in t:
                    category = "Suspensi Saham"
                elif "uma" in t:
                    category = "Unusual Market Activity"
                elif "keterbukaan" in t:
                    category = "Keterbukaan Informasi"
                else:
                    category = "Pengumuman Emiten"

                em = re.search(r"\b[A-Z]{4}\b", title)
                emiten = em.group(0) if em else "N/A"

                await set_presence("IDX Priority Alert")

                msg = (
                    "🚨 *IDX PRIORITY ALERT*\n\n"
                    f"📄 *Jenis:* {category}\n"
                    f"🏢 *Emiten:* {emiten}\n"
                    f"📰 *Judul:* {escape_markdown(title)}\n"
                    f"🔗 {link}"
                )

                await send_discord(msg)
                await send_telegram_broadcast(msg)

                idx_state["sent_ids"].append(hid)
                idx_state["sent_ids"] = idx_state["sent_ids"][-500:]
                save_json(IDX_STATE_FILE, idx_state)

                sent_count += 1
                asyncio.create_task(reset_presence_after(600))

            if sent_count == 0:
                if not is_market_open():
                    await set_presence("Market Closed")
                else:
                    await set_presence("IDX & Market News")

        except Exception as e:
            print(f"[IDX ERROR] {e}")

        await asyncio.sleep(IDX_INTERVAL)

async def reset_presence_after(seconds: int):
    await asyncio.sleep(seconds)

    if not is_market_open():
        await set_presence("Market Closed")
    else:
        await set_presence("IDX & Market News")