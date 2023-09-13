import disnake
import defs
from disnake.ext import commands


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all(), test_guilds=[1073728801344852009])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await defs.userdata(defs.is_record_exists, bot.guilds)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        await defs.onmessage(message, message.author.id)


@bot.event
async def on_raw_reaction_add(payload):
    await defs.reactionrole(payload, bot.guilds)


@bot.slash_command(name='рулетка', description='загадай число от 1 до 6')
async def roulete(interaction, number, ammo):
    await defs.roulette(interaction, number, ammo)


@bot.slash_command(name='монетка', description='подбрасывание монетки')
async def coin(interaction, flips):
    await defs.coin(interaction, flips)

bot.run('YOUR_TOKEN')
