import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.name import isdownloadable_link
from ..tools.progress_bar import humanbytes, TimeFormatter


@Client.on_message(filters.regex('.*http.*'))
async def remote_upload(c, m):
    upload_url = m.text
    status, name = await isdownloadable_link(upload_url)
    buttons = [[
        InlineKeyboardButton('Default', callback_data='default'),
        InlineKeyboardButton('Rename', callback_data='rename')
    ]]
    await m.reply_text(f'**File Name:** `{name}`', reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_callback_query(filters.regex('^default$'))
async def default(c, m):
    await m.answer()
    upload_url = m.message.reply_to_message.text
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/upload/url?key={api_key}&url={upload_url}"
    data = requests.get(url).json()
    if data['status'] == 400:
        return await m.message.edit('Your URL already exist in the queue 🙄')
    await m.message.edit('Adding to queue...')

    link = f"https://doodapi.com/api/urlupload/status?key={api_key}&file_code={data['result']['filecode']}"
    json_data = requests.get(link).json()
    for file in json_data['result']:
        if file['file_code'] == data['result']['filecode']:
            while True:
                link = f"https://doodapi.com/api/urlupload/status?key={api_key}&file_code={data['result']['filecode']}"
                json_data = requests.get(link).json()
                try:
                    file = file
                    index = json_data['result'].index(file)
                    if json_data['result'][index]['status'] == 'pending':
                        try:
                            await m.message.edit(f"Your task was added to queue. Uploading start soon")
                        except:
                            pass
                    elif json_data['result'][index]['status'] == 'working':
                        try:
                            await m.message.edit(f"__**Uploading**__\n\n**Total Size:** {humanbytes(file['bytes_total'])}\n**Done:** {humanbytes(file['bytes_downloaded'])}\n**Started on:** {file['created']}")
                        except:
                            pass
                    else:
                        break
                    await asyncio.sleep(3)
                except Exception as e:
                    break

    try:
        if file['status'] == 'error':
            await m.message.edit('The link you provided is not valid or not in supporting Sites so please try with different link')
    except:
        file_code = data['result']['filecode']
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
