import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex('^file'))
async def open_file(c, m):
    cmd, file_code = m.data.split('+')
    url = f"https://doodapi.com/api/file/info?key={your_api_key}&file_code={file_code}"
    await m.message.edit()
