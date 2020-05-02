import youtube_dl
import discord
import asyncio

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
    'rm-cache-dir': True
    
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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
    @classmethod
    async def from_url(self, songs, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        result = []
        for i in songs:
            song = await loop.run_in_executor(None, lambda: ytdl.extract_info(i, download=True))
            song = ytdl.extract_info(i, download=True)
            filename = ytdl.prepare_filename(song)
            result.append(YTDLSource(discord.FFmpegPCMAudio(filename, **ffmpeg_options),song=song, filename=filename))
        return result