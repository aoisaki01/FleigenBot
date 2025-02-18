import subprocess
import sys

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    "discord.py",
    "google-generativeai",
    "yt-dlp",
    "aiohttp",
    "beautifulsoup4"
]

# Install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

import discord
import os
import google.generativeai as genai
import asyncio
import yt_dlp as youtube_dl
import aiohttp
from bs4 import BeautifulSoup
from discord import FFmpegPCMAudio

DISCORD_API_KEY = 'x'
GEMINI_API_KEY = 'x'

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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

    if message.channel.id == id channel:
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
        channel_id = id channel
        message_content = message.content[len('fly1 '):].strip()
        channel = client.get_channel(channel_id)
        if channel:
            await send_long_message(channel, message_content)
            await message.channel.send("Message sent to bhot.")
            write_to_memory(f'User: {message_content}\nBot: Message sent to bhot.')
        else:
            await message.channel.send("Invalid channel ID for bhot.")
    
    if message.content.startswith('fly2'):
        channel_id = id channel
        message_content = message.content[len('fly2 '):].strip()
        channel = client.get_channel(channel_id)
        if channel:
            await send_long_message(channel, message_content)
            await message.channel.send("Message sent to general.")
            write_to_memory(f'User: {message_content}\nBot: Message sent to general.')
        else:
            await message.channel.send("Invalid channel ID for general.")
    
    if message.content.startswith('fly3'):
        channel_id = id channel
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
    if message.content.startswith('le'):
        await message.channel.send(file=discord.File('C:/Users/Carlos/Desktop/UTY/le.png'))
    if message.content.startswith('gimana le'):
        await message.channel.send('hisapkan dulu le')

    if message.content.startswith('!simpankanle'):
        url = message.content[len('!simpankanle '):].strip()
        if not url:
            await message.channel.send('habis simpankanle masukkan url gambar le. ')
            return
        await download_image(url, 'ur path')
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
            await message.channel.send('Please provide a query after the !fp command.')
            return
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send('You need to be in a voice channel to play music.')
            return
        voice_channel = message.author.voice.channel
        feedback_channel = client.get_channel(id channel)
        await feedback_channel.send("Searching for the song...")
        queue.append(query)
        if not voice_channel.guild.id in voice_clients:
            await play_next_song(voice_channel, feedback_channel)

    if message.content.startswith('!fstop'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_playing():
                vc.pause()
                feedback_channel = client.get_channel(id channel)
                await feedback_channel.send("Music paused.")
            else:
                await message.channel.send("No music is playing.")
        else:
            await message.channel.send("Bot is not connected to a voice channel.")

    if message.content.startswith('!fpp'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_paused():
                vc.resume()
                feedback_channel = client.get_channel(id channel)
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
            await message.channel.send("Bot has disconnected from the voice channel.")
        else:
            await message.channel.send("Bot is not connected to a voice channel.")

    if message.content.startswith('!flanjutmas'):
        if message.guild.id in voice_clients:
            vc = voice_clients[message.guild.id]
            if vc.is_paused():
                vc.stop()
                feedback_channel = client.get_channel(id channel)
                await feedback_channel.send("Reconnecting to voice channel...")
                voice_channel = message.author.voice.channel
                vc = await voice_channel.connect()
                voice_clients[message.guild.id] = vc
                await feedback_channel.send("Resuming music from the beginning...")
                await play_next_song(voice_channel, feedback_channel)
            else:
                await message.channel.send("Music is not paused.")
        else:
            if message.author.voice is None or message.author.voice.channel is None:
                await message.channel.send('You need to be in a voice channel to resume music.')
                return
            voice_channel = message.author.voice.channel
            feedback_channel = client.get_channel(id channel)
            await feedback_channel.send("Reconnecting to voice channel...")
            vc = await voice_channel.connect()
            voice_clients[message.guild.id] = vc
            await feedback_channel.send("Resuming music from the beginning...")
            await play_next_song(voice_channel, feedback_channel)

async def play_next_song(voice_channel, feedback_channel):
    if not queue:
        await feedback_channel.send("Queue is empty. Adding default song to the queue.")
        queue.append("https://www.youtube.com/watch?v=J_CFBjAyPWE")
    
    query = queue.pop(0)
    await play_music(voice_channel, query, feedback_channel)

async def play_music(voice_channel, query, feedback_channel):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True,
    }
    try:
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

        await feedback_channel.send(f"🎵 Now playing: **{title}**")

        # Play audio
        source = FFmpegPCMAudio(url2)
        vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(voice_channel, feedback_channel), client.loop))

    except Exception as e:
        await feedback_channel.send(f"⚠️ Error: {str(e)}")

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
        await feedback_channel.send(f"Could not fetch lyrics: {str(e)}")

async def download_image(url, save_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    file_name = os.path.join(save_path, os.path.basename(url))
                    with open(file_name, 'wb') as f:
                        f.write(image_data)
                    print(f"Image downloaded and saved to {file_name}")
                else:
                    print(f"Failed to download image. Status code: {response.status}")
    except Exception as e:
        print(f"Error downloading image: {str(e)}")

def get_gemini_response(query):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(query)
    return response.text

client.run(DISCORD_API_KEY)
