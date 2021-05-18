import time
from pyrogram import Client, filters
from ..tools.progress_bar import progress_bar
from ..config import Config


@Client.on_message((filters.document|filters.video))
async def tg_upload(c, m):
    await m.download()
