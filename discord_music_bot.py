import discord
from discord.ext import commands
import youtube_dl
import asyncio
import validators

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

song_queue = []  # List to store the queued songs
paused = False  # Flag to indicate if playback is paused
current_song = None  # Currently playing song

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

    if ctx.voice_client.is_playing() or paused:
        # Add the query to the queue
        song_queue.append(query)
        await ctx.send(f'Song added to the queue: {query}')
    else:
        if validators.url(query):
            await play_song(ctx, query)
        else:
            await search_and_play(ctx, query)

async def search_and_play(ctx, query):
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
            info = ydl.extract_info(query, download=False)
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

    ffmpeg_options = {
        'options': '-vn',
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
    }

    ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))

    current_song = {
        'url': url,
        'title': title
    }

    await ctx.send(f'Playing: {title}')

async def play_song(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']

    ffmpeg_options = {
        'options': '-vn',
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
    }

    ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))

    current_song = {
        'url': url,
        'title': title
    }

    await ctx.send(f'Playing: {title}')

async def play_next(ctx):
    global current_song
    if len(song_queue) > 0:
        next_query = song_queue.pop(0)
        if validators.url(next_query):
            await play_song(ctx, next_query)
        else:
            await search_and_play(ctx, next_query)
    else:
        current_song = None

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Stop the current song
        await ctx.send("Skipping to the next song.")
    else:
        await ctx.send("No song is currently playing.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client is not None:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Stop the current song

        await ctx.voice_client.disconnect()  # Disconnect the bot from the voice channel

        song_queue.clear()  # Clear the song queue
        current_song = None  # Reset the currently playing song

        await ctx.send("Playback stopped and queue cleared.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def pause(ctx):
    global paused
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        paused = True
        await ctx.send("Playback paused.")
    else:
        await ctx.send("No song is currently playing.")

@bot.command()
async def resume(ctx):
    global paused
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        paused = False
        await ctx.send("Playback resumed.")
    else:
        await ctx.send("Playback is not paused.")

@bot.command()
async def queue(ctx):
    if len(song_queue) > 0:
        queue_list = '\n'.join(song_queue)
        await ctx.send(f'Queue:\n{queue_list}')
    else:
        await ctx.send("The song queue is empty.")

bot.run('your_bot_token')
