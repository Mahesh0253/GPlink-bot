from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')

bot = Client('gplink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


start_msg = """
Hi {}!

I'm GPlink bot. Just send me link and get short link!

Send me a link to short a link with random alias.

For custom alias, <code>[link] | [custom_alias]</code>, Send in this format\n
Ex: https://t.me/example | Example

"""

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(start_msg.format(message.chat.first_name))
    

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    if "|" in message.text: # custom alias - [link] | [alias]
        link_parts = message.text.split("|")
        link = link_parts[0]
        alias = link_parts[1:-1+1]
        alias = "".join(alias)
    else:
        link = message.matches[0].group(0)
        alias = ""
    short_link = await get_shortlink(link, alias)
    await message.reply(short_link, quote=True)


async def get_shortlink(link, alias):
    url = f'https://gplinks.in/api'
    params = {'api': API_KEY,
              'url': link,
              'alias': alias
              }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            print(data["status"])
            if data["status"] == "success":
                return f"<code>{data['shortenedUrl']}</code>\n\nHere is your Link:\n{data['shortenedUrl']}"
            else:
                return f"Error: {data['message']}"


bot.run()
