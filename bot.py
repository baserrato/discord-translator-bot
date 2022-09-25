#!/usr/bin/python3
"""This script uses discord api to run a discord bot"""
import os
import discord
import re

from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    """"prints out to confirm that discord bot is ready"""
    print(str(client.user) + " has connected to Discord!")

@client.event
async def on_message(message):
    """Discord bot event handler to respond to certain triggers"""
    # to not event handle messages sent by the bot
    if message.author == client.user:
        return

    if "translate" in message.content.lower():
        wordRegex = re.compile("`[\w ]+`", re.UNICODE)
        result = wordRegex.search(message.content)
        testphrase = result.group()
        phrase = testphrase.replace("`", "")
        await message.channel.send(message.author.mention + " `" + phrase +"` means: `" + translator.translate(phrase).text + "`")

client.run(TOKEN)
