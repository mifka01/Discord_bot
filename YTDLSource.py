import youtube_dl
import discord
import asyncio
import time

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'songs/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'no-cache-dir': True
    
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def get_info(song, download=False):
     return ytdl.extract_info(song, download=download)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, song, filename, volume=0.5):
        super().__init__(source, volume)
        self.song = song
        self.song_data = {
                    'title': song.get('title'),
                    'filename': filename,
                    'url': song.get('url'),
                    'uploader': song.get('uploader'),
                    'uploader_url': song.get('uploader_url'),
                    'thumbnail': song.get('thumbnail'),
                    'viewcount': song.get('viewcount'),
                    'duration': song.get('duration')}

    def from_url(self, song, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        song = get_info(song=song, download=True)
        filename = ytdl.prepare_filename(song)
            
        return YTDLSource(discord.FFmpegPCMAudio(filename, **ffmpeg_options),song=song, filename=filename)

