## .play text works but .play URL doesn't


import discord
from discord.ext import commands
import youtube_dl
import asyncio

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

song_queue = []  # List to store the queued songs

@bot.command()
async def play(ctx, *, query):
    # Check if the user is in a voice channel
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel

    # Check if the bot is not connected to a voice channel
    if ctx.voice_client is None:
        voice_channel = await channel.connect()
        print(f"Bot joined voice channel: {voice_channel.channel.name}")
    else:
        # Move the bot to the user's voice channel if it's in a different channel
        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)

    if ctx.voice_client.is_playing():
        # Add the query to the queue
        song_queue.append(query)
        await ctx.send(f'Song added to the queue: {query}')
    else:
        await play_song(ctx, query)

async def play_song(ctx, query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch',  # Use YouTube search
        'noplaylist': True,  # Only download single video, not playlist
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info('ytsearch:' + query, download=False)
            if 'entries' in info:
                # Take the first entry if it's a playlist
                url = info['entries'][0]['formats'][0]['url']
                title = info['entries'][0]['title']
            else:
                url = info['formats'][0]['url']
                title = info['title']
        except youtube_dl.DownloadError as e:
            await ctx.send("An error occurred while trying to play the song.")
            print(f"Error: {str(e)}")
            return

    ctx.voice_client.play(discord.FFmpegPCMAudio(url))

    await ctx.send(f'Playing: {title}')

    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    if len(song_queue) > 0:
        next_query = song_queue.pop(0)
        await play_song(ctx, next_query)

@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Stop the current song
        await ctx.send("Skipping to the next song.")
        # Check if there are more songs in the queue
        if len(song_queue) > 0:
            next_query = song_queue.pop(0)  # Get the next query from the queue
            await play_song(ctx, next_query)  # Play the next song
    else:
        await ctx.send("No song is currently playing.")

bot.run('token')
