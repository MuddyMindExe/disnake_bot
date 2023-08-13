import disnake
import logging
import asyncio
import sqlite3
import moder
import defmodule
from disnake.ext import commands

bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all())
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await defmodule.userdata(defs.is_record_exists, bot.guilds)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
     await defmodule.onmessage(message, message.author.id)

@bot.event
async def on_raw_reaction_add(payload):
    await defmodule.reactionrole(payload, bot.guilds)

bot.run('YOUR_TOKEN')