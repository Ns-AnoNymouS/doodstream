import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('myfiles'))
async def myfiles(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}"
    data = requests.get(url).json()
    if data['status'] == 403:
        text = "Token Expired"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][:11]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}")])
        if len(folders) < 10:
            files = data['result']['files'][:11 - len(folders)]
            for file in files:
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"folder+{file['file_code']}")])
        if len(buttons) > 10:
            buttons.pop()
            buttons.append([InlineKeyboardButton('Next ➡️', callback_data='nxt+11+{11 - len(folders)}')])
        return await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        text = "Something Went wrong"
    await m.reply_text(text)


@Client.on_callback_query(filters.regex('^nxt'))
async def nxt(c, m):
    cmd, fld, fil = m.data.split("+")
    num = int(num)
    await m.answer()
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}"
    data = requests.get(url).json()
    if data['status'] == 403:
        text = "Token Expired"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][10 * num:(10 * num) + 10]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}")])
        if len(folders) < 10:
            if len(folders) != 0:
                files = data['result']['files'][:11 - len(folders)]
            else:
            for file in files:
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"folder+{file['file_code']}")])
        if len(buttons) > 10:
            buttons.pop()
            buttons.append([InlineKeyboardButton('Next ➡️', callback_data='nxt+1')])
        return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        text = "Something Went wrong"
    await m.reply_text(text)
