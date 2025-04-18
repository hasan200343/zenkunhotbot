from keep_alive import keep_alive
import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
last_hug_gif = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# ----------------------
# 🎴 GIF Lists
# ----------------------
hug_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PHZ7v9tfQu0o0/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GMFUrC8E8aWoo/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/sUIZWMnfd4Mb6/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/qTeLrzpDZBY2c/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/L5f4Z5JoOKARG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDFsY3Q2eGdpbTM5ejIydm9hd2N2OHZicWc0Yzg2MmVpZTE2cGxyNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZQN9jsRWp1M76/giphy.gif",
    "https://media.giphy.com/media/C4gbG94zAjyYE/giphy.gif?cid=ecf05e47ndnalkg2pzph7y15lydo52e1aed9lwrz2rdc3rbv&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDFsY3Q2eGdpbTM5ejIydm9hd2N2OHZicWc0Yzg2MmVpZTE2cGxyNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/LIqFOpO9Qh0uA/giphy.gif",
    "https://media.giphy.com/media/3o6ZsTopjMRVkJXAWI/giphy.gif?cid=ecf05e474m1rl4gkc0bf8mdjxk2q2l7j3a3nvakholetqwug&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDBrazhuamlxeDR3bmRmODJkOHA2eHJ5MG9zNGNvam9oaDd3bWw5diZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ttThLoTVJb1EQ/giphy.gif",
    "https://media.giphy.com/media/3og0ILx8f9adnoQRos/giphy.gif?cid=ecf05e47yhifg1xaa42rra1ukfyd40g7s44arl7zpd65znlg&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/u6Yn932Vu2J5YFzGhM/giphy.gif?cid=ecf05e47yhifg1xaa42rra1ukfyd40g7s44arl7zpd65znlg&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczJiNHUwaXltM3c5bW9vaHY5eHdxd2hkczk5MHh5dm03c25pZzc3ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/COGHvkvkhNSqk/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczJiNHUwaXltM3c5bW9vaHY5eHdxd2hkczk5MHh5dm03c25pZzc3ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/isT304mEdP1y8/giphy.gif",
    "https://c.tenor.com/bZzrhkxcs6cAAAAC/tenor.gif",
    "https://c.tenor.com/G_IvONY8EFgAAAAd/tenor.gif",
    ""

]

lovehug_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmcwcjg0NXExeGZib2dtcW8wbWYwaGw5NGR2bHFzemJ4ZTcwcm00ciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WynnqxhdFEPYY/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QFPoctlgZ5s0E/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/49mdjsMrH7oze/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/143v0Z4767T15e/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IRUb7GTCaPU8E/giphy.gif"
]

bonk_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODgwZGlhZ2hxd3F2cnhnemlvajVtdzBmcWxpM2NnNmltaWhjc3poZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FDq2YMke0IhObhgoQx/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3E1NHg3dmpkNzg2MHAxN3B5N3NsMncyb2xxOTFyMXEzeXc1a2V1YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/HmgnQQjEMbMz0oLpqn/giphy.gif",
    "https://media.giphy.com/media/4ibREl3R15F6AAPqKY/giphy.gif?cid=ecf05e47soeokc18potsul9b7dmeuwkj5b59n5c3j6c8m3jn&ep=v1_gifs_search&rid=giphy.gif&ct=g",
]

# ----------------------
# ✨ Titles & Descriptions
# ----------------------

hug_titles = [
    "A gentle hug! 🤗", "Warm vibes incoming 🧸", "Here comes a snuggle! 💙"
]
hug_descriptions = [
    "{sender} gives a warm hug to {receiver}! 🥰",
    "{sender} wraps {receiver} in a comforting hug. 💫",
    "Hug alert! {sender} really cares about {receiver} 💗"
    "A GOOD HUGGIE COMING IN FROM {sender} TO {receiver}"
]

lovehug_titles = [
    "Sending you lots of love 💖", "Overflowing love hug! 💘",
    "This one’s full of feelings 💞"
]
lovehug_descriptions = [
    "{sender} sends {receiver} the most loving hug ever! 💓",
    "{sender} melts into {receiver}'s arms with love. ❤️",
    "Cuteness overload! {sender} hugs {receiver} with all their heart 💑"
]

bonk_titles = ["BONK! 🔨", "Justice has been served 🪓", "Get rekt! 💥"]
bonk_descriptions = [
    "{sender} bonks {receiver}! To horny jail you go! 🚓",
    "That’s enough outta you, {receiver}! BONK! 🔨 – from {sender}",
    "{sender} shows no mercy. BONK time for {receiver} 😈"
]


# ----------------------
# 🧸 Hug Command
# ----------------------
# @bot.command()
# async def hug(ctx, member: discord.Member):
#     gif_url = random.shuffle(hug_gifs)
#     title = random.choice(hug_titles)
#     description = random.choice(hug_descriptions).format(
#         sender=ctx.author.mention, receiver=member.mention)

#     embed = discord.Embed(title=title,
#                           description=description,
#                           color=discord.Color.blue())
#     embed.set_image(url=gif_url)
#     await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    global last_hug_gif

    # Ensure we don’t repeat the last GIF
    if len(hug_gifs) == 1:
        gif_url = hug_gifs[0]
    else:
        gif_url = random.choice(hug_gifs)
        while gif_url == last_hug_gif:
            gif_url = random.choice(hug_gifs)
    last_hug_gif = gif_url

    title = random.choice(hug_titles)
    description = random.choice(hug_descriptions).format(
        sender=ctx.author.mention, receiver=member.mention)

    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Color.blue())
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

# ----------------------
# 💕 Love Hug Command
# ----------------------
@bot.command()
async def lovehug(ctx, member: discord.Member):
    gif_url = random.choice(lovehug_gifs)
    title = random.choice(lovehug_titles)
    description = random.choice(lovehug_descriptions).format(
        sender=ctx.author.mention, receiver=member.mention)

    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Color.magenta())
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)


@commands.has_permissions(administrator=True)
async def nuke(ctx):
    channel = ctx.channel
    new_channel = await channel.clone(reason="Channel nuked!")
    await channel.delete()
    await new_channel.send(f"💥 Boom! {ctx.author.mention} just nuked the channel!")

# ----------------------
# 🔨 Bonk Command
# ----------------------
@bot.command()
async def bonk(ctx, member: discord.Member):
    gif_url = random.choice(bonk_gifs)
    title = random.choice(bonk_titles)
    description = random.choice(bonk_descriptions).format(
        sender=ctx.author.mention, receiver=member.mention)

    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Color.red())
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)


keep_alive()
token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print(
        "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
    )
