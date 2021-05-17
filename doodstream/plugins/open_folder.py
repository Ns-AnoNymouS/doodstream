import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex('^folder'))
async def folder(c, m):
    await m.answer()
    cmd, folder_id, fld, fil = m.data.split("+")
    fld = int(fld)
    fil = int(fil)
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}&fld_id={folder_id}"
    data = requests.get(url).json()
    if data['status'] == 403:
        text = "Token Expired"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][fld : fld + 11]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}")])
        if len(folders) < 10:
            if fil < 0:
                fil = 0
            files = data['result']['files'][fil: fil + 11]
            fil += 10
            for file in files:
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"file+{file['file_code']}+{fld}+{fil - 10}")])
        button = []
        if fld != 0:
             button.append(InlineKeyboardButton('⬅️', callback_data=f'nxt+{fld - 10}+{fil - 20}'))
        if len(buttons) > 10:
            buttons.pop()
            button.append(InlineKeyboardButton('➡️', callback_data=f'nxt+{fld + 10}+{fil}'))
        buttons.append(button)
        if len(buttons) != 0:
            return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            return await m.message.edit("Something went wrong 🤔")
    else:
        text = "Something Went wrong"
    await m.reply_text(text)
