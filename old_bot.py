import discord
from discord import *
from discord.ext import commands, tasks
import random
import os
badwords = [
    'fuck',
    'shit',
    'ur dumb',
    "ur mum",
    "ur mom",
    "Ur mom",
    "Ur mum",
    "PHILOU",
    "Philou",
    "philou"]

client = commands.Bot(command_prefix = "%")

@client.event
async def on_ready():
    print("Bot is ready for operation!🎆")
    channel = client.get_channel(917955802302677073)
    embed = discord.Embed(title="Bot has started up", color=discord.Color.dark_gold())
    await channel.send(embed=embed)
    game = Game("whack-a-mole with bugs in my code")
    await client.change_presence(status=discord.Status.idle, activity=game)

#Swear prevention
@client.event
async def on_message(message):
   for i in badwords:
      if i in message.content:
        if message.author.name != "Berserk Bot":
            await message.delete()
            await message.channel.send(f"{message.author.mention} Don't use that word please!")
            client.dispatch('profanity', message, i)
            return
   await client.process_commands(message)

#Discord invite prevention
@client.listen("on_message")
async def on_message(message):
    if "https://discord.gg/" in message.content and message.author.name != "Berserk007":
        await message.delete()
        await message.channel.send(f"{message.author.mention} Don't send any discord invites please!")

#Profanity function
@client.event
async def on_profanity(message, word):
    channel = client.get_channel(917955802302677073)
    embed = discord.Embed(title="Profanity Alert!", description=f"{message.author.name} just said ||{word}||", color=discord.Color.dark_red())
    await channel.send(embed=embed)

#Bad words list
@client.command()
async def addbadword(ctx, word):
    await ctx.send("'" + word + "'" + " added to bad words list (This word list is reset everytime I restart(for now))")
    badwords.append(word)

#Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")

#8ball command
@client.command(aliases=["8ball", "eightball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

#Say command
@client.command()
async def say(ctx, *, text):
    await ctx.send(text)

#Clear command
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    if amount == 0:
        await ctx.message.delete()

#Kick command
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
    except:
        await ctx.send(f"{member.name} was not found")
    channel = client.get_channel(917955802302677073)
    embed = discord.Embed(title="Member kicked!", description=f"{ctx.message.author.name} just kicked {member.mention} for \"{reason}\"", color=discord.Color.dark_red())
    await channel.send(embed=embed)

#Ban command
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
    except:
        await ctx.send(f"{member.name} was not found")
    channel = client.get_channel(917955802302677073)
    embed = discord.Embed(title="Member banned!", description=f"{ctx.message.author.name} just banned {member.mention} for \"{reason}\"", color=discord.Color.darker_grey())
    await channel.send(embed=embed)

#Unban command
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            channel = client.get_channel(917955802302677073)
            embed = discord.Embed(title="Member unbanned!", description=f"{ctx.message.author.name} just unbanned {member.mention}", color=discord.Color.dark_green())
            await channel.send(embed=embed)

#Load command
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

#Unload command
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

#Load loop
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#Restart command
@client.command()
async def restart(ctx):
    channel = client.get_channel(917955802302677073)
    embed = discord.Embed(title="Bot restarting", color=discord.Color.dark_gold())
    await channel.send(embed=embed)
    os.system("python bot_starter.py")
    exit()

#@tasks.loop(seconds=10)
#async def change_status()

client.run("ODg1Njg3NzYzNDE0OTY2MzM1.YTqrAg.gZEnNZSdndVCSsPvlBiTXyucyL8")
