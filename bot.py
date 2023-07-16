import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import random
import os

# A space for any values that need to be held on to (during development):
# Something went wrong (dev is too lazy to determine what, just ask him for an answer)

token = open("token.txt", "r")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='%', intents=intents)


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
        if result == 69 or 420:
            await ctx.send(str(result) + " (nice)")
        else:
            await ctx.send(result)
    except ValueError:
        await ctx.send("The values entered must be integers and different")
    except MissingRequiredArgument:
        await ctx.send("Please enter two integer value, representing the lower and upper limit respectively")
    except TooManyArguments:
        await ctx.send("Please enter two integer value, representing the lower and upper limit respectively")


@bot.command()
async def whoami(ctx):
    await ctx.send("You are " + ctx.author.name)


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    if amount == 0:
        await ctx.message.delete()


@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="List of commands", color=discord.Color.green(), description=str(bot.commands))
    await ctx.send(embed=embed)


@bot.command()
async def stop(ctx):
    if ctx.author.name == "berserk007":
        embed = discord.Embed(title="Bot is shutting down", color=discord.Color.red())
        await ctx.send(embed=embed)
        await bot.close()


@bot.command()
async def restart(ctx):
    if ctx.author.name == "berserk007":
        embed = discord.Embed(title="Bot is restarting", color=discord.Color.dark_gold())
        await ctx.send(embed=embed)
        os.system("python bot_starter.py")
        await bot.close()


bot.run(token.read())
