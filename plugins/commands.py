from pyrogram import Client, filters


@Client_on_message(filters.command('token'))
async def login(c, m):
    if len(m.command) == 2:
        url = f"https://doodapi.com/api/account/info?key={api_key}"
