Just a Bot with AI with many goofy bugs ahhh

This is a Discord bot that uses Google Generative AI to generate responses and interact with users. The bot can also play music from YouTube and handle various commands.

## Features

- Generate responses using Google Generative AI
- Play music from YouTube
- Handle various text commands
- Download and save images
- Fetch and display song lyrics

## Requirements

- Python 3.8 or higher
- `discord.py` 2.0.0
- `google-generativeai` 1.0.0
- `yt-dlp`
- `aiohttp`
- `beautifulsoup4`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your API keys:
    ```env
    DISCORD_API_KEY=your_discord_api_key
    GEMINI_API_KEY=your_gemini_api_key
    ```

## Usage

1. Run the bot:
    ```sh
    python bot.py
    ```

2. Invite the bot to your Discord server using the OAuth2 URL with the necessary permissions.

## Commands

- `fly <query>`: Generate a response using the Gemini model.
- `fly1 <message>`: Send a message to the bhot channel.
- `fly2 <message>`: Send a message to the general channel.
- `fly3 <message>`: Send a message to the console channel.
- `flychannel`: List all available channels and their IDs.
- `flyhelp`: Show the help message.
- `!woi`: Respond with 'sabarlah tolol'.
- `!nandi`: Respond with 'nandi jembut'.
- `!rehan`: Respond with 'rehan anjing'.
- `!paris`: Respond with 'korek semalem mana'.
- `bagos`: Respond with 'yoi dong'.
- `bhot`: Respond with 'ha ?'.
- `!name`: Respond with 'My name is Furina'.
- `!blur`: Respond with 'halo king'.
- `!claw`: Respond with 'halo king'.
- `!rangga`: Respond with 'aku nak makan pempek la'.
- `!carlos`: Respond with 'halo ganteng'.
- `!fp <query>`: Search and play a song from YouTube based on the query.
- `!fps`: Stop the current song.
- `!fpp`: Resume the current song.
- `!keluargaklo`: Disconnect the bot from the voice channel.
- `!simpankanle <url>`: Download and save an image from the provided URL.
- `!kasihnama <name>`: Associate a name with the last downloaded image.

## License

My guwe ketika mk

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [Google Generative AI](https://github.com/google/generative-ai-python)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
