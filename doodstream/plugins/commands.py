import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('login') & filters.private & filters.incoming)
async def login(c, m):
    url = "https://doodstream.com/?op=my_account&generate_api_key=1"
    buttons = [[InlineKeyboardButton("Auth URL", url=url)]]
    await m.reply_text(
        text="--**Follow The below steps to login**--\n\n    • Open [Dood stream](http://doodstream.com) and login to the account\n\n    • And then press the below button and copy the API Key and paste here in the format `/token xxxxxxx...`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_message(filters.command('token') & filters.private & filters.incoming)
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


@Client.on_message(filters.private & filters.incoming)
async def token_check(c, m):
    api_key = await c.db.get_credential_status(m.from_user.id)
    if not api_key:
        return await m.reply_text("You didn't Authorize me yet")
    await m.continue_propagation()
