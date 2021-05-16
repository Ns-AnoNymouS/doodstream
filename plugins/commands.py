import requests
from pyrogram import Client, filters


@Client.on_message(filters.command('token'))
async def login(c, m):
    if len(m.command) == 2:
        cmd, api_key = m.text.split(' ')
        url = f"https://doodapi.com/api/account/info?key={api_key}"
        userdetails = requests.get(url).json()
        if userdetails['status'] == 403:
            text = "Send me the correct token"
        if userdetails['status'] == 200:
            text = "--**Your Details:**--\n\n"
            text += f"**Email:** {userdetails['result']['email']}\n" if 'email' in userdetails['result'] else ""
            text += f"**Balance:** {userdetails['result']['balance']}\n" if 'balance' in userdetails['result'] else ""   
            text += f"**Storage left:** {userdetails['result']['storage_left']}\n" if 'storage_left' in userdetails['result'] else ""
            text += f"**Premium Expiry:** {userdetails['result']['premim_expire']}\n" if 'premim_expire' in userdetails['result'] else "" 
        await m.reply_text(text)
