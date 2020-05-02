from discord.ext import commands
from commands_options import options
from youtube_search import YoutubeSearch
from YTDLSource import YTDLSource
from outputs import playing_output, queue_output, songs_in_queue_output, removed_song
import os
import shutil



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.queue = []
        self.current_song = None
        self.ctx = None

    def check_queue(self, error):
        try:
            song = self.queue[0].song_data["filename"]
            del self.queue[0]
            os.remove(song)
        except (PermissionError, IndexError, FileNotFoundError):
            pass
        
        if len(self.queue) > 0:
            self.current_song = self.queue[0].song_data
            self.voice_client.play(self.queue[0], after=self.check_queue)


    @commands.command(name=options["play"]["name"],
                      description=options["play"]["description"],
                      aliases=options["play"]["aliases"])
    async def play(self, ctx, *, song, playlist=False, first=False):
        """Bot will start playing music"""
        await self.join(ctx)
        if song[0:8] != "https://":
            song = YoutubeSearch(song, max_results=1).to_dict()
            song = f'https://www.youtube.com{song[0]["link"]}'

        source = await YTDLSource.from_url([song], loop=self.bot.loop, stream=False)
        if first:
            self.queue.insert(1, source[0])
        else:
            self.queue.extend(source)
        self.ctx = ctx
        if not self.voice_client.is_playing():
            self.current_song = self.queue[0].song_data
            self.voice_client.play(self.queue[0], after=self.check_queue)
            if not playlist:
                await ctx.send(embed=playing_output(ctx, self.queue[0].song_data))
            else:
                pass
        else:
            if not playlist:
                await ctx.send(embed=queue_output(ctx, self.queue[0].song_data))
            else:
                pass
            

                

    @commands.command(name=options["join"]["name"],
                      description=options["join"]["description"],
                      aliases=options["join"]["aliases"])
    async def join(self, ctx):
        """Bot will join authors voice channel"""
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(voice_channel)
        self.voice_client = await voice_channel.connect()

    @commands.command(name=options["leave"]["name"],
                      description=options["leave"]["description"],
                      aliases=options["leave"]["aliases"])
    async def leave(self, ctx):
        """Bot will leave authors voice channel"""
        guild = ctx.guild.voice_client
        await guild.disconnect()

    @commands.command(name=options["stop"]["name"],
                      description=options["stop"]["description"],
                      aliases=options["stop"]["aliases"]) 
    async def stop(self, ctx):
        """Bot will stop playing music"""
        self.queue = []
        self.voice_client.stop()
        await self.leave(ctx)
        shutil.rmtree('songs')

    @commands.command(name=options["pause"]["name"],
                      description=options["pause"]["description"],
                      aliases=options["pause"]["aliases"])
    async def pause(self, ctx):
        """Bot will pause currently playing song"""
        self.voice_client.pause()

    @commands.command(name=options["resume"]["name"],
                      description=options["resume"]["description"],
                      aliases=options["resume"]["aliases"])
    async def resume(self, ctx):
        """Bot will resume currently paused song"""
        self.voice_client.resume()
    
    @commands.command(name=options["skip"]["name"],
                      description=options["skip"]["description"],
                      aliases=options["skip"]["aliases"])
    async def skip(self, ctx):
        """Bot will skip currently playing song"""
        self.voice_client.stop()

    @commands.command(name=options["queue"]["name"],
                      description=options["queue"]["description"],
                      aliases=options["queue"]["aliases"])
    async def song_queue(self, ctx):
        """Bot will show songs in queue"""
        await songs_in_queue_output(ctx, self.queue)

    @commands.command(name=options["song"]["name"],
                      description=options["song"]["description"],
                      aliases=options["song"]["aliases"])
    async def song(self, ctx):
        """Bot will show currently playing"""
        await ctx.send(embed=playing_output(ctx, self.current_song))
    
    @commands.command(name=options["remove"]["name"],
                      description=options["remove"]["description"],
                      aliases=options["remove"]["aliases"])
    async def remove(self, ctx, num: int):
        """Bot will remove chosen song from queue"""
        if num <= len(self.queue) -1 :
            song = self.queue[num]
            if num == 0 :
                await self.skip(ctx)
            else:
                del self.queue[num]
                os.remove(song.song_data["filename"])
            await ctx.send(embed=removed_song(ctx, song.song_data))
        else:
            pass
    
    @commands.command(name=options["playfirst"]["name"],
                      description=options["playfirst"]["description"],
                      aliases=options["playfirst"]["aliases"])
    async def playfirst(self, ctx, *, song):
        """Bot will add song to first position in queue"""
        await self.play(ctx=ctx, song=song, first=True)
    
    
    