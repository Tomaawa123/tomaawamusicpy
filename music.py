import discord
from discord.ext import commands
import yt_dlp

FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command()
    async def play(self, ctx, *, search):
        if not ctx.author.voice: return await ctx.send("¡Únete a un canal!")
        channel = ctx.author.voice.channel
        if not ctx.voice_client: await channel.connect()
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            url = info['url']
        
        if ctx.guild.id not in self.queues: self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(url)
        if not ctx.voice_client.is_playing(): self.play_next(ctx)
        await ctx.send(f"Reproduciendo: {info['title']}")

    def play_next(self, ctx):
        if self.queues.get(ctx.guild.id):
            url = self.queues[ctx.guild.id].pop(0)
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()