import discord
import os
from discord.ext import tasks
from googleapiclient.discovery import build

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Configuración de canales
CHANNELS = [
    {"youtube_id": "UC-EIEjK-RcVSwCnYdEP1dMw", "youtube_name": "Alvu", "discord_channel_id": 906972008338821175},
]

last_videos = {ch['youtube_id']: None for ch in CHANNELS}

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Ver último video
def get_latest_video(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()
    if not response['items']:
        return None, None, None, None
    latest_video = response['items'][0]
    video_id = latest_video['id'].get('videoId')
    title = latest_video['snippet']['title']
    thumbnail_url = latest_video['snippet']['thumbnails']['high']['url']
    live_broadcast_content = latest_video['snippet'].get('liveBroadcastContent', 'none')
    return video_id, title, live_broadcast_content, thumbnail_url

# Revisar videos
@tasks.loop(minutes=300)
async def check_youtube():
    for ch in CHANNELS:
        vid_id, title, live_status, thumbnail = get_latest_video(ch["youtube_id"])
        if vid_id is None:
            continue

        if last_videos[ch["youtube_id"]] != vid_id:
            last_videos[ch["youtube_id"]] = vid_id
            channel_discord = client.get_channel(ch["discord_channel_id"])

            if not isinstance(channel_discord, discord.TextChannel):
                print(f"El canal {ch['discord_channel_id']} no es un TextChannel")
                continue

            video_url = f"https://youtu.be/{vid_id}"

# Mensaje
            if live_status != "live": 
                texto = f"{ch['youtube_name']} acaba de subir un nuevo video!"
            else: 
                texto = f"{ch['youtube_name']} está en directo!"
            
            embed = discord.Embed(
                title=f"[{title}]({video_url})",
                color=discord.Color.red() if live_status != "live" else discord.Color.blue()
            )
            embed.set_image(url=thumbnail)
            await channel_discord.send(content=texto, embed=embed)

# Comandos slash
@tree.command(name="hola", description="Saluda")
async def slash_hola(interaction: discord.Interaction):
    await interaction.response.send_message("¡Hola! Soy tu bot")

@tree.command(name="adios", description="Se despide")
async def slash_adios(interaction: discord.Interaction):
    await interaction.response.send_message("Vete a la mierda")

@tree.command(name="armonia", description="Foto Ciudadela de la Armonía")
async def ciudad_defensa(interaction: discord.Interaction):
    file = discord.File("./temporada/armonia.webp", filename="armonia.webp")
    await interaction.response.send_message(file=file)

# Evento ready
@client.event
async def on_ready():
    await tree.sync()
    check_youtube.start()
    print(f"Bot listo: {client.user}")

# Ejecutar bot
if not DISCORD_TOKEN:
    print("Error: DISCORD_BOT_TOKEN environment variable not set!")
    exit(1)

client.run(DISCORD_TOKEN)
