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
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}+0+0")])
        if len(folders) < 10:
            files = data['result']['files'][:11 - len(folders)]
            for file in files:
                fil = 10 - len(folders) if len(folders) >=10 else 0
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"file+{file['file_code']}+0+{fil}")])
        if len(buttons) > 10:
            buttons.pop()
            buttons.append([InlineKeyboardButton('➡️', callback_data=f'nxt+10+{10 - len(folders)}')])
        if len(buttons) != 0:
            return await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)
        else:
            return await m.reply_text("You didn't have any files yet", quote=True)
    else:
        text = "Something Went wrong"
    await m.reply_text(text)


@Client.on_callback_query(filters.regex('^nxt'))
async def nxt(c, m):
    await m.answer()
    cmd, fld, fil = m.data.split("+")
    fld = int(fld)
    fil = int(fil)
    #print(fld, fil)
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}"
    data = requests.get(url).json()
    if data['status'] == 403:
        text = "Token Expired"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][fld : fld + 11]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}+0+0")])
        if len(folders) < 10:
            val = fil if fil >=0 else 0
            fil = fil + 11 if len(folders) == 0 else 11 - len(folders)
            print(val, fil)
            files = data['result']['files'][val: fil]
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
        if len(buttons) != 1:
            #print(fil)
            return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            return await m.message.edit("Something went wrong 🤔")
    else:
        text = "Something Went wrong"
    await m.reply_text(text)
