from discord.ext import commands
from commands_options import options
from outputs import news_output
from get_data_methods import get_sport_data, get_news_data


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=options["news"]["name"],
                      description=options["news"]["description"],
                      aliases=options["news"]["aliases"])
    async def news(self, ctx, typex):
        """Send news of choosen type"""
        if typex in options['news']['sport_type']:
            output = news_output(get_sport_data())
        elif typex in options['news']['world_type']:
            output = news_output(get_news_data("https://www.novinky.cz/zahranicni"))
        elif typex in options['news']['home_type']:
            output = news_output(get_news_data("https://www.novinky.cz/domaci"))
        else:
            await ctx.send("Zadán nesprávný typ novinek")
            return

        for embed in output:
            await ctx.send(embed=embed)
           
