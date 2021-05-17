import requests
from pyrogram import Client, filters


@Client.on_message(filters.command('token'))
async def token(c, m):
    if len(m.command) == 2:
        cmd, api_key = m.text.split(' ')
        url = f"https://doodapi.com/api/account/info?key={api_key}"
        userdetails = requests.get(url).json()
        if userdetails['status'] == 403:
            text = "Send me the correct token"
        elif userdetails['status'] == 200:
            await c.db.update_credential_status(m.from_user.id,  api_key)
            text = "--**Your Details:**--\n\n"
            text += f"**Email:** {userdetails['result']['email']}\n" if 'email' in userdetails['result'] else ""
            text += f"**Balance:** {userdetails['result']['balance']}\n" if 'balance' in userdetails['result'] else ""   
            text += f"**Storage left:** {userdetails['result']['storage_left']}\n" if 'storage_left' in userdetails['result'] else ""
            text += f"**Premium Expiry:** {userdetails['result']['premim_expire']}\n" if 'premim_expire' in userdetails['result'] else "" 
        else:
            text = "Something Went wrong"
        await m.reply_text(text)


@Client.on_message(filters.command('myfiles'))
async def myfiles(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/folder/list?key={api_key}"
    data = requests.get(url).json()
    await m.reply_text(data)
