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
#removing default help for custom help command
client.remove_command('help')

@client.event
async def on_ready():
    """"prints out to confirm that discord bot is ready"""
    print(str(client.user) + " has connected to Discord!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        error_command = re.compile("\".+\"").search(str(error)).group().replace("\"", "")
        error_message = "Command `!" + error_command + "` Not Found.\n"
        if error_command.lower() == "help":
            error_message += "> Did you mean to use command: ```!help```"
        elif error_command.lower() == "lang":
            error_message += "> Did you mean to use command: ```!lang```"
        elif error_command.lower() == "source":
            error_message += "> Did you mean to use command: ```!source```"
        elif error_command.lower() == "translate":
            error_message += "> Did you mean to use command: ```!translate```"
        elif error_command.lower() == "pronounce":
            error_message += "> Did you mean to use command: ```!pronounce```"
        error_message += "\nRefer to the command `!help` to see available commands."
        await ctx.send(error_message)
    print(error)

@client.command(name="help")
async def help_command(ctx):
    embed_help = discord.Embed(
            title = "Translator Bot Help Listing",
            description = "Commands that can be called for the Translator Bot",
            color = discord.Color.blurple()
            )
    embed_help.add_field(name="**!lang**", value="> Displays a list of languages can be translated", inline=False)
    embed_help.add_field(name="**!source** ``` `[phrase to source]` ```", value="> Gives language source of phrase", inline=False)
    embed_help.add_field(name="**!translate** ``` `[phrase to translate]` ```", value="Translates phrase to chosen language (default is english)\n\nOptional Parameters:\n\n >>> \"[language to translate]\" -> Language to translate to \n\n\U0001F5E3 -> Add a pronunciation recording to be included", inline=False)
    embed_help.add_field(name="**!pronounce** ``` `[phrase to pronounce]` ```", value="> Shows the pronunciation of a phrase and gives a recording to hear the pronunciation", inline=False)
    await ctx.send(embed=embed_help)

@client.command(name='lang')
async def languages(ctx):
    embed_lang = discord.Embed(
            title = "Translator Bot Supported Languages",
            description = "A listing of all supported languages Translator Bot can translate to",
            color = discord.Color.blurple()
            )
    lang_support = ""
    lang_count = 0
    for idx, languages in enumerate(googletrans.LANGUAGES):
        if idx > 0 and idx % 6 == 0:
            lang_count += 1
            embed_lang.add_field(name="Language List #"+ str(lang_count), value=lang_support) 
            lang_support = ""
        lang_support += "`" + languages + "` = ***" + googletrans.LANGUAGES[languages] + "*** \n"
    lang_count += 1
    embed_lang.add_field(name="Language List #"+ str(lang_count), value=lang_support)
    embed_lang.set_footer(text = "Total of " + str(len(googletrans.LANGUAGES)) + " supported languages")
    await ctx.send(embed=embed_lang)

@client.command(name='source')
async def source(ctx):
    wordRegex = re.compile("`[\w\W]+`", re.UNICODE)
    result = wordRegex.search(ctx.message.content)
    if result != None:
        testPhrase = result.group()
        if testPhrase != None:
            phrase = testPhrase.replace("`", "")
            langSource = translator.detect(phrase).lang
            await ctx.send(ctx.message.author.mention + " The phrase `" + phrase + "` is `" + googletrans.LANGUAGES[langSource.lower()] + "`")
    else:
        await ctx.send("Missing argument for `!source` requires phrase to source\nCommand Usage:```!source `[phrase]` ```")

@client.command(name='translate')
async def translate(ctx):
    regexPhrase = re.compile("`.+`", re.UNICODE)
    regexDest = re.compile("\".+\"")
    testPhrase = regexPhrase.search(ctx.message.content)
    testDest = regexDest.search(ctx.message.content)
    if testPhrase != None:
        phrase = testPhrase.group().replace("`", "")
        if testDest != None:
            destination = testDest.group().replace("\"", "")
            try:
                translateResult = translator.translate(phrase, dest=destination)
                await ctx.send(ctx.message.author.mention + " `" + phrase + "` ("+ googletrans.LANGUAGES[translateResult.src.lower()] + ") translates to `"   +  googletrans.LANGUAGES[translateResult.dest.lower()] + "` as: `" + translateResult.text + "`")
            except:
                error_message = "Language requested `"+ destination +"` not recognized"
                if destination == "chinese":
                    error_message += "\nDid you mean `chinese (simplified)[zh-cn]` or `chinese (traditional)[zh-tw]?`"
                elif destination == "myanmar":
                    error_message += "\nDid you mean `myanmar (burmese)[my]`?"
                elif destination == "kurdish":
                    error_message += "\nDid you mean `kurdish (kurmanji)[ku]`?"
                error_message += "\nRefer to !lang command to see all supported languages"
                await ctx.send(error_message)
                return
            emojiExtract = re.compile("\U0001F5E3")
            emojiFind = emojiExtract.search(ctx.message.content)
            if emojiFind != None:
                try:
                    tts = gTTS(translateResult.text, lang = translateResult.dest.lower())
                    tts.save('dest.mp3')
                    await ctx.send(file=discord.File(r'dest.mp3'))
                except:
                    await ctx.send("\U0001F5E3 Recording not supported for language `"+ googletrans.LANGUAGES[translateResult.dest.lower()] +"`" )
        else:
            translateResult = translator.translate(phrase)
            await ctx.send(ctx.message.author.mention + " `" + phrase + "` ["+ googletrans.LANGUAGES[translateResult.src.lower()] + "] translates to `"   +  googletrans.LANGUAGES[translateResult.dest.lower()] + "` as: `" + translateResult.text + "`")
            emojiExtract = re.compile("\U0001F5E3")
            emojiFind = emojiExtract.search(ctx.message.content)
            if emojiFind != None:
                tts = gTTS(translateResult.text, lang = translateResult.dest.lower())
                tts.save('dest.mp3')
                await ctx.send(file=discord.File(r'dest.mp3'))
    elif testPhrase == None:
        await ctx.send("Missing argument for `!translate` requires phrase to translate\nCommand Usage:```Default:\n!translate `[phrase]`\n\nOptional:\n!translate `[phrase]` \"[translate to language]\"```")

@client.command(name='pronounce')
async def pronounce(ctx):
    wordRegex = re.compile("`[\w ]+`", re.UNICODE)
    result = wordRegex.search(ctx.message.content)
    if result != None:
        testPhrase = result.group()
        if testPhrase != None:
            phrase = testPhrase.replace("`", "")
            langSource = translator.detect(phrase).lang
            langPronounce = translator.translate(phrase, dest = langSource.lower())
            tts = gTTS(phrase, lang = langSource.lower())
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
