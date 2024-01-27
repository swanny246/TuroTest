import re, os, asyncio, random, string, time
from discord.ext import commands, tasks

token = os.environ['token']
spam_id = os.environ['spam_id']
timeout_secs = int(os.environ['timeout_secs'])

pokename = 874910942490677270
poketox = 875526899386953779
p2assistant = 854233015475109888
authorized_ids = [pokename, poketox, p2assistant]
client = commands.Bot(command_prefix='.')
intervals = [3.4, 3.6, 2.8, 3.0, 3.2]

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

@client.event
async def on_message(message):
    if message.author.id in authorized_ids:
        content = message.content

        if ("Rare Ping" in content or "Regional Ping" in content or "Collection Pings" in content or "Shiny Hunt Pings" in content) and "@" in content:
            try:
                await client.wait_for('message', timeout=timeout_secs, check=lambda m: m.author != client.user and 'Bots' not in [role.name for role in m.author.roles])
                print("Interrupted, not shiny locking!")
            except asyncio.TimeoutError:
              try:
                  await message.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                  await message.send(f'{ctx.channel.mention} is now locked.')
              except Exception as e:
                  print(f"Error locking channel: {e}")
                  await ctx.send("An error occurred while locking the channel.")
              await message.channel.set_permissions(message.guild.default_role, send_messages=False)
              await message.channel.send(f'<#{message.channel.id}> locked')

    await client.process_commands(message)

@client.command()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f'{ctx.channel.mention} is now locked.')
    print(f'Channel {ctx.channel.name} locked by {ctx.author.name}.')
    
@client.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f'{ctx.channel.mention} is now unlocked.')
    print(f'Channel {ctx.channel.name} locked by {ctx.author.name}.')
    
client.run(f"{token}")
