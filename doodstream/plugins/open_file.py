import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex('^file'))
async def open_file(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    cmd, file_code = m.data.split('+')
    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    data = requests.get(url).json()
    if data['status'] == 200:
        text = f"Title: {data['result']['title']}"
        text += f"Duration: {data['result']['length']}"
        text += f"Size: {data['result']['size']}"
    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"
    elif data['status'] == 451:
        text = "Your TOKEN was expired. Send me new one"
    else:
        text = "File Not Found 🤪"
    await m.message.edit(text)
