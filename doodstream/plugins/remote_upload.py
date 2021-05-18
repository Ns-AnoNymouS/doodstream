import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.regex('.*http.*'))
async def remote_upload(c, m):
    upload_url = m.text
    url = f"https://doodapi.com/api/upload/url?key={your_api_key}&url={upload_url}"
