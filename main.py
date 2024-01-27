import re, os, asyncio, random, string#, keep_alive
from discord.ext import commands, tasks

version = 'v1.0'

user_token = os.environ['user_token']
spam_id = os.environ['spam_id']

client = commands.Bot(command_prefix= '^' )
intervals = [3.0, 3.2, 3.4, 2.6, 2.8]

@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    await channel.send(''.join(random.sample(['1','2','3','4','5','6','7','8','9','0'],7)*5))

@spam.before_loop
async def before_spam():
    await client.wait_until_ready()

spam.start()
@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')

print(f'santos el halper spambot {version}')
#keep_alive.keep_alive()
client.run(f"{user_token}")