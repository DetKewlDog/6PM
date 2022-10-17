import discord
import random
import os
import keep_alive
import asyncio
import re

ID_6AM = 368307072065863680
ID_BOT = 1017048782904492122
ID_RANDOM = 836379248595435580

intents = discord.Intents(messages=True, guilds=True)

client = discord.Client(intents=intents)


def check_tuna(msg):
    count = 0
    for i in msg:
        if i in "t u r n a".split():
            count += 1
        if i == " ":
            count = 0
    return count >= 3


def check_6am(msg):
    return '6am' in msg or '6pm' in msg


def check_good_bot(msg):
    return 'good 6am' in msg or 'good 6pm' in msg


def check_bad_bot(msg):
    return 'bad 6am' in msg or 'bad 6pm' in msg


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


correct_the = True


@client.event
async def on_message(message):
    global correct_the
    message = await message.channel.fetch_message(message.id)

    if message.author.id == ID_BOT:
        return

    if check_good_bot(message.content.lower()):
        await message.add_reaction('❤')

    if check_bad_bot(message.content.lower()):
        await message.add_reaction('💔')

    if message.content == '!stopfight':
        correct_the = False
        await asyncio.sleep(10)
        correct_the = True

    if message.content == '!fight':
        await message.reply('Use ``!stopfight`` to stop the fight, as this feature causes a lot of spam')
        await message.channel.send(f'<@{ID_RANDOM}>')

    chance = random.randrange(1, 350)
    if message.author.id == ID_6AM:
        chance = random.randrange(1, 85)

    override = False
    if client.user in message.mentions:
        override = True

    if (chance == 2 or override) and correct_the:
        with open('db.txt', 'r') as f:
            lst = f.readlines()
            resp = random.choice(lst)
            mentions = discord.AllowedMentions(users=False)
            await message.reply(resp, allowed_mentions=mentions)
          
            no_punc = re.sub(r'[^\w\s]','',resp).strip()
            if (check_tuna(resp.lower()) and len(no_punc.split(' ')) <= 4) or resp.endswith(','):
                await message.channel.send(
                    f"{random.choice([x for x in lst if not check_tuna(x.lower()) and not x.endswith(',')])}", allowed_mentions=mentions)
              
    # if "fetch" in message.content:
    #     await message.channel.send('Getting messages 🥰')
    #     lst = message.channel.history(limit=5000)
    #     lst = [msg async for msg in lst if msg.author.id == ID_6AM]
    #     with open('db.txt', 'w') as f:
    #         for msg in lst:
    #             try:
    #                 f.write(msg.content + '\n')
    #             except:
    #                 continue


keep_alive.keep_alive()
try:
  client.run(os.getenv('TOKEN'))
except:
  os.system('kill 1')
