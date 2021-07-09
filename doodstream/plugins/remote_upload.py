import time
import math
import asyncio
from ..tools.requests import req
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.name import isdownloadable_link
from ..tools.progress_bar import humanbytes, TimeFormatter


@Client.on_message(filters.regex('.*http.*') & filters.private & filters.incoming)
async def remote_upload(c, m):
    upload_url = m.text
    status, name = await isdownloadable_link(upload_url)
    buttons = [[
        InlineKeyboardButton('Default', callback_data='default+False'),
        InlineKeyboardButton('Rename', callback_data='default+True')
    ]]
    await m.reply_text(f'**File Name:** `{name}`', reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_callback_query(filters.regex('^default'))
async def default(c, m):
    await m.answer()
    cmd, sts = m.data.split('+')
    upload_url = m.message.reply_to_message.text
    api_key = await c.db.get_credential_status(m.from_user.id)

    if sts == 'False':
        url = f"https://doodapi.com/api/upload/url?key={api_key}&url={upload_url}"

    if sts == 'True':
        status, name = await isdownloadable_link(upload_url)
        new_title = await c.ask(
            chat_id=m.from_user.id,
            text=f"**FileName:** `{name}`\n\nSend me the New file Name",
            filters=filters.text
        )
        url = f"https://doodapi.com/api/upload/url?key={api_key}&url={upload_url.encode().decode()}&new_title={new_title.text}"
        await new_title.delete()
        await new_title.request.delete()


    data = await req(url)
    start = time.time()
    file_code = data['result']['filecode']
    if data['status'] == 400:
        return await m.message.edit('Your URL already exist in the queue 🙄')
    await m.message.edit('Adding to queue...\n\nThis might take some time plz wait')


    while True:
        link = f"https://doodapi.com/api/urlupload/status?key={api_key}&file_code={data['result']['filecode']}"
        json_data = await req(link)
        for file in json_data['result']:
            if file['file_code'] == file_code:
                if file['status'] == 'pending':
                    try:
                        await m.message.edit(f"Your task was added to queue. Uploading start soon 📤.")
                    except:
                        pass
                elif file['status'] == 'working':
                    total = file['bytes_total']
                    done = file['bytes_downloaded']
                    percentage = (int(done) / int(total)) * 100
                    progress = "[{0}{1}]".format(
                        ''.join(["█" for i in range(math.floor(percentage / 10))]),
                        ''.join(["░" for i in range(10 - math.floor(percentage / 10))]))

                    try:
                        await m.message.edit(f"__**Uploading:**__\n\n{progress}{round(percentage, 2)}%\n\n**Total Size:** {humanbytes(total)}\n**Done:** {humanbytes()}\n**Started on:** {file['created']}")
                    except:
                        pass
                elif file['status'] == 'error':
                    await m.message.edit(f"**Unable to Upload File**\n\n__This file may not be a supported remote link please trying again 😶.__")
                else:
                    print(file['status'])
                    break
        await asyncio.sleep(3)


    url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={file_code}"
    files_url = f"https://doodapi.com/api/file/list?key={api_key}"
    data_file = await req(files_url)
    files = data_file['result']['files'] 
    for file in files:
        if file['file_code'] == file_code:
            file_data = file
            break
    data = await req(url)

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
            InlineKeyboardButton("Watch Online 👀", url=f"https://dood.so{data['result'][0]['protected_embed']}")
        ]]
        return await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data['status'] == 451:
        text = "Your video was disabled due to DMCA"

    elif data['status'] == 403:
        text = "Your TOKEN was expired. So please logout and login again"
 
    else:
        text = "File Not Found 🤪"

    await m.message.edit(text)
