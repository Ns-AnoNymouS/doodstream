import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.name import isdownloadable_link


@Client.on_message(filters.regex('.*http.*'))
async def remote_upload(c, m):
    upload_url = m.text
    status, name = await isdownloadable_link(upload_url)
    buttons = [[
        InlineKeyboardButton('Default', callback_data='default'),
        InlineKeyboardButton('Rename', callback_data='rename')
    ]]
    await m.reply_text(f'**File Name:** `{name}`', reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_callback_query(filters.regex('^default$'))
async def default(c, m):
    upload_url = m.message.reply_to_message.text
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/upload/url?key={api_key}&url={upload_url}"
    data = requests.get(url).json()
    while True:
        link = f"https://doodapi.com/api/urlupload/status?key={api_key}&file_code={data['result']['filecode']}"
        json_data = requests.get(link).json()
        if json_data['result']['status'] == pending:
            print(json_data)
        else:
            break
    print(data)
    await m.message.edit(json_data)
