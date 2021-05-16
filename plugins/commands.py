import requests
from pyrogram import Client, filters


@Client_on_message(filters.command('token'))
async def login(c, m):
    if len(m.command) == 2:
        cmd, api_key = m.text.split(' ')
        url = f"https://doodapi.com/api/account/info?key={api_key}"
        userdetails = requests.get(url).json()
        await m.reply_text(userdetails)
