from keep_alive import keep_alive
import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


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
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFteWt6NmMza3BoYmlrcTdnanp5bWMwZ205ODFxdGN0NW1nb3A5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/L5f4Z5JoOKARG/giphy.gif"
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
@bot.command()
async def hug(ctx, member: discord.Member):
    gif_url = random.choice(hug_gifs)
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
