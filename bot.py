import subprocess

import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import random
import os
import asyncio
import youtube_dl
import moviepy.editor as mp

# A space for any values that need to be held on to (during development):
# Something went wrong (dev is too lazy to determine what, just ask him for an answer)

token = open("token.txt", "r")

global loop
loop = False

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='%', intents=intents)

forbidden_words = [
    "rawr",
    "nuzzles",
    "nuzzle",
    "rubbies",
    "uwu",
    "owo",
    "cringe"
]

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    print("Bot is ready for operation!🎆")
    embed = discord.Embed(title="Bot has started up", color=discord.Color.green())
    channel = bot.get_channel(1129867086148141138)
    await channel.send(embed=embed)
    game = discord.Game("whack-a-mole with bugs in my code")
    await bot.change_presence(status=discord.Status.idle, activity=game)


# @bot.event
# async def on_message(message):
#    if message.content.lower() in forbidden_words:
#        await message.reply("cringe")


@bot.command()
async def foo(ctx, *, arg):
    if arg == "ping":
        await ctx.send("pong")
    else:
        await ctx.send(arg)


@bot.command()
async def randint(ctx, start: int, end: int):
    try:
        result = random.randrange(start, end)
        if result == 69 or result == 420:
            await ctx.send(str(result) + " (nice)")
        else:
            await ctx.send(result)
    except ValueError:
        await ctx.send("The values entered must be integers and different")
    except MissingRequiredArgument:
        await ctx.send("Please enter two integer values, representing the lower and upper limit respectively")
    except TooManyArguments:
        await ctx.send("Please enter two integer values, representing the lower and upper limit respectively")


@bot.command()
async def whoami(ctx):
    await ctx.send("You are " + ctx.author.name)


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    if amount == 0:
        await ctx.message.delete()


@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="List of commands", color=discord.Color.green(), description=str(bot.commands))
    await ctx.send(embed=embed)
    help_text = "```"
    for command in bot.commands:
        help_text += f"{command}\n"
    help_text += "```"
    await ctx.send(help_text)


@bot.command()
async def line(ctx):
    await ctx.send("e\ne")


@bot.command()
async def annoy(ctx, author: discord.Member, limit: int, *text):
    i = 0
    if limit < 0:
        await ctx.send("cringe")
        return
    while i < limit:
        textToSend = ''.join(text)
        await ctx.send(author.mention + " " + textToSend)
        await asyncio.sleep(0.5)
        i += 1


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
        # return "C:\\Users\\Dorno\\Desktop\\Coding projects\\discord_bot\\music\\" + filename


@bot.command()
async def play(ctx, url):
    if ctx.author.name == "potatocrusher6":
        await ctx.send("fuck you, you're just gonna download a bunch of porn on my pc")
        return
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        while True:
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename, pipe=False))
            await ctx.send('**Now playing:** {}'.format(filename))
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                 filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            duration = float(result.stdout) + 1
            await asyncio.sleep(duration)
            if not loop:
                break
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def loop(ctx):
    global loop
    loop = not loop
    await ctx.send("Loop mode: " + str(loop))


@bot.command()
async def stopmusic(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    await voice_channel.disconnect()


@bot.command()
async def stop(ctx):
    if ctx.author.name == "berserk007":
        embed = discord.Embed(title="Bot is shutting down", color=discord.Color.red())
        await ctx.send(embed=embed)
        await bot.close()
    else:
        await ctx.send("cringe")


@bot.command()
async def restart(ctx):
    if ctx.author.name == "berserk007":
        embed = discord.Embed(title="Bot is restarting", color=discord.Color.dark_gold())
        await ctx.send(embed=embed)
        os.system("python bot_starter.py")
        await bot.close()
    else:
        await ctx.send("cringe")


bot.run(token.read())
