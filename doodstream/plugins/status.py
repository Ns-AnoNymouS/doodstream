import asyncio
import requests
import concurrent.futures
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('status') & filters.private & filters.incoming)
async def status(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    url = f"https://doodapi.com/api/account/info?key={api_key}"
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        userdetails = await loop.run_in_executor(pool, requests.get, url)
    userdetails = userdetails.json()
    if userdetails['status'] == 403:
        text = "Your Token expired"
    elif userdetails['status'] == 200:
        await c.db.update_credential_status(m.from_user.id,  api_key)
        text = "--**Your Details:**--\n\n"
        text += f"**👤 Email:** {userdetails['result']['email']}\n" if 'email' in userdetails['result'] else ""
        text += f"**💰 Balance:** {userdetails['result']['balance']}\n" if 'balance' in userdetails['result'] else ""   
        text += f"**📈 Storage left:** {userdetails['result']['storage_left']}\n" if 'storage_left' in userdetails['result'] else ""
        text += f"**💠 Premium Expiry:** {userdetails['result']['premim_expire']}\n" if 'premim_expire' in userdetails['result'] else "" 
    else:
        text = f"Error: {userdetails['msg']}"

    await m.reply_text(text)
