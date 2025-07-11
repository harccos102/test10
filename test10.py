import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer

TOKEN = 'MTM4Mzc3OTE3NzM0MTEyODcxNA.G-wStK.RuNyvDVT4Jq6HlpllBDgOejWCRk356RMv-2QUE'
VOICE_CHANNEL_ID = 1391699395363340380  # Írd ide a saját hangcsatorna ID-t
MC_SERVER_IP = "play.woodcraft.hu:25565"  # Minecraft szerver címe

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
last_name = None  # Ezzel figyeljük, hogy változott-e a név

@bot.event
async def on_ready():
    print(f"✅ Bejelentkezve mint: {bot.user}")
    update_channel_name.start()

@tasks.loop(minutes=5)
async def update_channel_name():
    global last_name
    try:
        server = JavaServer.lookup(MC_SERVER_IP)
        status = await server.async_status()
        player_count = status.players.online
        new_name = f"wood player ({player_count})"
    except Exception as e:
        print(f"❌ Hiba történt a szerver lekérésénél: {e}")
        new_name = "🌐 Szerver nem elérhető"

    if new_name != last_name:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                await channel.edit(name=new_name)
                print(f"✅ Csatorna frissítve: {new_name}")
                last_name = new_name
            except Exception as e:
                print(f"❌ Nem sikerült módosítani a csatornát: {e}")
        else:
            print("❌ A megadott csatorna nem hangcsatorna vagy nem található.")
    else:
        print("ℹ️ Nincs változás, nem frissítjük a nevet.")

bot.run(TOKEN)