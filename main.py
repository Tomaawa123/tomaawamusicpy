import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import music

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='t!', intents=intents)

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')

async def setup():
    await bot.add_cog(music.music(bot))

keep_alive()
bot.run(os.environ['TOKEN'])