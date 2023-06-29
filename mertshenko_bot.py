import discord
from discord.ext import commands
import youtube_dl

intents = discord.Intents.default()

intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.command()
async def play(ctx, url):
    # Check if the bot is already connected to a voice channel
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        await ctx.send("I am already playing audio in a voice channel. Use the .stop command to stop the current audio.")
        return

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

bot.run('token')




