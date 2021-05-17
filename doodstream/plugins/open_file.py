import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex('^file'))
async def open_file(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    cmd, file_code = m.data.split('+')
    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    data = requests.get(url).json()

    if data['status'] == 200:
        text = f"**📁 Title:** {data['result'][0]['title']}\n"
        text += f"**⏰ Duration:** {data['result'][0]['length']}\n"
        text += f"**📊 Size:** {data['result'][0]['size']}"
        text += f"**👁 Views:** {data['result'][0]['views']}"
        text += f"**📆 Uploaded on:** {data['result'][0]['uploaded']}"
        buttons = [[
            InlineKeyboardButton("Rename ✏", callback_data=f"rename+{data['result'][0]['filecode']}"),
            InlineKeyboardButton("Download Url", url="https://dood.so{data['result'][0]['protected_dl']}")
        ]]
           # InlineKeyboardButton()
        return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"

    elif data['status'] == 403:
        text = "Your TOKEN was expired. So please logout and login again"
 
    else:
        text = "File Not Found 🤪"

    await m.message.edit(text)
