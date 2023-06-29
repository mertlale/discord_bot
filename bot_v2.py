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
async def play(ctx, url):
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
        # Add the URL to the queue
        song_queue.append(url)
        await ctx.send(f'Song added to the queue: {url}')
    else:
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
            url2 = info['formats'][0]['url']

        ctx.voice_client.play(discord.FFmpegPCMAudio(url2))

        await ctx.send(f'Playing: {url}')

        # Wait until the current song finishes playing
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)  # Use asyncio.sleep instead of discord.utils.sleep_until

        # Check if there are more songs in the queue
        if len(song_queue) > 0:
            next_url = song_queue.pop(0)  # Get the next URL from the queue
            await play(ctx, next_url)  # Play the next song recursively

bot.run('token')

