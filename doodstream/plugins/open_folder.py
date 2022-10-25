import asyncio
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
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, requests.get, url)
    data = data.json()

    if data['status'] == 403:
        text = "Token Expired"
    elif data['status'] == 200:
        text = "Select your file\n\n"
        folders = data['result']['folders'][fld : fld + 11]
        buttons = []
        for folder in folders:
            buttons.append([InlineKeyboardButton(f"📁 {folder['name']}", callback_data=f"folder+{folder['fld_id']}+0+0")])
        if (len(folders) < 10) & (len(folders) != 0):
            fil = 10 - len(folders)
        if len(folders) < 10:
            val = fil - 10 if fil > 10 else 0
            #print(val, fil)
            files = data['result']['files'][val: fil + 1]
            for file in files:
                buttons.append([InlineKeyboardButton(f"🎥 {file['title']}", callback_data=f"fle+{folder_id}+{file['file_code']}+{fld}+{fil}")])
        button = []
        if fld != 0:
             button.append(InlineKeyboardButton('⬅️', callback_data=f'folder+{folder_id}+{fld - 10}+{fil - 10}'))
        if len(buttons) > 10:
            buttons.pop()
            button.append(InlineKeyboardButton('➡️', callback_data=f'folder+{folder_id}+{fld + 10}+{fil + 10}'))
        buttons.append(button)
        buttons.append([InlineKeyboardButton('Home 🏡', callback_data="nxt+0+0")])
        if len(buttons) != 2:
            return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            return await m.message.edit("You don't have anyfiles here", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        text = "Something Went wrong"
    await m.reply_text(text)
