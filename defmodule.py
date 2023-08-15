import disnake
import logging
import asyncio
import sqlite3
import moder
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect('DB file location')
cursor = conn.cursor()

#change all 'name' to name of your table
cursor.execute(""" CREATE TABLE IF NOT EXISTS name ( 
    user_id TEXT,
    user_lvl INTEGER,
    user_xp INTEGER,
    xp_needed INTEGER
    )""")
async def onmessage(message, user_id):
    await moder.on_message(message)  # <- checks on banned words
    xp = 3
    cursor.execute('UPDATE name SET user_xp = user_xp + ? WHERE user_id = ?', (xp, user_id)) # <- updates user_xp after every message
    cursor.execute('SELECT user_lvl, user_xp, xp_needed FROM name WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    user_lvl, user_xp, xp_needed = result
    if user_xp >= xp_needed: # <- updates user_lvl if user_xp >= xp_needed
        user_lvl += 1
        user_xp = 0
        xp_needed += 60
        cursor.execute('UPDATE name SET user_lvl = ?, user_xp = ?, xp_needed = ? WHERE user_id = ?',
                       (user_lvl, user_xp, xp_needed, user_id))
        await message.channel.send('<@' + str(message.author.id) + '> ' + 'Your new lvl is now - ' + str(user_lvl))
    conn.commit()
    if message.content.startswith('Messagge'): #gives user special role for 30 min if he writes special message
        member = message.author
        guild = bot.get_guild(message.guild.id)
        roleid = #role id as integer
        role = guild.get_role(roleid)
        await member.add_roles(role)
        await message.channel.send('messagge that bot will send')
        await asyncio.sleep(1800)
        await member.remove_roles(role)

async def reactionrole(payload, guilds):
    for guild in guilds:
        target_message_id = #message_id as integer
        if payload.message_id == target_message_id:
            member = guild.get_member(payload.user_id)
            target_emoji_id = #emoji_id as integer
            if payload.emoji.id == target_emoji_id:
                role_id = #role id as integer
                role = guild.get_role(role_id)
                await member.add_roles(role)

def is_record_exists(user_id): #< - selects all user_ids from table
    cursor.execute(f'SELECT * FROM name WHERE user_id = {user_id}')
    result = cursor.fetchall()
    return result is not None

async def userdata(result, guilds):
    for guild in guilds:
        for member in guild.members:
            user_id = member.id
            role_id = #role id as integer
            role = guild.get_role(role_id)
            if role not in member.roles:
                if not result(user_id):
                    cursor.execute("SELECT user_id FROM name WHERE user_id = ?", (user_id,))
                    cursor.execute("INSERT INTO name (user_id) VALUES (?)", (user_id,))
                    conn.commit()
                    await member.add_roles(role)
                else:
                    await member.add_roles(role)
            else:
                continue
            if result(user_id):
                if user_id not in guild.members:
                    cursor.execute("DELETE FROM name WHERE user_id = ?", (user_id,))
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
                    await checklvl(interaction.author.id, interaction)
                    if ammo == 1:
                        await interaction.response.send_message(f'I have made a number {str(number)}. I won!')
                    else:
                        await interaction.response.send_message(f'I have made a numbers {str(", ".join(str(num) for num in sorted(botnums)))}. I won!')
                    cursor.execute("UPDATE levels SET user_xp = user_xp - ? WHERE user_id = ?", (30 * ammo, user_id,))
                    cursor.execute("SELECT user_xp FROM levels WHERE user_id = ?", (user_id, ))
                    user_xp = cursor.fetchone()
                    if user_xp < 0:
                        cursor.execute("UPDATE levels SET user_xp = ? WHERE user_id = ?", (0, user_id, ))
                    conn.commit()
                elif int(number) >= 7:
                    await interaction.response.send_message('Make a number from 1 to 6!')
                else:
                    await checklvl(interaction.author.id, interaction)
                    if ammo == 1:
                        await interaction.response.send_message(f'I have made number: {botnums[0]}. You won and earn 15xp!')
                    else:
                        await interaction.response.send_message(f'I have made numbers {str(", ".join(str(num) for num in sorted(botnums)))}. You won and earn 15xp!')
                    cursor.execute("UPDATE levels SET user_xp = user_xp + ? WHERE user_id = ?", (12 * ammo, user_id,))
                    conn.commit()
        else:
            await interaction.response.send_message('Makke a number from 1 to 6')
    else:
        await interaction.response.send_message('Enter a number!')

async def coin(interaction, flips):
    options = ['Eagle', 'Tails']
    if int(flips) != 1:
        await interaction.response.send_message(f"Results: {', '.join(random.choice(options) for i in range(int(flips)))}")
    else:
        await interaction.response.send_message(f"Result: {random.choice(options)}\n")