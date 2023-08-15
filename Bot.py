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

@bot.slash_command(name='roulette', description='make a number from 1 to 6')
async def roulete(interaction, number, ammo):
    await defs.roulette(interaction, number, ammo)

@bot.slash_command(name='coin', description='fliping a coin')
async def coin(interaction, flips):
    await defs.coin(interaction, flips)

bot.run('YOUR_TOKEN')