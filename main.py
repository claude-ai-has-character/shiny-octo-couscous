import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from python_aternos import Client

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASS = os.getenv("ATERNOS_PASS")

# Discord setup
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

# Login to Aternos
atclient = Client()
atclient.login(ATERNOS_USER, ATERNOS_PASS)

servers = atclient.account.list_servers()
server = servers[0]


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Sync failed: {e}")

    print(f"✅ Logged in as {bot.user}")


# /hello
@bot.tree.command(name="hello", description="Check if the bot is online")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("👋 Bot is working!")


# /info
@bot.tree.command(name="info", description="Show Minecraft server info")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"""## 🎮 Minecraft Server

**Name:** {server.name}
**Address:** {server.address}
**Software:** {server.software}
**Version:** {server.version}
"""
    )


# /start
@bot.tree.command(name="start", description="Start the Minecraft server")
async def start(interaction: discord.Interaction):

    await interaction.response.send_message(
        "@everyone 🟢 Someone is starting the Minecraft server..."
    )

    try:
        server.start()
        await interaction.followup.send("✅ Start command sent!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")


# /stop
@bot.tree.command(name="stop", description="Stop the Minecraft server")
async def stop(interaction: discord.Interaction):

    await interaction.response.send_message(
        "@everyone 🔴 Someone is stopping the Minecraft server..."
    )

    try:
        server.stop()
        await interaction.followup.send("✅ Stop command sent!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")


bot.run(DISCORD_TOKEN)
