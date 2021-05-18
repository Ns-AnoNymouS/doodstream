from pyrogram import Client, filters

@Client.on_message((filters.document|filters.video))
async def tg_upload(c, m):
    
