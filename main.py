import asyncio
from config import DISCORD_TOKEN
from platforms.discord import client, set_presence
from platforms.telegram import telegram_status_listener, start_telegram_worker
from pipelines.idx import idx_pipeline
from pipelines.media import media_pipeline
from core.market import is_market_open

async def market_presence_watcher():
    while True:
        if is_market_open():
            await set_presence("IDX & Market News")
        else:
            await set_presence("Market Closed")
        await asyncio.sleep(300)

@client.event
async def on_ready():
    await start_telegram_worker()
    if is_market_open():
        await set_presence("IDX & Market News")
    else:
        await set_presence("Market Closed")

    client.loop.create_task(idx_pipeline())
    client.loop.create_task(media_pipeline())
    client.loop.create_task(telegram_status_listener())
    client.loop.create_task(market_presence_watcher())


    print("✅ Tuschology is online")

def main():
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()