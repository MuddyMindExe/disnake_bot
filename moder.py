import disnake

group1 = () # <- banned words in g1
group2 = () # <- banned words in g2
group3 = () # <- banned words in g3

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    if any(word in message.content.lower() for word in niggagroup):
        await message.channel.send('Your message1')
    elif any(word in message.content.lower() for word in pidorgroup):
        await message.channel.send('Your message2')
    elif any(word in message.content.lower() for word in daungroup):
        await message.channel.send('Your message3')