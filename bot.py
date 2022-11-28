#!/usr/bin/python3
"""This script uses discord api to run a discord bot"""
import os
import googletrans
import discord
import re
import time
import subprocess
import socket
import requests
import json

from gtts import gTTS
from googletrans import Translator
from dotenv import load_dotenv
from discord.ext import commands

def connect():
        try:
            r = requests.get('http://localhost:4040')
            fields = r.json()
            if fields["name"] == socket.gethostname():
                return True
            else:
                return False
        except:
            return False

#while not connect():
#    print("Awaiting Lease...")
#    time.sleep(5)

print("Lease Acquired!")

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix="!")
translator = Translator()
client.remove_command('help')

@client.event
async def on_ready():
    """"prints out to confirm that discord bot is ready"""
    print(str(client.user) + " has connected to Discord!")

@client.command(name="help")
async def help_command(ctx):
    help_string = "```Commands you can run with this bot: \n \n"
    help_string += "!lang -> shows a list of languages can be translated \n\n"
    help_string += "!source `[phrase to translate]` -> gives language source of phrase. \n\n"
    help_string += "!translate `[phrase to translate]` \"[language to translate to(optional)]\" \n\t\t-> translates phrase to chosen language (default is english)```"
    await ctx.send(help_string)

@client.command(name='lang')
async def languages(ctx):
    lang_string = "```"
    for idx, languages in enumerate(googletrans.LANGUAGES):
        lang_string += languages + " = " + googletrans.LANGUAGES[languages]
        if idx % 3 == 0 and idx != 0:
            lang_string += "\n"
        elif idx < len(googletrans.LANGUAGES) - 1:
            lang_string += " | "
    lang_string += "```"
    await ctx.send(lang_string)

@client.command(name='source')
async def source(ctx):
    wordRegex = re.compile("`[\w ]+`", re.UNICODE)
    result = wordRegex.search(ctx.message.content)
    if result != None:
        testPhrase = result.group()
        if testPhrase != None:
            phrase = testPhrase.replace("`", "")
            langSource = translator.detect(phrase).lang
            await ctx.send(ctx.message.author.mention + " The phrase `" + phrase + "` is `" + googletrans.LANGUAGES[langSource] + "`")
    else:
        await ctx.send("Missing argument for `!source` requires phrase to source\nCommand Usage:```!source `[phrase]` ```")

@client.command(name='translate')
async def translate(ctx):
    regexPhrase = re.compile("`[\w ]+`", re.UNICODE)
    regexDest = re.compile("\"[A-Za-z]+\"")
    testPhrase = regexPhrase.search(ctx.message.content)
    testDest = regexDest.search(ctx.message.content)
    if testPhrase != None:
        phrase = testPhrase.group().replace("`", "")
        if testDest != None:
            destination = testDest.group().replace("\"", "")
            translateResult = translator.translate(phrase, dest=destination)
            tts = gTTS(translateResult.text, lang = translateResult.dest)
            tts.save('dest.mp3')
            await ctx.send(ctx.message.author.mention + " `" + phrase + "` ("+ googletrans.LANGUAGES[translateResult.src] + ") translates to `"   +  googletrans.LANGUAGES[translateResult.dest] + "` as: `" + translateResult.text + "`")
            await ctx.send(file=discord.File(r'dest.mp3'))
        else:
            translateResult = translator.translate(phrase)
            await ctx.send(ctx.message.author.mention + " `" + phrase + "` ("+ googletrans.LANGUAGES[translateResult.src] + ") translates to `"   +  googletrans.LANGUAGES[translateResult.dest] + "` as: `" + translateResult.text + "`")
    elif testPhrase == None:
        await ctx.send("Missing argument for `!translate` requires phrase to source\nCommand Usage:```Default:\n!translate `[phrase]`\n\nOptional:\n!translate `[phrase]` \"[translate to language]\"```")

@client.command(name='pronounce')
async def pronounce(ctx):
    wordRegex = re.compile("`[\w ]+`", re.UNICODE)
    result = wordRegex.search(ctx.message.content)
    if result != None:
        testPhrase = result.group()
        if testPhrase != None:
            phrase = testPhrase.replace("`", "")
            langSource = translator.detect(phrase).lang
            langPronounce = translator.translate(phrase, dest = langSource)
            tts = gTTS(phrase, lang = langSource)
            tts.save('pronounce.mp3')
            if langPronounce.pronunciation != None:
                await ctx.send(ctx.message.author.mention + " The phrase `" + phrase + "` pronunciation is `" + str(langPronounce.pronunciation) + "`")
            else:
                await ctx.send(ctx.message.author.mention + " The phrase `" + phrase + "` pronunciation is `" + phrase + "`")
            await ctx.send(file=discord.File(r'pronounce.mp3'))
    else:
        await ctx.send("Missing argument for `!pronounce` requires phrase to pronounce\nCommand Usage:```!pronounce `[phrase]` ```")

@client.event
async def on_message(message):
    #ignores when author of message is the bot itself
    if message.author == client.user:
        return
    #processes commands that are used in a message
    await client.process_commands(message)

client.run(TOKEN)
