import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

load_dotenv()  # betölti a .env fájlt

TOKEN = os.getenv("MTM4Mzc3OTE3NzM0MTEyODcxNA.GjHSiO.fNg-ATAG-EiHHP1YFv5g7xqSqKpesWdrgm44Xk")
GUILD_ID = 1368975077470765177
VOICE_CHANNEL_ID = 1391699395363340380
MINECRAFT_IP = "play.woodcraft.hu"
MINECRAFT_PORT = 25565

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"A bot bejelentkezett mint: {bot.user}")
    update_voice_channel.start()

@tasks.loop(seconds=60)
async def update_voice_channel():
    try:
        server = JavaServer.lookup(f"{MINECRAFT_IP}:{MINECRAFT_PORT}")
        status = server.status()
        player_count = status.players.online

        guild = bot.get_guild(GUILD_ID)
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            await channel.edit(name=f"🎮 Játékosok: {player_count}")
            print(f"[Frissítve] 🎮 Játékosok: {player_count}")
    except Exception as e:
        print(f"Hiba történt: {e}")

bot.run(TOKEN)