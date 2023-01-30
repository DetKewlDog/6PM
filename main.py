import discord
import random
import os
import keep_alive
import asyncio
import re
import difflib
from datetime import datetime

ID_6AM = 368307072065863680
ID_BOT = 1017048782904492122
ID_RANDOM = 836379248595435580
ID_DOG = 516976811981144065
ID_CHEE = 535483016546615302

intents = discord.Intents(messages=True, guilds=True)

client = discord.Client(intents=intents)


def check_tuna(msg):
  count = 0
  for i in msg:
    if i in "t u r".split():
      count += 1
    if i == " ":
      count = 0
  return count >= 3


def check_named(msg):
  return '6am' in msg or '6pm' in msg or 'bot' in msg


def check_good_bot(msg):
  return 'good 6am' in msg or 'good 6pm' in msg or 'good bot' in msg


def check_bad_bot(msg):
  return 'bad 6am' in msg or 'bad 6pm' in msg or 'bad bot' in msg


def find_occurence(s, pos, ch):
  min_distance = len(s)
  found_position = -1
  for i in range(len(s)):
    if s[i] == ch:
      distance = abs(pos - i)
      if distance < min_distance:
        min_distance = distance
        found_position = i
  return found_position


def get_every_tuna():
  content = ''
  with open('db.txt', 'r') as f:
    content = f.read()
  msg = 'The following is a list of the world\'s most notorious sex offenders:\n'
  content = re.sub(r'[^\w]', ' ', content)
  words = content.replace('\n', '').split(' ')
  words = list(set([word.lower() for word in words]))

  temps = [
    'tuna', 'tturna', 'turna', 'turn', 'trun', 'ttun', 'ttuna', 'turner',
    'tturner', 'tun', 'tonno', 'tuntun', 'tuner', 'ttuner'
  ]
  temps += [t.upper() for t in temps]
  lst = []
  for temp in temps:
    lst += difflib.get_close_matches(temp, words)
  words = list(set(lst))
  msg += ', '.join(words)
  if len(msg) > 2000:
    msg = msg[:find_occurence(msg, 2000, ' ') - 1]
  return msg


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


correct_the = True


@client.event
async def on_message_edit(before, after):
  if random.randint(0, 100) < 3:
    await before.reply(
      'https://tenor.com/view/edited-tf2-meet-the-medic-gif-22002258')


@client.event
async def on_message(message):
  global correct_the
  message = await message.channel.fetch_message(message.id)

  if message.author.id == ID_BOT:
    return
  if message.author.id == ID_6AM:
    with open('db.txt', 'a') as f:
      f.write('\n' + message.content.replace('\n', '\\n'))

  if message.author.id == ID_CHEE:
    last_time = 0
    with open('cheetimer.txt', 'r') as f:
      last_time = datetime.fromtimestamp(int(f.read()))
    current_time = datetime.now()
    difference = current_time - last_time
    if (difference.total_seconds() / 3600 >= 8):
      await message.reply('<:holdinggun:1040138431759650816> <:holdinggun:1040138431759650816> <:holdinggun:1040138431759650816> WORK ON RED NIV <:holdinggun:1040138431759650816> <:holdinggun:1040138431759650816> <:holdinggun:1040138431759650816>')
    with open('cheetimer.txt', 'w') as f:
      f.write(str(int(current_time.timestamp())))

  if check_named(message.content.lower()):
    if check_good_bot(message.content.lower()):
      await message.add_reaction('❤')

    if check_bad_bot(message.content.lower()):
      await message.add_reaction('💔')

  if message.content == '!stopfight':
    correct_the = False
    await asyncio.sleep(10)
    correct_the = True

  if message.content == '!fight':
    await message.reply(
      'Use ``!stopfight`` to stop the fight, as this feature causes a lot of spam'
    )
    await message.channel.send(f'<@{ID_RANDOM}>')

  if message.content == '!tuna':
    await message.reply(get_every_tuna())

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

      no_punc = re.sub(r'[^\w\s]', '', resp).strip()
      if (check_tuna(resp.lower())
          and len(no_punc.split(' ')) <= 4) or resp.endswith(','):
        await message.channel.send(
          f"{random.choice([x for x in lst if not check_tuna(x.lower()) and not x.endswith(',')])}",
          allowed_mentions=mentions)

  if message.content == "!fetch" and message.author.id == ID_DOG:
    await message.channel.send('Getting messages 🥰')
    lst = message.channel.history(limit=15000)
    lst = [msg async for msg in lst if msg.author.id == ID_6AM]

    with open('db.txt', 'w') as f:
      for msg in lst:
        try:
          f.write(msg.content + '\n')
        except:
          continue
    txt = ''
    with open('db.txt', 'r') as f:
      txt = f.read()
      txt.replace('\n\n', '\n')
    with open('db.txt', 'w') as f:
      f.write(txt)


keep_alive.keep_alive()
try:
  client.run(os.getenv('TOKEN'))
except:
  os.system('kill 1')

good_words = """
  attractive
  sexy
  good
  pog
  cool
  nice
  legendary
  great
  neat
  best
  brilliant
  incredible 
  fantastic
  godly
  lovely
  pretty
  perfect
  neat
  smart
  super
  sweet
  wholesome
  wise
  swag
  poggers

  clever
  conscious
  cute
  funny
  fun
  friendly
  flattering
  glorious
  helpful
  inspiring
  intelligent
  kind
  marvellous
  pleasant
  polite
  perceptive
  patient
  praiseworthy
  rational
  self-aware
  sensational
  sensible
  sharp
  strong
  spectacular
  stunning
  superior
  supportive
  thoughtful
  trustworthy
  unparalleled
  valuable
  vigilant
  well-mannered
  wonderful
  captivating
  magnificent
  breathtaking
  splendid
  stellar
  epic
""".split()

neautral_words = """
  special
  drunk
  faulty
  confusing
""".split()

negative_words = """
  bad
  stupid
  mean
  dumb
  cringe
  weird
  rude
  lazy
  foolish
  cruel
  awful
  idiot

  basic
  bland
  bizare
  bloated
  blind
  bloody
  blunt
  boring
  brainless
  cancerous
  mentally-challenged
  cheap
  childish
  clueless
  cocky
  concerning
  convoluted
  corny
  corrupt
  cowardly
  costly
  crazy
  daft
  dangerous
  defective
  deformed
  dense
  dirty
  disgusting
  empty
  faulty
  idiotic
  moody
  nosy
  petty
  pitiful
  tacky
""".split()

evil_words = """
  coldhearted
  cruel
  controversial
  creepy
  evil
  racist
  toxic
""".split()