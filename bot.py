#bot.py
import os
import discord
from parser import parse_event
from calendar_api import create_calendar_event
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.channel.name == "calendar":
        event = parse_event(message.content)

        if event is None:
            await message.channel.send("Sorry, I couldn't understand that.")
            return

        calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
        create_calendar_event(calendar_id, event)
        await message.channel.send(f"Added: {event['title']} at {event['start']}")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set")

client.run(TOKEN)