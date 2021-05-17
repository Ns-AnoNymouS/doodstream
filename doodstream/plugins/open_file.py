import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.progress_bar import humanbytes, TimeFormatter

@Client.on_callback_query(filters.regex('^file'))
async def open_file(c, m):
    await m.answer()
    api_key = await c.db.get_credential_status(m.from_user.id)
    cmd, file_code, fld, fil = m.data.split('+')
    print(fil)
    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    files_url = f"https://doodapi.com/api/file/list?key={api_key}"
    data_file = requests.get(files_url).json()
    files = data_file['result']['files'] #.find_one({'filecode':file_code})
    for file in files:
        if file['file_code'] == file_code:
            file_data = file
            break
    data = requests.get(url).json()

    if data['status'] == 200:
        text = f"**📁 Title:** {data['result'][0]['title']}\n\n"
        text += f"**⏰ Duration:** {TimeFormatter(int(data['result'][0]['length']) * 1000)}\n\n"
        text += f"**📊 Size:** {humanbytes(int(data['result'][0]['size']))}\n\n"
        text += f"**👁 Views:** {data['result'][0]['views']}\n\n"
        text += f"**📆 Uploaded on:** {data['result'][0]['uploaded']}"
        buttons = [[
            InlineKeyboardButton("Rename ✏", callback_data=f"rename+{data['result'][0]['filecode']}"),
            InlineKeyboardButton("Download 📥", url=f"{file_data['download_url']}"),
            ],[
            InlineKeyboardButton("Watch Online 👀", url=f"https://dood.so{data['result'][0]['protected_embed']}"),
            InlineKeyboardButton("Back 🔙", callback_data=f"nxt+{fld}+{fil - 10}")
        ]]
        return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"

    elif data['status'] == 403:
        text = "Your TOKEN was expired. So please logout and login again"
 
    else:
        text = "File Not Found 🤪"

    await m.message.edit(text)


@Client.on_callback_query(filters.regex('^fle'))
async def openfile(c, m):
    await m.answer()
    api_key = await c.db.get_credential_status(m.from_user.id)
    cmd, folder_id, file_code, fld, fil = m.data.split('+')
    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    files_url = f"https://doodapi.com/api/file/list?key={api_key}"
    data_file = requests.get(files_url).json()
    files = data_file['result']['files'] #.find_one({'filecode':file_code})
    for file in files:
        if file['file_code'] == file_code:
            file_data = file
            break
    data = requests.get(url).json()

    if data['status'] == 200:
        text = f"**📁 Title:** {data['result'][0]['title']}\n\n"
        text += f"**⏰ Duration:** {TimeFormatter(int(data['result'][0]['length']) * 1000)}\n\n"
        text += f"**📊 Size:** {humanbytes(int(data['result'][0]['size']))}\n\n"
        text += f"**👁 Views:** {data['result'][0]['views']}\n\n"
        text += f"**📆 Uploaded on:** {data['result'][0]['uploaded']}"
        buttons = [[
            InlineKeyboardButton("Rename ✏", callback_data=f"rename+{data['result'][0]['filecode']}"),
            InlineKeyboardButton("Download 📥", url=f"{file_data['download_url']}"),
            ],[
            InlineKeyboardButton("Watch Online 👀", url=f"https://dood.so{data['result'][0]['protected_embed']}"),
            InlineKeyboardButton("Back 🔙", callback_data=f"folder+{folder_id}+{fld}+{fil}")
        ]]
        return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"

    elif data['status'] == 403:
        text = "Your TOKEN was expired. So please logout and login again"
 
    else:
        text = "File Not Found 🤪"

    await m.message.edit(text)
