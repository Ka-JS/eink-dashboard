#bot.py
import os
import discord
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
        print(message.content)
        await message.channel.send(f"You said: {message.content}")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set")

client.run(TOKEN)