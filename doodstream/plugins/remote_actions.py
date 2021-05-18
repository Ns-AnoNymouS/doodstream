import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('remote_actions))
async def actions(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/urlupload/slots?key={api_key}"
    list_uploads = f"https://doodapi.com/api/urlupload/list?key={api_key}"
    data = requests.get(url).json()
    remote_list = requests.get(list_uploads).json()
    print(data, remote_list)
    """buttons = [[
    ]]
    await m.reply_text()"""
