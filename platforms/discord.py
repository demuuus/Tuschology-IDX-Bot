import discord
from discord import Activity, ActivityType
from config import CHANNEL_TOPIC_MARKER

intents = discord.Intents.default()
client = discord.Client(intents=intents)

current_presence = None

async def set_presence(text):
    global current_presence
    if current_presence == text:
        return
    current_presence = text
    await client.change_presence(
        activity=Activity(type=ActivityType.watching, name=text)
    )

def get_target_channels():
    out = []
    for g in client.guilds:
        for c in g.text_channels:
            print(f"[DEBUG] {c.name} | topic={c.topic}")
            if c.topic and CHANNEL_TOPIC_MARKER in c.topic:
                out.append(c)
    return out


async def send_discord(msg):
    for c in get_target_channels():
        try:
            await c.send(msg)
        except Exception as e:
            print(f"[DISCORD SEND ERROR] {c.name}: {e}")