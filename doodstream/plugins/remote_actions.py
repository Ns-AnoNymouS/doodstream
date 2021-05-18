import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('remote_actions'))
async def actions(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/urlupload/slots?key={api_key}"
    list_uploads = f"https://doodapi.com/api/urlupload/list?key={api_key}"
    data = requests.get(url).json()
    remote_list = requests.get(list_uploads).json()
    print(data, remote_list)
    text = "--**Remote Upload:**--\n\n"
    text += f"**Total Slots:** {data['total_slots']}\n"
    text += f"**Used Slots:** {data['used_slots']}\n\n\n"
    if data['used_slots'] != 0:
        text += "--**Active Uploads:**--\n\n"
        for file in remote_list['result']:
            text += f"**Total Slots:** {data['total_slots']}\n"
            text += f"**Used Slots:** {data['used_slots']}\n\n\n"
    """buttons = [[
    ]]
    await m.reply_text()"""
