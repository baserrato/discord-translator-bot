#!/usr/bin/python3
"""This script uses discord api to run a discord bot"""
import os
import googletrans
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

    if "source" in message.content.lower():
        wordRegex = re.compile("`[\w ]+`", re.UNICODE)
        result = wordRegex.search(message.content)
        testPhrase = result.group()
        phrase = testPhrase.replace("`", "")
        langSource = translator.detect(phrase).lang
        await message.channel.send(message.author.mention + " The phrase `" + phrase + "` is `" + googletrans.LANGUAGES[langSource] + "`")

    if "translate" in message.content.lower():
        regexPhrase = re.compile("`[\w ]+`", re.UNICODE)
        regexDest = re.compile("\"[a-zA-Z_ ]+\"")
        testPhrase = regexPhrase.search(message.content)
        testDest = regexDest.search(message.content)
        phrase = testPhrase.group().replace("`", "")
        if testDest != None:
            destination = testDest.group().replace("\"", "")
            translateResult = translator.translate(phrase, dest=destination)
            await message.channel.send(message.author.mention + " `" + phrase + "` translates to `"   +  googletrans.LANGUAGES[translateResult.dest] + "` as: `" + translateResult.text + "`")
        else:
            translateResult = translator.translate(phrase)
            await message.channel.send(message.author.mention + " `" + phrase + "` translates to `"   +  googletrans.LANGUAGES[translateResult.dest] + "` as: `" + translateResult.text + "`")
         
client.run(TOKEN)
