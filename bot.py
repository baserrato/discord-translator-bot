#!/usr/bin/python3.8
import os
import discord
import translator

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(str(client.user) + " has connected to Discord!")

@client.event
async def on_message(message):
    # to not event handle messages sent by the bot
    if message.author == client.user:
        return

    if "hello world" in message.content.lower():
        await message.channel.send("🌎 Hello World to you to!" + message.author.mention + "🌎")
    
client.run(TOKEN)
