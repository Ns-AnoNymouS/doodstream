import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('myfiles'))
async def myfiles(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}"
    data = requests.get(url).json()
    if data['status'] == 403:
        text = "Send me the correct token"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][:10]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}")])
        if len(folders) < 10:
            files = data['result']['files'][:10 - len(folders)]
            for file in files:
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"folder+{file['file_code']}")])
        if len(buttons) > 10:
            
    else:
        text = "Something Went wrong"
    await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex('nxt'))
async def nxt(c, m):
    await m.answer()
