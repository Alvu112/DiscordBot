import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def hola(ctx):
    await ctx.send("¡Hola! Soy tu bot")

bot.run("BOTTOKEN")
