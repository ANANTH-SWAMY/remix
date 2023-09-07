import discord
from discord.ext import commands
import asyncio
# import youtube_dl as yt
import yt_dlp as yt
import os

intents = discord.Intents.default()
intents.message_content=True

TOKEN = '' #Put your discord bot token here
client = commands.Bot(command_prefix='<',intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="<help"))
    print("ready")

@client.command(name="join",help="Joins voice channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    try:
        await channel.connect()
    except discord.errors.ClientException:
        await ctx.send("Already connected to voice channel")

@client.command(name="leave",help="Leaves the connected voice channel")
async def leave(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    vc=discord.utils.get(ctx.guild.voice_channels,name="Radio")
    if voice.is_connected():
        try: 
            await voice.disconnect()
        except AttributeError:
            await ctx.send("Not in voice channel")

@client.command(name="play",help="Plays the youtube video")
async def play(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    vc=discord.utils.get(ctx.guild.voice_channels,name="Radio")
    YDL_OPTIONS={"format":"bestaudio/best"}
    
    test=ctx.message.content.lstrip("<play")
    st=test.split()
    url=""
    for i in st:
        url+=i+"_"

    if os.path.isfile("song.webm"):
        os.remove("song.webm")

    with yt.YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.download([f"ytsearch:{url}"])
    for f in os.listdir("./"):
        if f.endswith(".webm"):
            os.rename(f,"song.webm")
    try:
        voice.play(discord.FFmpegPCMAudio("song.webm"))
        print(info_1)
    except AttributeError:
        await ctx.send("Connect Remix to a voice channel")

@client.command(name="pause",help="Pauses current song")
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    try:
        if voice.is_playing:
            voice.pause()
            await ctx.send("Music paused")
        else:
            await ctx.send("Not playing any song to pause")
    except AttributeError:
        await ctx.send("Connect Remix to a voice channel")

@client.command(name="resume",help="Resumes the song")
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
            await ctx.send("Resuming music...")
        elif voice.is_playing():
            await ctx.send("Already playing")
        else:
            await ctx.send("Not playing any song to resume")
    except AttributeError:
        await ctx.send("Connect Remix to a voice channel")

@client.command(name="stop",help="Stops playing")
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    try:
        voice.stop()
        await ctx.send("Music stopped")
    except AttributeError:
        await ctx.send("Connect Remix to a voice channel")

client.run(TOKEN)
