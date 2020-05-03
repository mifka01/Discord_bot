from discord.ext import commands
from commands_options import options
from youtube_search import YoutubeSearch
from Music import Music
from outputs import songs_in_playlist_output
from YTDLSource import YTDLSource, get_info
import json
import random
import time
import youtube_dl

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
        link = YoutubeSearch(song, max_results=1).to_dict()
        link = f'https://www.youtube.com{link[0]["link"]}'
        song = get_info(song=link)
        song_data = {
                    'title': song.get('title'),
                    'url': link,
                    'duration': song.get('duration')}

        if song in self.playlists[playlist]:
            await ctx.send(f'{song_data["title"]} už je v tomto playlistu')
        else:
            self.playlists[playlist].append(song_data)
            await ctx.send(f"{song_data['title']} byl přidán to playlistu: {playlist}")

        with open("playlists/playlists.json", 'w') as f:
            json_object = json.dumps(self.playlists, sort_keys=True, indent=4)
            f.write(json_object)

    @commands.command(name=options["plrm"]["name"],
                      description=options["plrm"]["description"],
                      aliases=options["plrm"]["aliases"])
    async def plrm(self, ctx, playlist, *, song):
        """Bot will remove song from chosen playlist"""
        link = YoutubeSearch(song, max_results=1).to_dict()
        link = f'https://www.youtube.com{link[0]["link"]}'
        song = get_info(song=link)
        song_data = {
                    'title': song.get('title'),
                    'url': link,
                    'duration': song.get('duration')}
        if song_data in self.playlists[playlist]:
            self.playlists[playlist].remove(song_data)
            await ctx.send(f'{song_data["title"]} byl odstraněn z playlistu: {playlist}')
        else:
            await ctx.send(f'{song_data["title"]} není v playlistu: {playlist}')
        with open("playlists/playlists.json", 'w') as f:
            json_object = json.dumps(self.playlists, sort_keys=True, indent=4)
            f.write(json_object)

    @commands.command(name=options["plplay"]["name"],
                      description=options["plplay"]["description"],
                      aliases=options["plplay"]["aliases"])
    async def plplay(self, ctx, playlist):
        """Bot will start playing songs from chosen playlist"""
        Music = self.bot.get_cog("Music")
        shuffled_playlist = random.sample(self.playlists[playlist], len(self.playlists[playlist]))
        for song in shuffled_playlist[:5]:
            await Music.play(song=song['url'], playlist=True, ctx=ctx)
        for song in shuffled_playlist[5:]:
            Music.queue.append(song)
        await ctx.send("Playlist byl nahrán")

    @commands.command(name=options["plsongs"]["name"],
                      description=options["plsongs"]["description"],
                      aliases=options["plsongs"]["aliases"])
    async def plsongs(self, ctx, playlist):
        """Bot will show all songs in playlist"""
        playlist = self.playlists[playlist]
        await songs_in_playlist_output(ctx, playlist)
