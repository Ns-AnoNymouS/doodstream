import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.regex('.*http.*'))
async def remote_upload(c, m):
    upload_url = m.text
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/upload/url?key={api_key}&url={upload_url}"
    data = requests.post(url)
    print(data.text)
