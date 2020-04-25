from discord.ext import commands
from commands_options import options
from randomize_methods import random_insult, random_online_user
from outputs import covid_output, weather_output, gaytest_output 


class Informative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=options["covid"]["name"],
                      description=options["covid"]["description"],
                      aliases=options["covid"]["aliases"])
    async def covid(self, ctx):
        """Send info about Covid-19"""
        await ctx.send(embed=covid_output())

    @commands.command(name=options["filip"]["name"],
                      description=options["filip"]["description"],
                      aliases=options["filip"]["aliases"])
    async def filip(self, ctx):
        """Bot will insult Filip"""
        for user in ctx.guild.members:
            if str(user)[-5:] == "#1926":
                filip = user
        await ctx.send(filip.mention + ' je ' + random_insult())

    @commands.command(name=options["insult"]["name"],
                      description=options["insult"]["description"],
                      aliases=options["insult"]["aliases"])
    async def insult(self, ctx):
        """Bot will insult random online person"""
        await ctx.send(random_online_user(ctx) + ' je ' + random_insult())

    @commands.command(name=options["weather"]["name"],
                      description=options["weather"]["description"],
                      aliases=options["weather"]["aliases"])
    async def weather(self, ctx, *, city):
        """Send info about weather in choosen destination"""
        await ctx.send(embed=weather_output(city))

    @commands.command(name=options["gaytest"]["name"],
                      description=options["gaytest"]["description"],
                      aliases=options["gaytest"]["aliases"])
    async def gaytest(self, ctx):
        """Bot will test if you're gay"""
        await ctx.send(embed=gaytest_output(ctx))
