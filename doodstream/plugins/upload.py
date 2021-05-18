import os
import time
from pyrogram import Client, filters
from ..tools.progress_bar import progress_bar
from ..config import Config


@Client.on_message((filters.document|filters.video))
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

    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/upload/server?key={api_key}" 
    data = requests.get(url).json()
    url_for_upload = data['result']
    post_files = {"file": (filename, open(file_location, "rb"))}
    post_data = {"api_key": api_key}
    up = requests.post(url_for_upload, data=post_data, files=post_files)
    print(data)
    print(up.text)
