import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(917955802302677073)
        embed = discord.Embed(title="Test cog successfully loaded", color=discord.Color.dark_gold())
        await channel.send(embed=embed)
    
    @commands.command()
    async def embed(self, ctx, *, title):
        embed = discord.Embed(title=title, color=discord.Color.green())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Test(client))