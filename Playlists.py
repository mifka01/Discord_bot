from discord.ext import commands
from commands_options import options
from youtube_search import YoutubeSearch
from Music import Music
from outputs import songs_in_playlist_output
from YTDLSource import YTDLSource
import json
import random
import time


class Playlists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.initialize_playlists()

    def initialize_playlists(self):
        with open('playlists/playlists.json') as json_file:
            data = json.load(json_file)
            self.playlists = data

    @commands.command(name=options["plnew"]["name"],
                      description=options["plnew"]["description"],
                      aliases=options["plnew"]["aliases"])
    async def plnew(self, ctx, playlist):
        """Bot will create new playlist"""
        if playlist not in self.playlists:
            self.playlists[playlist] = []
            await ctx.send(f"Playlist: {playlist} byl vytvořen")
            with open("playlists/playlists.json", 'w') as f:
                json_object = json.dumps(
                    self.playlists, sort_keys=True, indent=4)
                f.write(json_object)
        else:
            await ctx.send(f"Playlist {playlist} již existuje")

    @commands.command(name=options["pldel"]["name"],
                      description=options["pldel"]["description"],
                      aliases=options["pldel"]["aliases"])
    async def pldel(self, ctx, playlist):
        """Bot will delete chosen playlist"""
        if playlist in self.playlists:
            del self.playlists[playlist]
            await ctx.send(f"{playlist} byl smazán")
        else:
            await ctx.send(f"Playlist: {playlist} neexistuje")
        with open("playlists/playlists.json", 'w') as f:
            json_object = json.dumps(self.playlists, sort_keys=True, indent=4)
            f.write(json_object)

    @commands.command(name=options["pladd"]["name"],
                      description=options["pladd"]["description"],
                      aliases=options["pladd"]["aliases"])
    async def pladd(self, ctx, playlist, *, song):
        """Bot will add song to chosen playlist"""
        song = YoutubeSearch(song, max_results=1).to_dict()
        song = {'name': song[0]['title'],
                'url': f'https://www.youtube.com{song[0]["link"]}'}

        if song in self.playlists[playlist]:
            await ctx.send(f'{song["name"]} už je v tomto playlistu')
        else:
            self.playlists[playlist].append(song)
            await ctx.send(f"{song['name']} byl přidán to playlistu: {playlist}")

        with open("playlists/playlists.json", 'w') as f:
            json_object = json.dumps(self.playlists, sort_keys=True, indent=4)
            f.write(json_object)

    @commands.command(name=options["plrm"]["name"],
                      description=options["plrm"]["description"],
                      aliases=options["plrm"]["aliases"])
    async def plrm(self, ctx, playlist, *, song):
        """Bot will remove song from chosen playlist"""
        song = YoutubeSearch(song, max_results=1).to_dict()
        song = {'name': song[0]['title'],
                'url': f'https://www.youtube.com{song[0]["link"]}'}
        if song in self.playlists[playlist]:
            self.playlists[playlist].remove(song)
            await ctx.send(f'{song["name"]} byl odstraněn z playlistu: {playlist}')
        else:
            await ctx.send(f'{song["name"]} není v playlistu: {playlist}')
        with open("playlists/playlists.json", 'w') as f:
            json_object = json.dumps(self.playlists, sort_keys=True, indent=4)
            f.write(json_object)

    @commands.command(name=options["plplay"]["name"],
                      description=options["plplay"]["description"],
                      aliases=options["plplay"]["aliases"])
    async def plplay(self, ctx, playlist):
        """Bot will start playing songs from chosen playlist"""
        Music = self.bot.get_cog("Music")
        first_song = random.choice(self.playlists[playlist])['url']
        urls = []
        for song in self.playlists[playlist]:
            urls.append(song["url"])
        await Music.play(song=first_song, playlist=True, ctx=ctx)
        Music.queue.extend(await YTDLSource.from_url(songs=urls))

        await ctx.send("Playlist byl nahrán")

    @commands.command(name=options["plsongs"]["name"],
                      description=options["plsongs"]["description"],
                      aliases=options["plsongs"]["aliases"])
    async def plsongs(self, ctx, playlist):
        """Bot will show all songs in playlist"""
        playlist = self.playlists[playlist]
        await songs_in_playlist_output(ctx, playlist)
