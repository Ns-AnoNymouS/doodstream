from ..tools.requests import reqPost
from pyrogram import Client, filters


@Client.on_callback_query(filters.regex(''))
async def delete(c, m):
    data = m.data.split('+')
    folderId = 0
    if len(data) == 2:
        cmd, fileId = data
    else:
        cmd, fileId, folderId = data

    postData = {
        'fld_id: int(folderId),
        'file_id': int(fileId),
        'op': 'videos_json',
        'del_selected': 'Delete selected',
        'token': a44f6bd5ce74c6e5f263727a47f02638
    }
    jsonData = await reqPost('https://doodstream.com/', postData)
    print(jsonData)
