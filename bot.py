from discord.ext import commands
from Informative import Informative
from Music import Music
from News import News 
from Playlists import Playlists
import os
from bot_token import TOKEN


bot = commands.Bot(command_prefix=commands.when_mentioned_or("??"))
@bot.event 
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


#@bot.event
#async def on_command_error(ctx, error):
    #await ctx.send(f"{ctx.message.author.mention} Unknown command -> use ?help")


bot.add_cog(Informative(bot))
bot.add_cog(Music(bot))
bot.add_cog(News(bot))  
bot.add_cog(Playlists(bot))
bot.run(TOKEN)