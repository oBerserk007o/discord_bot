import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import random
import fileinput

# A space for any values that need to be held on to (during development):
# Something went wrong (dev is too lazy to determine what, just ask him for an answer)

token = open("token.txt", "r")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='%', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


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
        if result == 69:
            await ctx.send(str(result) + " (nice)")
        else:
            await ctx.send(result)
    except ValueError:
        await ctx.send("The values entered must be integers and different")
    except MissingRequiredArgument:
        await ctx.send("Please enter two integer value, representing the lower and upper limit respectively")
    except TooManyArguments:
        await ctx.send("Please enter two integer value, representing the lower and upper limit respectively")


bot.run(token.read())
