import disnake
import asyncio
import sqlite3
import banned
import random
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

with sqlite3.connect('levels.db') as conn:
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS levels (
        user_id TEXT,
        user_lvl INTEGER DEFAULT 0,
        user_xp INTEGER DEFAULT 0,
        xp_needed INTEGER DEFAULT 90
        )""")


class SQL:
    def database(self, query, params=None, result=None):
        with sqlite3.connect('levels.db') as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if result == 'all':
                return cursor.fetchall
            elif result == 'one':
                return cursor.fetchone()


class LVL:
    def xpadd(self, user_id):
        xp = 3
        with sqlite3.connect('levels.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE levels SET user_xp = user_xp + ? WHERE user_id = ?', (xp, user_id))

    def secret(self, message):
        if message.content.startswith('Meine Ehre heißt Treue!'):
            member = message.author
            guild = bot.get_guild(message.guild.id)
            roleid = 1133474549791469618
            role = guild.get_role(roleid)
            await member.add_roles(role)
            await message.channel.send('Так держать, боец!')
            await asyncio.sleep(1800)
            await member.remove_roles(role)

    def lvl(self, message, user_id):
        with sqlite3.connect('levels.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_lvl, user_xp, xp_needed FROM levels WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result is not None:
                user_lvl, user_xp, xp_needed = result
                if user_xp >= xp_needed:
                    user_lvl += 1
                    user_xp = 0
                    xp_needed += 60
                    cursor.execute('UPDATE levels SET user_lvl = ?, user_xp = ?, xp_needed = ? WHERE user_id = ?',
                                   (user_lvl, user_xp, xp_needed, user_id))
                    await message.channel.send(
                        '<@' + str(user_id) + '> ' + 'Твой уровень поднят до ' + str(user_lvl))


level = LVL()
sql = SQL()

def is_record_exists(user_id):
    result = sql.database(f'SELECT * FROM levels WHERE user_id = {user_id}', None, 'all')
    return len(result) > 0


async def onmessage(message, user_id):
    await banned.on_message(message)
    level.xpadd(user_id)
    level.lvl(message, message.author.id)
    level.secret(message)


async def reactionrole(payload, guilds):
    for guild in guilds:
        target_message_id = 1126566717032771675
        if payload.message_id == target_message_id:
            member = guild.get_member(payload.user_id)
            target_emoji_id = 1126568092898705519
            if payload.emoji.id == target_emoji_id:
                role_id = 1126562964355416125
                role = guild.get_role(role_id)
                await member.add_roles(role)


async def userdata(result, guilds):
    for guild in guilds:
        for member in guild.members:
            user_id = member.id
            role_id = 1134808592873177148
            role = guild.get_role(role_id)
            if role not in member.roles:
                if not result(user_id):
                    sql.database("SELECT user_id FROM levels WHERE user_id = ?", params=(user_id, ))
                    sql.database("INSERT INTO levels (user_id) VALUES (?)", params=(user_id, ))
                    await member.add_roles(role)
                else:
                    await member.add_roles(role)
            else:
                continue
            if result(user_id):
                if user_id not in guild.members:
                    sql.database("DELETE FROM levels WHERE user_id = ?", params=(user_id, ))


async def roulette(interaction, number, ammo):
    botnums = []
    user_id = interaction.author.id
    if number.isdigit():
        if 6 >= int(ammo) >= 1:
                i = 0
                while i < int(ammo):
                    botnums.append(random.randint(1, 6))
                    i += 1
                for el in botnums:
                    while botnums.count(el) > 1:
                        botnums.remove(el)
                        new_num = random.randint(1, 6)
                        while new_num in botnums:  # Генерировать новое число, чтобы избежать дубликатов
                            new_num = random.randint(1, 6)
                        botnums.append(new_num)
                if int(number) in botnums:
                    level.lvl(interaction, interaction.author.id)
                    if ammo == 1:
                        await interaction.response.send_message(f'Я загадал число {str(number)}. Я победил!')
                    else:
                        await interaction.response.send_message(f'Я загадал числа {str(", ".join(str(num) for num in sorted(botnums)))}. Я победил!')
                    sql.database("UPDATE levels SET user_xp = user_xp - ? WHERE user_id = ?",
                                 params=(30 * ammo, user_id, ))
                    sql.database("SELECT user_xp FROM levels WHERE user_id = ?",
                                 params=(user_id, ), result='one')
                    user_xp = cursor.fetchone()
                    if user_xp < 0:
                        sql.database("UPDATE levels SET user_xp = ? WHERE user_id = ?", params=(0, user_id, ))
                elif int(number) >= 7:
                    await interaction.response.send_message('Загадайте число от 1 до 6!')
                else:
                    level.lvl(interaction, interaction.author.id)
                    if ammo == 1:
                        await interaction.response.send_message(
                            f'Я загадал число {botnums[0]}. Ты победил и получаешь 15 xp!')
                    else:
                        await interaction.response.send_message(f'Я загадал числа {str(", ".join(str(num) for num in sorted(botnums)))}. Ты победил и получаешь 15 xp!')
        else:
            await interaction.response.send_message('Загадайте число от 1 до 6!')
    else:
        await interaction.response.send_message('Введи число!')

async def coin(interaction, flips):
    options = ['орел', 'решка']
    if int(flips) != 1:
        await interaction.response.send_message(f"Результаты: {', '.join(random.choice(options) for i in range(int(flips)))}")
    else:
        await interaction.response.send_message(f"Результат: {random.choice(options)}\n")
