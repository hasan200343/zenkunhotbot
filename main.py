from asyncio import tasks
import datetime
from keep_alive import keep_alive
import discord
from discord.ext import commands
import random
import os
import asyncio
import json

class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(birthday_check(self))  # Pass the bot instance to the task

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = MyBot(command_prefix="!", intents=intents)
last_hug_gif = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ----------------------
# 🚫 Abusive Words List
# ----------------------

abusive_words = ["fuck", "shit", "motherfucker", "moron", "bozo", "biggot", "bigot",
    "imbecile", "bitch", "bastard", "asshole", "dumbass", "douche", "retard",
    "cunt", "slut", "whore", "prick", "nigga", "nigger", "faggot", "twat", "jackass",
    "dipshit", "dick", "cock", "pussy", "wanker", "tosser", "arsehole", "suck my",
    "suck it", "niga", "cum", "retard", "niggi", "pussy"]

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
    "https://c.tenor.com/G_IvONY8EFgAAAAd/tenor.gif"

]

lovehug_gifs = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmcwcjg0NXExeGZib2dtcW8wbWYwaGw5NGR2bHFzemJ4ZTcwcm00ciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WynnqxhdFEPYY/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QFPoctlgZ5s0E/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/49mdjsMrH7oze/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/143v0Z4767T15e/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHpvbG1tb2M5cXo0eG1nMWo2ZjJrOGhpbTVkZ2l2bmMzb3pqNnhvNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IRUb7GTCaPU8E/giphy.gif"
]

homiehug_gifs = [
    "https://c.tenor.com/DDp3OiYHJxEAAAAC/tenor.gif",
    "https://c.tenor.com/WpbZhwwj6zAAAAAC/tenor.gif",
    "https://c.tenor.com/gtbvMmW3pYsAAAAC/tenor.gif",
    "https://c.tenor.com/2c7DJsPqwk8AAAAd/tenor.gif",
    "https://c.tenor.com/UBq2T-exSbkAAAAC/tenor.gif",
    "https://c.tenor.com/g4ZmqWSZqSIAAAAC/tenor.gif",
    "https://c.tenor.com/OaQvZ5AIPGUAAAAd/tenor.gif"

]

bonk_gifs = [
    "https://c.tenor.com/bkXZ1GhsTTsAAAAC/tenor.gif",
    "https://c.tenor.com/D6Ln3UPAdKcAAAAd/tenor.gif",
    "https://c.tenor.com/mXwNLMSQRN8AAAAC/tenor.gif",
    "https://c.tenor.com/BgSitYC0vboAAAAC/tenor.gif",
    # "https://c.tenor.com/1Kwjdke1U0UAAAAd/tenor.gif", (THIS IS FOR KILL COMMAND)
    "https://c.tenor.com/qeazzHmCPrYAAAAC/tenor.gif",
    "https://media.tenor.com/ddw1dL-KF8UAAAAi/newspaper-anime.gif",
    "https://c.tenor.com/FJsjk_9b_XgAAAAC/tenor.gif",
    "https://c.tenor.com/Gg4wSkuH6b4AAAAC/tenor.gif",
    "https://c.tenor.com/VHGbBswo_rQAAAAC/tenor.gif"
]

kill_gifs = [
    "https://c.tenor.com/1Kwjdke1U0UAAAAd/tenor.gif",
    "https://c.tenor.com/NbBCakbfZnkAAAAC/tenor.gif",
    "https://media.tenor.com/HqHu-BqxJUEAAAAi/anime-xd.gif",
    "https://c.tenor.com/G4SGjQE8wCEAAAAC/tenor.gif",
    "https://c.tenor.com/Ze50E1rW44UAAAAd/tenor.gif",
    "https://c.tenor.com/GjgIRbO-xOsAAAAC/tenor.gif"
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
homiehug_titles = [
    "Two brothers having a nice homie time 🤝",
    "ZA BESTOO FURENZO!! ✊"
]

homiehug_descriptions = [
    "{sender} sends {receiver} hug respectively **NO HOMO** 💪",
    "{sender} gives {receiver} a good cheeky hug 🫂",
    "A good manly hug has been bestowed upon {receiver} by {sender} ✊",
    "{sender} has crushed {receiver} ribs while giving a BIG AAH HUG!! ☠️"
]

bonk_titles = ["BONK! 🔨", "Justice has been served 🪓", "Get rekt! 💥"]

bonk_descriptions = [
    "{sender} bonks {receiver}! To horny jail you go! 🚓",
    "That’s enough outta you, {receiver}! BONK! 🔨 – from {sender}",
    "{sender} shows no mercy. BONK time for {receiver} 😈"
]

kill_titles = [
    "GWEHEH SHINDAGO !! 😵",
    "Time to dig a grave 🪦",
    "Oh no we got one less homo sapiens from us.....🫂"
]

kill_descriptions = [
    "{sender} wanna dice {receiver} into the abyss, LET EM BE BURRIED ☠️",
    "{sender} just deleted {receiver} from the existence. 💢",
    "{sender} did it extra brutal to {receiver} now MUWAHAHAHAAHAHA ! ! !"
]


# ----------------------
# 🫂 Hug Command
# ----------------------
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

# ----------------------
# 💣 Nuke Command
# ----------------------
import asyncio

@bot.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 120, commands.BucketType.channel)  # 2-minute cooldown
async def nuke(ctx):
    countdown_msg = await ctx.send("☢️ Initiating nuke sequence...")

    for i in range(4, 0, -1):
        await asyncio.sleep(1)
        await countdown_msg.edit(content=f"💣 Nuke in {i}...")
    
    await asyncio.sleep(1)
    await countdown_msg.edit(content="🔥 Detonating...")

    # Purge messages (excluding the last one or two to avoid deleting the countdown)
    await ctx.channel.purge(limit=None)

    # Nuke effect embed
    embed = discord.Embed(
        title="💣 Channel Nuked!",
        description=f"# {ctx.author.mention} JUST BOOOOMMMMMMED!!!! ALL TEXTS HAVE BEEN GONE TO THE ABYSS!! ||only those with the moded discord can see the chats :cat_hehe||",
        color=discord.Color.red()
    )
    embed.set_image(url="https://media.giphy.com/media/oe33xf3B50fsc/giphy.gif")  # Optional explosion GIF
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

# ----------------------
# 🤝 Homie Hug Command
# ----------------------
@bot.command()
async def homiehug(ctx, member: discord.Member):
    gif_url = random.choice(homiehug_gifs)
    title = random.choice(homiehug_titles)
    description = random.choice(homiehug_descriptions).format(
        sender=ctx.author.mention, receiver=member.mention)

    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Color.dark_grey())
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

# ----------------------
# 💢 Auto Filter and Auto Moderation
# ----------------------

# Channel ID for moderation logs
MOD_LOG_CHANNEL_ID = 1360343036558835872  # not used anymore for logs
TIMEOUT_DURATION = 5  # seconds

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()
    if any(word in content_lower for word in abusive_words):
        if message.guild:
            try:
                await message.delete()

                await message.author.timeout(
                    duration=TIMEOUT_DURATION,
                    reason="Abusive language detected."
                )

                # Send dramatic message in the same channel
                await message.channel.send(
                    "🚨 OH MY! This person just used abusive language...\n"
                    "TIME TO THROW THEM OUT OF THE BALCONY!!! 🪟🪂"
                )

            except Exception as e:
                print(f"Error timing out user: {e}")

    await bot.process_commands(message)

# ----------------------
# SUS Command
# ----------------------

@bot.command(name="sus")
async def sus(ctx):
    if not ctx.message.mentions:
        await ctx.send("Please mention at least one person to check their susness 👀")
        return

    responses = []
    for member in ctx.message.mentions:
        sus_percentage = random.randint(0, 100)
        emoji = "😇" if sus_percentage < 25 else "🤨" if sus_percentage < 75 else "🚨"
        responses.append(f"{emoji} {member.mention} is {sus_percentage}% sus!")

    await ctx.send("\n".join(responses))


# ----------------------
# 🎉 Birthday Handling
# ----------------------

# Load birthdays from JSON
def load_birthdays():
    if not os.path.exists("birthdays.json"):
        return {}
    with open("birthdays.json", "r") as f:
        return json.load(f)

# Save birthdays to JSON
def save_birthdays(birthdays):
    with open("birthdays.json", "w") as f:
        json.dump(birthdays, f)

# Scheduled birthday check
async def birthday_check(bot):
    await bot.wait_until_ready()
    channel_id = 123456789012345678  # Replace with your channel ID

    while not bot.is_closed():
        today = datetime.datetime.now().strftime('%m-%d')
        with open('birthdays.json', 'r') as f:
            birthdays = json.load(f)

        channel = bot.get_channel(channel_id)
        if not channel:
            print("Channel not found. Check the ID.")
            return

        for user_id, bday in birthdays.items():
            if bday == today:
                user = await bot.fetch_user(int(user_id))
                if user:
                    await channel.send(f"🎉 @everyone Please wish a very happy birthday to {user.mention}! 🎂")
                    print(f"Sent birthday message for {user.name} in {channel.name}")

        await asyncio.sleep(10)  # Wait one day before next check


bot.loop.create_task(birthday_check())



# ----------------------
# 🚫 Error Handling
# ----------------------
keep_alive()
token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print(
        "Error: Discord bot token not found. Please set the 'TOKEN' environment variable."
    )
