import os
import re
import time
import aiohttp
from ..tools.requests import req
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.progress_bar import progress_bar, humanbytes, TimeFormatter
from ..config import Config


@Client.on_message((filters.document|filters.video) & filters.private & filters.incoming)
async def tg_upload(c, m):
    msg = await m.reply_text("𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀....🕵️‍♂️", quote=True)

    start_time = time.time()
    id = f"{time.time()}/{m.from_user.id}"
    Config.ACTIVE_DOWNLOADS.append(id)

    download_location = f"./download/{m.from_user.id}{time.time()}/"
    if not os.path.isdir(download_location):
        os.makedirs(download_location)

    try:
        await msg.edit("𝖳𝗋𝗒𝗂𝗇𝗀 𝖳𝗈 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽...📥")
    except:
        pass

    file_location = await m.download(
        file_name=download_location,
        progress=progress_bar,
        progress_args=("Downloading:", start_time, c, msg, id)
    )

    if file_location is None:
        try:
            if not id in Config.ACTIVE_DOWNLOADS:
                await msg.edit("𝖯𝗋𝗈𝖼𝖾𝗌𝗌 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽 𝖲𝗎𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 ✅")
            else:
                await msg.edit("**𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖥𝖺𝗂𝗅𝖾𝖽!!**\n\n𝖲𝗈𝗆𝖾 𝗋𝖾𝖼𝖾𝗇𝗍𝗅𝗒 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝖿𝗂𝗅𝖾𝗌 𝖺𝗋𝖾 𝗎𝗇𝖺𝖻𝗅𝖾 𝗍𝗈 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗌𝗈 𝗉𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝖿𝗍𝖾𝗋 𝗌𝗈𝗆𝖾 𝗍𝗂𝗆𝖾.", parse_mode="markdown")
            return
        except:
            pass

    await msg.edit("Downloaded Sucessfully\n\nTrying to upload to doodstream.com")
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/upload/server?key={api_key}" 
    data = await req(url)
    print(data)
    if data['status'] == 200:
        url = f"{data['result']}?{api_key}"
    elif data['status'] == 403:
        return await msg.edit(text="Your TOKEN was expired. So please logout and login again")
    else:
        return await msg.edit(text=f"Error: {data['msg']}")

    url_for_upload = data['result']
    filename = file_location.split("/")[-1]

    with open(file_location, "rb") as f:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"api_key": api_key, "file": f}) as response:
                up = await response.text()
    print(up)
    try:
        os.remove(file_location)

        url = f"https://doodapi.com/api/file/info?key={api_key}&file_code={dic['file_code']}"
        data = await req(url)
        text = f"**📁 Title:** {data['result'][0]['title']}\n\n"
        text += f"**⏰ Duration:** {TimeFormatter(int(data['result'][0]['length']) * 1000)}\n\n"
        text += f"**📊 Size:** {humanbytes(int(data['result'][0]['size']))}\n\n"
        text += f"**👁 Views:** {data['result'][0]['views']}\n\n"
        text += f"**📆 Uploaded on:** {data['result'][0]['uploaded']}"
        buttons = [[
            InlineKeyboardButton("Rename ✏", callback_data=f"rename+{data['result'][0]['filecode']}"),
            InlineKeyboardButton("Download 📥", url=f"{dic['file_url']}"),
            ],[
            InlineKeyboardButton("Watch Online 👀", url=f"https://dood.so{data['result'][0]['protected_embed']}")
        ]]
        return await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        print(f'Sorry i am unable to upload tg file due to {e}')
        return await msg.edit(f"unsupported video format {filename}, please upload video with mkv, mp4, wmv, avi, mpeg4, mpegps, flv, 3gp, webm, mov, mpg & m4v format")

