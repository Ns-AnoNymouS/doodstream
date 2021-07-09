from pyrogram import Client, filters


@Client.on_callback_query(filters.regex(''))
async def delete(c, m):
    data = m.data.split('+')
    if len(data) == 2:
        cmd, fileId = data
    else:
        cmd, fileId, folderId = data

    
