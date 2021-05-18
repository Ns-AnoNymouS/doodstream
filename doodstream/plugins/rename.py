import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.progress_bar import humanbytes, TimeFormatter


@Client.on_callback_query(filters.regex('^rename'))
async def remame(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    try:
        cmd, file_code, fld, fil = m.data.split('+')
    except:
        cmd, file_code = m.data.split('+')

    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    data = requests.get(url).json()

    newname = await Client.ask(
        self=c,
        chat_id=m.from_user.id,
        text="**FileName:** {data['result'][0]['title']}\n\nSend me the New file Name",
        filters=filters.text
    )
    print(newname)
