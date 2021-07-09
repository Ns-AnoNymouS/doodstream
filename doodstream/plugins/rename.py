from ..tools.requests import req
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.progress_bar import humanbytes, TimeFormatter


@Client.on_callback_query(filters.regex('^rename'))
async def remame(c, m):
    await m.answer()
    api_key = await c.db.get_credential_status(m.from_user.id)
    fld = False
    try:
        cmd, file_code, fld, fil = m.data.split('+')
    except:
        cmd, file_code = m.data.split('+')

    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    data = await req(url)

    files_url = f"https://doodapi.com/api/file/list?key={api_key}"
    data_file = await req(files_url)
    files = data_file['result']['files'] 
    for file in files:
        if file['file_code'] == file_code:
            file_data = file
            break
   
    new_title = await Client.ask(
        self=c,
        chat_id=m.from_user.id,
        text=f"**FileName:** {file_data['title']}\n\nSend me the New file Name",
        filters=filters.text
    )
    rename_url = f"https://doodapi.com/api/file/rename?key={api_key}&file_code={file_code}&title={new_title.text}"
    sts = await req(rename_url)
    
    if sts['status'] != 200:
        return await c.send_message(m.from_user.id, f"Unable to rename the file\n**Reason:** {sts['msg']}")

    if data['status'] == 200:
        text = f"**📁 Title:** {new_title.text}\n\n"
        text += f"**⏰ Duration:** {TimeFormatter(int(data['result'][0]['length']) * 1000)}\n\n"
        text += f"**📊 Size:** {humanbytes(int(data['result'][0]['size']))}\n\n"
        text += f"**👁 Views:** {data['result'][0]['views']}\n\n"
        text += f"**📆 Uploaded on:** {data['result'][0]['uploaded']}"
        buttons = [[
            InlineKeyboardButton("Rename ✏", callback_data=f"rename+{data['result'][0]['filecode']}"),
            InlineKeyboardButton("Download 📥", url=f"{file_data['download_url']}"),
            ],[
            InlineKeyboardButton("Watch Online 👀", url=f"https://dood.so{data['result'][0]['protected_embed']}"),
        ]]
        if fld:
            buttons[1].append(InlineKeyboardButton("Back 🔙", callback_data=f"nxt+{fld}+{fil}"))
        return await c.send_message(m.from_user.id, text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"

    elif data['status'] == 403:
        text = "Your TOKEN was expired. So please logout and login again"
 
    else:
        text = "File Not Found 🤪"

    await c.send_message(m.from_user.id, text)
