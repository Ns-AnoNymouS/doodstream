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

    reply_markup = None
    text = "--**Remote Upload:**--\n\n"
    text += f"**Total Slots:** {data['total_slots']}\n"
    text += f"**Used Slots:** {data['used_slots']}\n\n\n"
    if data['used_slots'] != 0:
        text += "--**Active Uploads:**--\n\n"
        for file in remote_list['result']:
            text += f"**🔗 Url:** {file['remote_url']}\n"
            text += f"**📊 Status:** {file['status']}\n\n\n"
        buttons = [[
            InlineKeyboardButton("", callback_data="")
            InlineKeyboardButton("", callback_data="")
            InlineKeyboardButton("", callback_data="")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
    await m.reply_text(text=text, reply_markup=reply_markup, quote=True)
