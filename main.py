import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from python_aternos import Client

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASS = os.getenv("ATERNOS_PASS")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Aternos login
atclient = Client()
atclient.login(ATERNOS_USER, ATERNOS_PASS)

servers = atclient.account.list_servers()
server = servers[0]


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("👋 Bot is working!")


@bot.command()
async def info(ctx):
    await ctx.send(
        f"""
**Server Info**

**Name:** {server.name}
**Address:** {server.address}
**Software:** {server.software}
**Version:** {server.version}
"""
    )


@bot.command()
async def start(ctx):
    await ctx.send("@everyone 🟢 Someone is starting the Minecraft server!")
    server.start()
    await ctx.send("✅ Start command sent!")


@bot.command()
async def stop(ctx):
    await ctx.send("@everyone 🔴 Someone is stopping the Minecraft server!")
    server.stop()
    await ctx.send("✅ Stop command sent!")


bot.run(DISCORD_TOKEN)