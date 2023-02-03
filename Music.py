import discord
import youtube_dl
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

client = discord.Client()

# A list to store the songs in the playlist
playlist = []

# A flag to track if the bot is playing music
playing = False

# A flag to track if the bot is paused
paused = False

# A flag to track if the user has added a song to the playlist
song_added = False

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global playlist
    global playing
    global paused
    global song_added

    if message.content.startswith('!play'):
        url = message.content[6:]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            author = info['uploader']
            print(f'Adding music to playlist: {title} by {author}')
            playlist.append(info)
            song_added = True

    if song_added:
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        song_added = False

    if message.content == '!playlist':
        for i, song in enumerate(playlist):
            print(f'{i + 1}. {song["title"]} by {song["uploader"]}')

    if message.content == '!start':
        if not playlist:
            print('Playlist is empty!')
            return

        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()

        playing = True
        while playlist and playing:
            if paused:
                await asyncio.sleep(1)
                continue
            song = playlist.pop(0)
            print(f'Playing music: {song["title"]} by {song["uploader"]}')
            vc.play(discord.FFmpegPCMAudio(song['url']))
            while vc.is_playing():
                await asyncio.sleep(1)

    if message.content == '!skip':
        if not playing:
            print('No music is playing!')
            return

        vc.stop()

    if message.content == '!pause':
        if not playing:
            print('No music is playing!')
            return

        paused = True
        print('Music is paused.')

    if message.content == '!resume':
        if not playing:
            print('No music is playing!')
            return

        paused = False
        print

client.run('MTA3MTExMjI1NDM2OTU4MzE1NQ.GbvYaK.GNH1zh4EyvYLwxQoV9BO8G64Ia26NvOAi1fo_E')