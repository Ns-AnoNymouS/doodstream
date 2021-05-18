from pyrogram import Client, filters
from ..tools.progress_bar import progress_bar


@Client.on_message((filters.document|filters.video))
async def tg_upload(c, m):
    
