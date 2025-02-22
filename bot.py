import discord
import os
import google.generativeai as genai
import asyncio
import yt_dlp as youtube_dl
import aiohttp
from bs4 import BeautifulSoup
from discord import FFmpegPCMAudio
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

DISCORD_API_KEY = 'MMM'
GEMINI_API_KEY = 'MMM'
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'  # Replace with your actual Client ID
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'  # Replace with your actual Client Secret

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CHAT_MEMORY_FILE = 'chat_memory.txt'
MAX_FILE_SIZE_MB = 50

voice_clients = {}
current_song_info = {}
queue = []
image_prompts = {}  # Dictionary to store prompt-image associations
pending_prompts = {}  # Dictionary to store pending prompts

# Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

async def send_long_message(channel, message):
    if len(message) <= 2000:
        await channel.send(message)
    else:
        for i in range(0, len(message), 2000):
            await channel.send(message[i:i+2000])

def write_to_memory(content):
    if os.path.exists(CHAT_MEMORY_FILE):
        if os.path.getsize(CHAT_MEMORY_FILE) > MAX_FILE_SIZE_MB * 1024 * 1024:
            os.remove(CHAT_MEMORY_FILE)
    with open(CHAT_MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 1341038015186862201:
        response = get_gemini_response(message.content)
        await send_long_message(message.channel, response)
        write_to_memory(f'User: {message.content}\nBot: {response}')
        return

    if message.content.startswith('fly'):
        query = message.content[len('fly '):].strip()
        if not query:
            await message.channel.send('Please provide a query after the fly command.')
            return
        response = get_gemini_response(query)
        await send_long_message(message.channel, response)
        write_to_memory(f'User: {query}\nBot: {response}')
    
    if message.content.startswith('fly1'):
        channel_id = 1332111384523309156
        message_content = message.content[len('fly1 '):].strip()
        channel = client.get_channel(channel_id)
        if channel:
            await send_long_message(channel, message_content)
            await message.channel.send("Message sent to bhot.")
            write_to_memory(f'User: {message_content}\nBot: Message sent to bhot.')
        else:
            await message.channel.send("Invalid channel ID for bhot.")
    
    if message.content.startswith('fly2'):
        channel_id = 1332113600894079131
        message_content = message.content[len('fly2 '):].strip()
        channel = client.get_channel(channel_id)
        if channel:
            await send_long_message(channel, message_content)
            await message.channel.send("Message sent to general.")
            write_to_memory(f'User: {message_content}\nBot: Message sent to general.')
        else:
            await message.channel.send("Invalid channel ID for general.")
    
    if message.content.startswith('fly3'):
        channel_id = 1340942564379070535
        message_content = message.content[len('fly3 '):].strip()
        channel = client.get_channel(channel_id)
        if channel:
            await send_long_message(channel, message_content)
            await message.channel.send("Message sent to console.")
            write_to_memory(f'User: {message_content}\nBot: Message sent to console.')
        else:
            await message.channel.send("Invalid channel ID for console.")

    if message.content.startswith('flychannel'):
        await message.channel.send("List of channels:\n1. bhot (1332111384523309156)\n2. general (1332113600894079131)\n3. console (1340942564379070535)")

    if message.content.startswith('flyhelp'):
        await message.channel.send(
            "Here are the available commands:\n"
            "1. `fly <query>`: Generate a response using the Gemini model.\n"
            "2. `fly1 <message>`: Send a message to the bhot channel (1332111384523309156).\n"
            "3. `fly2 <message>`: Send a message to the general channel (1332113600894079131).\n"
            "4. `fly3 <message>`: Send a message to the console channel (1340942564379070535).\n"
            "5. `flychannel`: List all available channels and their IDs.\n"
            "6. `flyhelp`: Show this help message.\n"
            "7. `!woi`: Respond with 'sabarlah tolol'.\n"
            "8. `!nandi`: Respond with 'nandi jembut'.\n"
            "9. `!rehan`: Respond with 'rehan anjing'.\n"
            "10. `!paris`: Respond with 'korek semalem mana'.\n"
            "11. `bagos`: Respond with 'yoi dong'.\n"
            "12. `bhot`: Respond with 'ha ?'.\n"
            "13. `!name`: Respond with 'My name is Furina'.\n"
            "14. `!blur`: Respond with 'halo king'.\n"
            "15. `!claw`: Respond with 'halo king'.\n"
            "16. `!rangga`: Respond with 'aku nak makan pempek la'.\n"
            "17. `!carlos`: Respond with 'halo ganteng'.\n"
            "18. `!fp <query>`: Search and play a song from YouTube based on the query.\n"
            "19. `!fps`: Stop the current song.\n"
            "20. `!fpp`: Resume the current song.\n"
            "21. `!keluargaklo`: Disconnect the bot from the voice channel."
        )

    if message.content.startswith('!woi'):
        await message.channel.send('sabarlah tolol')
    if message.content.startswith('!nandi'):
        await message.channel.send('nandi jembut')
    if message.content.startswith('!rehan'):
        await message.channel.send('rehan anjing')
    if message.content.startswith('!paris'):
        await message.channel.send('korek semalem mana')
    if message.content.startswith('bagos'):
        await message.channel.send('yoi dong')
    if message.content.startswith('bhot'):
        await message.channel.send('ha ?')
    if message.content.startswith('!name'):
        await message.channel.send('My name is Furina')
    if message.content.startswith('!blur'):
        await message.channel.send('halo king')
    if message.content.startswith('!claw'):
        await message.channel.send('halo king')
    if message.content.startswith('!rangga'):
        await message.channel.send('aku nak makan pempek la')
    if message.content.startswith('!carlos'):
        await message.channel.send('halo ganteng')
    if message.content.endswith('le'):
        await message.channel.send(file=discord.File('C:/Users/Carlos/Desktop/UTY/le.png'))
    if message.content.startswith('gimana le'):
        await message.channel.send('hisapkan dulu le')

    if message.content.startswith('!simpankanle'):
        url = message.content[len('!simpankanle '):].strip()
        if not url:
            await message.channel.send('habis simpankanle masukkan url gambar le. ')
            return
        await download_image(url, 'C:/Users/Carlos/Desktop/UTY')
        await message.channel.send(f'udah tak savein le. mau dikasih nama apa le.')
        pending_prompts[message.author.id] = os.path.join('C:/Users/Carlos/Desktop/UTY', os.path.basename(url))

    if message.content.startswith('!kasihnama'):
        if message.author.id in pending_prompts:
            prompt_name = message.content[len('!kasihnama '):].strip()
            image_path = pending_prompts.pop(message.author.id)
            image_prompts[prompt_name] = image_path
            await message.channel.send(f'Image has been associated with the prompt "{prompt_name}".')
        else:
            await message.channel.send('No image is pending for naming.')

    if message.content in image_prompts:
        await message.channel.send(file=discord.File(image_prompts[message.content]))

    if message.content.startswith('!fp'):
        query = message.content[len('!fp '):].strip()
        if not query:
            await message.channel.send('abis !fp masukin judul lagu')
            return
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send('minimal masuk dulu ke voice')
            return
        voice_channel = message.author.voice.channel
        feedback_channel = client.get_channel(1332111384523309156)
        await feedback_channel.send("sabar cari dulu")
        queue.append(query)
        if not voice_channel.guild.id in voice_clients:
            await play_next_song(voice_channel, feedback_channel)

    if message.content.startswith('!fstop'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_playing():
                vc.pause()
                feedback_channel = client.get_channel(1332111384523309156)
                await feedback_channel.send("pause lagu")
            else:
                await message.channel.send("ga ada lagu muter")
        else:
            await message.channel.send("manggil siape ?")

    if message.content.startswith('!fpp'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_paused():
                vc.resume()
                feedback_channel = client.get_channel(1332111384523309156)
                await feedback_channel.send("Music resumed.")
            else:
                await message.channel.send("Music is not paused.")
        else:
            await message.channel.send("Bot is not connected to a voice channel.")

    if message.content.startswith('!keluargaklo'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            await vc.disconnect()
            del voice_clients[message.guild.id]
            await message.channel.send("cabut dulu")
        else:
            await message.channel.send("kaga kehubung gw jir")

    if message.content.startswith('!flanjutmas'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_paused():
                vc.stop()
                feedback_channel = client.get_channel(1332111384523309156)
                await feedback_channel.send("relog bentar")
                voice_channel = message.author.voice.channel
                vc = await voice_channel.connect()
                voice_clients[message.guild.id] = vc
                await feedback_channel.send("sabar lanjut dulu")
                await play_next_song(voice_channel, feedback_channel)
            else:
                await message.channel.send("musiknya kaga ke pause jir")
        else:
            if message.author.voice is None or message.author.voice.channel is None:
                await message.channel.send('masuk voice dulu baru lanjut')
                return
            voice_channel = message.author.voice.channel
            feedback_channel = client.get_channel(1332111384523309156)
            await feedback_channel.send("rikonek bentar")
            vc = await voice_channel.connect()
            voice_clients[message.guild.id] = vc
            await feedback_channel.send("nih lanjutannya")
            await play_next_song(voice_channel, feedback_channel)

async def play_next_song(voice_channel, feedback_channel):
    if not queue:
        await feedback_channel.send("dikarenakan ga ada queue")
        vc = voice_clients.pop(voice_channel.guild.id, None)
        if vc:
            await vc.disconnect()
        return
    
    query = queue.pop(0)
    await play_music(voice_channel, query, feedback_channel)

async def play_music(voice_channel, query, feedback_channel):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True,
        'cookies': 'SID=g.a000twhngFyAPJ_nQqg-ce-glrlKoTmHAjXYuSTuO-zktHMgU_-PQ7EELFh-3VzfaqaBLGbFSAACgYKAZgSARQSFQHGX2Mih5K5Dk_usSVlDmYjjRsRZxoVAUF8yKpxVmO1AKHZ7bG1Tw-851690076',  # Directly use the cookie value
    }
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -c:v mp4v -filter:a "volume=0.15"'
    }
    try:
        # Check if the query is a Spotify URL
        if "open.spotify.com" in query:
            if "playlist" in query:
                playlist_id = query.split("/")[-1].split("?")[0]
                playlist_tracks = sp.playlist_tracks(playlist_id)
                for item in playlist_tracks['items']:
                    track = item['track']
                    track_query = f"{track['name']} {track['artists'][0]['name']}"
                    queue.append(track_query)
                await feedback_channel.send(f"Added {len(playlist_tracks['items'])} tracks from the playlist to the queue.")
                if not voice_channel.guild.id in voice_clients:
                    await play_next_song(voice_channel, feedback_channel)
                return
            else:
                track_info = sp.track(query)
                query = f"{track_info['name']} {track_info['artists'][0]['name']}"

        # Search and download URL Audio
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url2 = info['url']
            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)
            current_song_info[voice_channel.guild.id] = {'url': url2, 'title': title}

        # Check if bot is already in voice channel
        if voice_channel.guild.id in voice_clients:
            vc = voice_clients[voice_channel.guild.id]
        else:
            vc = await voice_channel.connect(self_deaf=True)
            voice_clients[voice_channel.guild.id] = vc

        await feedback_channel.send(f"memuterkan lagu: {title}")

        # Play audio
        source = FFmpegPCMAudio(url2, **ffmpeg_options)
        vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(voice_channel, feedback_channel), client.loop))

        # Wait for the audio to finish playing
        while vc.is_playing():
            await asyncio.sleep(1)

        logging.info(f"ffmpeg process for {title} successfully terminated")

    except Exception as e:
        logging.error(f"error cok: {str(e)}")
        await feedback_channel.send(f"Error: {str(e)}")

async def fetch_and_send_lyrics(title, feedback_channel):
    try:
        search_url = f"https://genius.com/api/search/multi?per_page=1&q={title}"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                data = await response.json()
        song_path = data['response']['sections'][0]['hits'][0]['result']['path']
        lyrics_url = f"https://genius.com{song_path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(lyrics_url) as lyrics_page:
                lyrics_page_text = await lyrics_page.text()
        soup = BeautifulSoup(lyrics_page_text, 'html.parser')
        lyrics_div = soup.find('div', class_='lyrics') or soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-6')
        if lyrics_div:
            if isinstance(lyrics_div, list):
                lyrics = '\n'.join([div.get_text(separator='\n') for div in lyrics_div])
            else:
                lyrics = lyrics_div.get_text(separator='\n')
            await send_long_message(feedback_channel, f"Lyrics for {title}:\n{lyrics}")
        else:
            await feedback_channel.send(f"Could not find lyrics for {title}.")
    except Exception as e:
        logging.error(f"Error fetching lyrics: {str(e)}")
        await feedback_channel,send(f"Could not fetch lyrics: {str(e)}")

async def download_image(url, save_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    file_name = os.path.join(save_path, os.path.basename(url))
                    with open(file_name, 'wb') as f:
                        f.write(image_data)
                    logging.info(f"Image downloaded and saved to {file_name}")
                else:
                    logging.error(f"Failed to download image. Status code: {response.status}")
    except Exception as e:
        logging.error(f"Error downloading image: {str(e)}")

def get_gemini_response(query):
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(query)
        return response.text
    except Exception as e:
        logging.error(f"Error getting Gemini response: {str(e)}")
        return "Error getting response from Gemini."

client.run(DISCORD_API_KEY)
