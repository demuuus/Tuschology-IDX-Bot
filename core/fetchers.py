import asyncio
import feedparser
import aiohttp

USER_AGENT = "Mozilla/5.0 (compatible; IDXPriorityBot/1.0)"

async def fetch_feed(url):
    return await asyncio.to_thread(feedparser.parse, url, agent=USER_AGENT)

async def fetch_html(url):
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout, headers={"User-Agent": USER_AGENT}) as s:
        async with s.get(url) as r:
            return await r.text()